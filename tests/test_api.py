import json
import os
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from arccraft.service import app, SyntheticRequest, synthetic_run

class ContractTests(unittest.TestCase):
    def setUp(self): self.client=TestClient(app)
    def test_health_and_closed_artifact_registry(self):
        response=self.client.get('/api/v1/health')
        self.assertEqual(response.json()['status'],'ok')
        self.assertIsNone(response.json()['archive_doi'])
        self.assertEqual(self.client.get('/api/v1/artifacts/unknown').status_code,404)
    def test_canonical_parameters_cannot_be_changed(self):
        for payload in [{'seed':4},{'worlds':200},{'variant':'no_validator'},{'unknown':1},{'worlds':True},{'seed':-1}]:
            self.assertEqual(self.client.post('/api/v1/simulate/synthetic',json=payload).status_code,422,payload)
    def test_registered_selection_is_closed(self):
        self.assertEqual(self.client.post('/api/v1/simulate/synthetic',json={'mode':'REGISTERED_VARIANT','seed':42}).status_code,422)
    def test_motor_no_leakage_and_assumption_pair(self):
        for payload in [{'start_year':2024},{'n_simulations':10000},{'mode':'EXPLORATORY','expense_ratio':0.1},{'mode':'EXPLORATORY','frequency_multiplier':-1}]:
            self.assertEqual(self.client.post('/api/v1/simulate/motor',json=payload).status_code,422,payload)
    def test_payload_limit(self):
        self.assertEqual(self.client.post('/api/v1/simulate/synthetic',content='x'*5000).status_code,413)
    def test_public_compute_fails_closed(self):
        with patch.dict(os.environ,{'VERCEL':'1','ARCCRAFT_COMPUTE_PROTECTION':''}):
            self.assertFalse(self.client.get('/api/v1/health').json()['live_computation'])
            self.assertEqual(self.client.post('/api/v1/simulate/motor',json={}).status_code,503)
    def test_motor_reference_and_exploration_are_distinct(self):
        canonical=self.client.post('/api/v1/simulate/motor',json={}).json()
        self.assertEqual(canonical['proof_status'],'VERIFIED')
        exploratory=self.client.post('/api/v1/simulate/motor',json={'mode':'EXPLORATORY','severity_multiplier':1.25}).json()
        self.assertEqual(exploratory['proof_status'],'EXPLORATORY_NOT_VALIDATED')
        self.assertNotEqual(canonical['output_semantic_sha256'],exploratory['output_semantic_sha256'])
    def test_full_precision_canonical_and_rejects(self):
        result=synthetic_run(SyntheticRequest(world_id=1))
        self.assertEqual(result['proof_status'],'VERIFIED')
        self.assertEqual(result['selected_world']['world_id'],1)
        rejected=[r for r in result['atlas'] if r['statut_validation']=='REJECT']
        self.assertEqual(len(rejected),5)
        self.assertTrue(all(r['combined_ratio'] is None and r['tracabilite_score'] is None for r in rejected))
        json.dumps(result,allow_nan=False)
    def test_all_registered_adapter_fingerprints(self):
        for variant in ['full','no_validator','strict_reject','no_transitions','shared_stream']:
            for seed in [20260825,20260826,20260827]:
                with self.subTest(variant=variant,seed=seed):
                    r=synthetic_run(SyntheticRequest(mode='REGISTERED_VARIANT',variant=variant,seed=seed))
                    self.assertEqual(r['proof_status'],'VERIFIED')

if __name__=='__main__':unittest.main()
