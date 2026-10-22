import json,subprocess,sys,tempfile,unittest
from pathlib import Path
class InterfaceTests(unittest.TestCase):
 def test_three_languages(self):
  for lang in ('fr','en','es'):
   r=subprocess.run([sys.executable,'-m','sql_lineage_perturbation','examples/demo.json','--lang',lang],capture_output=True,text=True)
   self.assertEqual(r.returncode,0,r.stderr); d=json.loads(r.stdout);self.assertEqual(d['language'],lang);self.assertTrue(d['summary'])
 def test_invalid_input_localized(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'bad.json';p.write_text('{"x":NaN}')
   messages=[]
   for lang in ('fr','en','es'):
    r=subprocess.run([sys.executable,'-m','sql_lineage_perturbation',str(p),'--lang',lang],capture_output=True,text=True)
    self.assertEqual(r.returncode,2);self.assertEqual(r.stdout,'');d=json.loads(r.stderr);self.assertEqual(d['code'],'invalid_input');messages.append(d['message'])
   self.assertEqual(len(set(messages)),3)
