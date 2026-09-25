"""Describe platform drift without changing the reference or accepting a tolerance."""
import argparse, json, sys, platform
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from arccraft.service import SyntheticRequest, MotorRequest, synthetic_run, motor, digest, REGISTRY

def compare(actual, expected):
    changes=[]; structure=[]
    def walk(a,b,path=''):
        if isinstance(a,dict) and isinstance(b,dict):
            if a.keys()!=b.keys():structure.append(path+': keys')
            for key in a.keys()&b.keys():walk(a[key],b[key],path+'/'+str(key))
        elif isinstance(a,list) and isinstance(b,list):
            if len(a)!=len(b):structure.append(path+': length')
            for i,(x,y) in enumerate(zip(a,b)):walk(x,y,path+'/'+str(i))
        elif a!=b:
            if type(a) in (float,int) and type(b) in (float,int):changes.append({'path':path,'reference':b,'actual':a,'absolute_difference':abs(a-b)})
            else:structure.append(path)
    walk(actual,expected)
    return {'numerical_fields_different':len(changes),'max_absolute_difference':max((r['absolute_difference'] for r in changes),default=0),'non_numerical_differences':structure,'examples':changes[:12],'max_difference_examples':sorted(changes,key=lambda r:r['absolute_difference'],reverse=True)[:8]}

def main():
    p=argparse.ArgumentParser();p.add_argument('--synthetic-json');p.add_argument('--motor-json');p.add_argument('--output',default='test-results/cross-runtime.json');args=p.parse_args()
    s=json.loads(Path(args.synthetic_json).read_text(encoding='utf-8')) if args.synthetic_json else synthetic_run(SyntheticRequest())
    m=json.loads(Path(args.motor_json).read_text(encoding='utf-8')) if args.motor_json else motor(MotorRequest())
    golden=json.loads((ROOT/'artifacts/candidate/canonical-worlds.json').read_text(encoding='utf-8'))
    motor_golden=json.loads((ROOT/'artifacts/candidate/motor-forecast.json').read_text(encoding='utf-8'))
    report={'policy':'Exact reference unchanged; no tolerance introduced. DIVERGENT remains DIVERGENT.',
      'reference_environment':'Windows AMD64 / Python 3.12.14 / NumPy 2.3.5',
      'synthetic':{'runtime':s['runtime'],'proof_status':s['proof_status'],'output_semantic_sha256':s['output_semantic_sha256'],'expected_semantic_sha256':s['expected_semantic_sha256'],'historical_fingerprint':s['historical_fingerprint'],'historical_fingerprint_matches':s['historical_fingerprint']==REGISTRY['registered_fingerprints']['full:20260825'],**compare(s['result'],golden)},
      'motor':{'runtime':m['runtime'],'proof_status':m['proof_status'],'output_semantic_sha256':m['output_semantic_sha256'],'expected_semantic_sha256':m['expected_semantic_sha256'],**compare(m['result'],motor_golden)}}
    for response in [s,m]:
        assert digest(response['result'])==response['output_semantic_sha256']
        assert response['proof_status']==('VERIFIED' if response['output_semantic_sha256']==response['expected_semantic_sha256'] else 'DIVERGENT')
    out=ROOT/args.output;out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({k:{x:v[x] for x in ['proof_status','numerical_fields_different','max_absolute_difference','non_numerical_differences']} for k,v in report.items() if isinstance(v,dict)},indent=2))
if __name__=='__main__':main()
