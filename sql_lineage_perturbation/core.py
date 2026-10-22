from collections import Counter
import json,sqlite3
from .common import identifier

ALLOWED_FUNCTIONS={'count','sum','avg','min','max','total','coalesce','ifnull','nullif','abs','round','lower','upper','length','substr','substring','trim'}
def quote(x):return '"'+x.replace('"','""')+'"'
def run(data):
    tables=data['tables'];query=data['query']
    if not isinstance(query,str) or len(query)>20000 or not 1<=len(tables)<=10:raise ValueError('query')
    conn=sqlite3.connect(':memory:');locations=[]
    try:
        for name,table in tables.items():
            identifier(name);columns=table['columns'];rows=table['rows']
            if not columns or len(columns)>30 or len(set(columns))!=len(columns):raise ValueError('columns')
            for c in columns:identifier(c)
            if 'rowid' in {c.lower() for c in columns} or '_rowid_' in {c.lower() for c in columns}:raise ValueError('reserved_rowid')
            conn.execute('CREATE TABLE '+quote(name)+' ('+','.join(quote(c) for c in columns)+')')
            for i,row in enumerate(rows,1):
                if len(row)!=len(columns) or any(isinstance(v,(dict,list,bool)) for v in row):raise ValueError('row')
                conn.execute('INSERT INTO '+quote(name)+' VALUES ('+','.join('?' for _ in columns)+')',row);locations.append((name,i,row,columns))
            if len(locations)>100:raise ValueError('size')
        def authorize(action,a,b,db,trigger):
            if action in (sqlite3.SQLITE_SELECT,sqlite3.SQLITE_READ):return sqlite3.SQLITE_OK
            if action==sqlite3.SQLITE_FUNCTION and (b or a or '').lower() in ALLOWED_FUNCTIONS:return sqlite3.SQLITE_OK
            return sqlite3.SQLITE_DENY
        def evaluate():
            calls=[0]
            def stop():calls[0]+=1;return calls[0]>1000
            conn.set_authorizer(authorize);conn.set_progress_handler(stop,100)
            try:
                values=conn.execute(query).fetchmany(1001)
                if len(values)>1000:raise ValueError('result_size')
                return Counter(json.dumps(row,sort_keys=True,allow_nan=False) for row in values)
            except sqlite3.Error as e:raise ValueError('restricted_query') from e
            finally:conn.set_authorizer(None);conn.set_progress_handler(None,0)
        baseline=evaluate();effects=[]
        for name,i,row,columns in locations:
            conn.execute('DELETE FROM '+quote(name)+' WHERE rowid=?',(i,))
            changed=evaluate();conn.execute('INSERT INTO '+quote(name)+' (rowid,'+','.join(quote(c) for c in columns)+') VALUES ('+','.join('?' for _ in range(len(columns)+1))+')',[i]+row)
            if changed!=baseline:effects.append({'table':name,'rowid':i,'removed_result_rows':list((baseline-changed).elements()),'added_result_rows':list((changed-baseline).elements())})
        return {'baseline_rows':[json.loads(v) for v in baseline.elements()],'influential_single_deletions':effects,'checked_source_rows':len(locations),'scope':'bag semantics; individual deletion sensitivity, not complete logical provenance'}
    finally:conn.close()
