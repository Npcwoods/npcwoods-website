import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
from contextlib import redirect_stdout, redirect_stderr
from tests.test_deploy_tool import load_module, PAGE


class ApprovalSnapshotTest(unittest.TestCase):
    def test_changed_approval_hash_blocks_before_loading_credentials(self):
        m = load_module()
        with mock.patch.object(m, 'sftp_connect', side_effect=AssertionError('must not contact SFTP')), mock.patch.object(m, 'load_env') as credentials, redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            code = m.main(['deploy.py', '--pages', PAGE, '--live', '--confirm-live-deploy',
                           m.LIVE_DEPLOY_CONFIRMATION, '--expected-source-hashes', json.dumps({PAGE: '0' * 64})])
        self.assertEqual(code, 2)
        credentials.assert_not_called()

    def test_live_cannot_skip_required_verification(self):
        m = load_module()
        with mock.patch.object(m, 'sftp_connect', side_effect=AssertionError('must not contact SFTP')), mock.patch.object(m, 'load_env') as credentials, redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            code = m.main(['deploy.py', '--pages', PAGE, '--live', '--skip-verify',
                           '--confirm-live-deploy', m.LIVE_DEPLOY_CONFIRMATION])
        self.assertEqual(code, 2)
        credentials.assert_not_called()

    def test_upload_uses_exact_bytes_checked_in_plan(self):
        m = load_module()
        self.assertTrue(callable(getattr(m, 'upload_planned_page', None)), 'upload needs an immutable checked snapshot')
        with tempfile.TemporaryDirectory() as tmp:
            local = Path(tmp) / 'page/index.html'
            local.parent.mkdir()
            local.write_text('<!doctype html><title>Approved</title><h1>Approved</h1>')
            with mock.patch.object(m, 'local_path_for', return_value=local):
                plan = m.build_plan(['page'])
            expected = local.read_bytes()
            local.write_text('unreviewed later edit')
            sftp = mock.Mock()
            uploaded = []
            sftp.putfo.side_effect = lambda file, remote: uploaded.append(file.read())
            m.upload_planned_page(sftp, plan[0])
            self.assertEqual(uploaded, [expected])

