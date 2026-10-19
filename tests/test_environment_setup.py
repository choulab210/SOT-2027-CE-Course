"""Regression checks: validation must never install packages in the kernel.
Run: python -m unittest discover -s tests -v
"""
import contextlib
import importlib
import importlib.metadata
import inspect
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
NB=json.loads((ROOT/'MNP_Transfer_Learning_Colab.ipynb').read_text(encoding='utf-8'))
SOURCE=''.join(next(c for c in NB['cells'] if c['id']=='install')['source'])

class EnvironmentSetupTests(unittest.TestCase):
    def execute(self):
        namespace={}
        with contextlib.redirect_stdout(io.StringIO()), patch('subprocess.check_call',side_effect=AssertionError('Setup must never invoke pip')):
            exec(compile(SOURCE,'notebook_setup','exec'),namespace)
        return namespace

    def test_healthy_environment_is_retained(self):
        names=['torch','numpy','pandas','scikit-learn','matplotlib']
        before={n:importlib.metadata.version(n) for n in names}
        namespace=self.execute()
        self.assertFalse(namespace['problems'])
        self.assertEqual(before,{n:importlib.metadata.version(n) for n in names})

    def test_missing_package_stops_with_restart_guidance(self):
        original=importlib.import_module
        def simulated(name,*args,**kwargs):
            if name=='pandas':raise ModuleNotFoundError("No module named 'pandas'")
            return original(name,*args,**kwargs)
        with patch('importlib.import_module',side_effect=simulated):
            with self.assertRaisesRegex(RuntimeError,'restart.*runtime'):
                self.execute()

    def test_numpy_import_failure_stops_without_installing(self):
        original=importlib.import_module
        def simulated(name,*args,**kwargs):
            if name=='numpy':raise ImportError("cannot import name '_slice' from numpy._core.umath")
            return original(name,*args,**kwargs)
        with patch('importlib.import_module',side_effect=simulated):
            with self.assertRaisesRegex(RuntimeError,'No packages were changed'):
                self.execute()

    def test_loaded_disk_version_mismatch_stops(self):
        original=importlib.metadata.version
        with patch('importlib.metadata.version',side_effect=lambda name:'0.0.0' if name=='numpy' else original(name)):
            with self.assertRaisesRegex(RuntimeError,'STOP'):
                self.execute()

    def test_required_torch_api_is_checked(self):
        import torch
        original=inspect.signature
        with patch('inspect.signature',side_effect=lambda obj:inspect.Signature() if obj is torch.load else original(obj)):
            with self.assertRaisesRegex(RuntimeError,'STOP'):
                self.execute()

if __name__=='__main__': unittest.main()
