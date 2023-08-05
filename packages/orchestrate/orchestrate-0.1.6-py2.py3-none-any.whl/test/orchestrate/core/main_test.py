import os
from mock import patch, Mock
import uuid

import pytest

from orchestrate.common import safe_format
from orchestrate.core.main import OrchestrateApp
from orchestrate.core.paths import get_executable_path


# From cement docs: http://builtoncement.com/2.10/dev/testing.html
class OrchestrateTestApp(OrchestrateApp):
  class Meta(object):
    argv = []
    config_files = []


class TestOrchestrateCommands(object):
  app_class = OrchestrateTestApp

  @pytest.mark.skip(reason="Need to mock")
  def test_orchestrate_run(self, tmpdir):
    with OrchestrateTestApp(argv=['init', '--directory', tmpdir]) as app:
      app.run()

    with OrchestrateTestApp(argv=['run', '--filename', safe_format('{}/orchestrate.yml', tmpdir)]) as app:
      with patch('orchestrate.core.run.sigopt.Connection') as mock_conn:
        mock_conn.return_value = Mock(
          experiments=Mock(
            return_value=Mock(
              create=Mock(
                return_value=Mock(id=uuid.uuid4())
              )
            )
          )
        )
        app.run()
        assert mock_conn.called

    os.remove(safe_format('{}/orchestrate.yml', tmpdir))

  def test_orchestrate_version(self):
    with OrchestrateTestApp(argv=['version']) as app:
      app.run()

  def test_orchestrate_init(self):
    with OrchestrateTestApp(argv=['init']) as app:
      app.run()

  def test_orchestrate_status(self):
    with OrchestrateTestApp(argv=['status']) as app:
      with pytest.raises(SystemExit) as e:
        app.run()
      assert e.value.code == 2

  @pytest.mark.skip(reason='job for 123 does not exist')
  def test_orchestrate_status_with_args(self):
    with OrchestrateTestApp(argv=['status', '123']) as app:
      with pytest.raises(NotImplementedError) as e:
        app.run()
      assert e.value.args[0] == "Status: 123"

  def test_orchestrate_logs(self):
    with OrchestrateTestApp(argv=['logs']) as app:
      with pytest.raises(SystemExit) as e:
        app.run()
      assert e.value.code == 2

  @pytest.mark.skip(reason='job for 123 does not exist')
  def test_orchestrate_logs_with_args(self):
    with OrchestrateTestApp(argv=['logs', '123']) as app:
      app.run()

  def test_orchestrate_kubectl(self):
    kubectl_env_dict = {
      'KUBECONFIG': 'dummy_kubeconfig',
      'PATH': '/dummy/bin',
    }
    with \
      patch('os.execvpe') as mock_execvpe, \
      patch('orchestrate.core.kubernetes.service.KubernetesService.kubectl_env', side_effect=kubectl_env_dict):
      with OrchestrateTestApp(argv=['kubectl', 'get', '-h']) as app:
        app.run()
      exec_path = get_executable_path('kubectl')
      assert mock_execvpe.called_once_with(
        exec_path,
        [exec_path, 'get', '-h'],
        env=kubectl_env_dict,
      )

  def test_unknown_arg(self):
    with OrchestrateTestApp(argv=['status-all', 'bogus', '--option']) as app:
      with pytest.raises(SystemExit) as e:
        app.run()
      assert e.value.code == 2
