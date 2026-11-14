"""Only verify opt-in boundary; CI never downloads or loads neural weights."""
from pathlib import Path
import subprocess
import sys
import unittest

SCRIPT = Path(__file__).with_name("real_embedding_eval.py")


class RealEmbeddingBoundary(unittest.TestCase):
    def test_dry_run_has_no_install_or_network(self):
        p = subprocess.run([sys.executable, str(SCRIPT)], text=True, capture_output=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("DRY RUN ONLY", p.stdout)

    def test_nonlocal_model_path_fails_before_import(self):
        p = subprocess.run([sys.executable, str(SCRIPT), "--model-path", "/unlikely/nonexistent/model"],
                           text=True, capture_output=True)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("existing local directory", p.stderr)


if __name__ == "__main__":
    unittest.main()
