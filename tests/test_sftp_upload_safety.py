import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "sftp-upload.py"


def load_module():
    spec = importlib.util.spec_from_file_location("sftp_upload", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SftpUploadSafetyTest(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_default_mode_is_dry_run_and_does_not_load_credentials(self):
        target = self.module.ROOT / "html" / "shared" / "tracking.js"
        with mock.patch.object(self.module, "load_env") as load_env:
            output = io.StringIO()
            with redirect_stdout(output):
                exit_code = self.module.main(["sftp-upload.py", str(target.relative_to(self.module.ROOT))])

        self.assertEqual(exit_code, 0)
        load_env.assert_not_called()
        self.assertIn("[dry-run]", output.getvalue())
        self.assertIn("add --execute", output.getvalue())

    def test_execute_requires_confirmation_phrase(self):
        target = self.module.ROOT / "html" / "shared" / "tracking.js"
        with mock.patch.object(self.module, "load_env") as load_env:
            exit_code = self.module.main(
                ["sftp-upload.py", "--execute", str(target.relative_to(self.module.ROOT))]
            )

        self.assertEqual(exit_code, 2)
        load_env.assert_not_called()

    def test_remote_path_blocks_paths_outside_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            outside = Path(tmp) / "outside.html"
            outside.write_text("x", encoding="utf-8")

            with self.assertRaises(ValueError):
                self.module.remote_path_for(outside)


if __name__ == "__main__":
    unittest.main()
