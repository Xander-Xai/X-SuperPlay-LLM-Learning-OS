"""No-key dry-run contract: never attempts a provider call in CI."""
import os
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "ragas_live_optional.py"


class OptionalRagasBoundary(unittest.TestCase):
    def test_default_is_offline_and_free(self):
        env = dict(os.environ)
        env.pop("OPENAI_API_KEY", None)
        p = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True,
                           text=True, env=env)
        self.assertEqual(p.returncode, 0)
        self.assertIn("NOT RUN", p.stdout)
        self.assertNotIn("Faithfulness example score", p.stdout)

    def test_live_requires_explicit_provider_key(self):
        env = dict(os.environ)
        env.pop("OPENAI_API_KEY", None)
        p = subprocess.run([sys.executable, str(SCRIPT), "--live"],
                           capture_output=True, text=True, env=env)
        self.assertEqual(p.returncode, 2)
        self.assertIn("NO-GO", p.stderr)

    def test_help_does_not_require_dependencies(self):
        p = subprocess.run([sys.executable, str(SCRIPT), "--help"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)
        self.assertIn("--model", p.stdout)


if __name__ == "__main__":
    unittest.main()
