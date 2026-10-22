import unittest
from sql_lineage_perturbation import run
D={'tables':{'t':{'columns':['id','value'],'rows':[['a',1],['b',2],['c',3]]}}}
class DomainTests(unittest.TestCase):
 def test_filtered_rows_not_influential(self):
  r=run(dict(D,query='SELECT sum(value) FROM t WHERE value<3'));self.assertEqual([x['rowid'] for x in r['influential_single_deletions']],[1,2]);self.assertEqual(r['baseline_rows'],[[3]])
 def test_duplicate_support_not_complete_provenance(self):
  r=run({'tables':{'t':{'columns':['value'],'rows':[[1],[1]]}},'query':'SELECT DISTINCT value FROM t'});self.assertEqual(r['influential_single_deletions'],[])
 def test_writes_rejected(self):
  with self.assertRaises(ValueError):run(dict(D,query='DELETE FROM t'))
 def test_nondeterministic_function_rejected(self):
  with self.assertRaises(ValueError):run(dict(D,query='SELECT random()'))
 def test_multiple_statements_rejected(self):
  with self.assertRaises(ValueError):run(dict(D,query='SELECT 1; DROP TABLE t'))
 def test_count_bag_multiplicity(self):
  r=run({'tables':{'t':{'columns':['v'],'rows':[[1],[1]]}},'query':'SELECT v FROM t'});self.assertEqual(len(r['influential_single_deletions']),2)
