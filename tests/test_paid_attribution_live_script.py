import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "verify-paid-attribution-live.mjs"


class PaidAttributionLiveScriptTest(unittest.TestCase):
    def test_self_test_runs_without_browser_or_network(self):
        completed = subprocess.run(
            ["node", str(SCRIPT), "--self-test"],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("ok verify-paid-attribution-live self-test", completed.stdout)


if __name__ == "__main__":
    unittest.main()
