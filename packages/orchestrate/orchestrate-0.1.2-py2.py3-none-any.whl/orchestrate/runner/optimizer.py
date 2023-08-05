from __future__ import print_function
import json
import os
import six
import subprocess
import sys
import warnings

from sigopt import Connection
from sigopt.exception import ApiException

from orchestrate.common import safe_format
from orchestrate.runner.log_parser import LogParser

class BaseOptimizer(object):
  def __init__(self, config, suggestion_path, log_path, pod_name):
    self.suggestion_path = suggestion_path
    self.log_path = log_path
    self.metrics = config['metrics']
    self.run_command_list = config['run_commands']
    self.pod_name = pod_name

  def optimization_loop(self):
    while self.is_experiment_running():
      self.run_observation()

  def run_observation(self):
    suggestion_json = self.get_suggestion_json()
    with open(self.suggestion_path, 'w') as suggestion_fp:
      json.dump(suggestion_json, suggestion_fp)
    open(self.log_path, 'w').close()
    called_process_error = None
    try:
      self.run_user_commands()
    except subprocess.CalledProcessError as cpe:
      called_process_error = cpe
    finally:
      parsed_logs = LogParser(self.log_path, self.metrics)
      os.remove(self.log_path)
      os.remove(self.suggestion_path)
    self.create_observation(
      suggestion_json=suggestion_json,
      parsed_logs=parsed_logs,
      called_process_error=called_process_error,
    )

  def run_user_commands(self):
    env = os.environ.copy()
    env.update({
      'ORCHESTRATE_IO_ENABLED': 'true',
      'ORCHESTRATE_LOG': self.log_path,
      'ORCHESTRATE_SUGGESTION': self.suggestion_path,
    })
    for command in self.run_command_list:
      subprocess.check_call(command, bufsize=1, env=env, shell=True)

  def log_observation(self, **kwargs):
    sys.stdout.write("Observation data: ")
    json.dump(kwargs, sys.stdout)
    sys.stdout.write(os.linesep)
    sys.stdout.flush()

  def create_observation(self, suggestion_json, parsed_logs, called_process_error=None):
    if parsed_logs.failed:
      warnings.warn(safe_format(
        "A failure was logged for suggestion {}",
        suggestion_json['id'],
      ), RuntimeWarning)
    if called_process_error is not None:
      warnings.warn(str(called_process_error), RuntimeWarning)
      parsed_logs.set_failed()
    values, metadata, failed, missing_metrics = parsed_logs.get_observation_data()
    suggestion_id = suggestion_json['id']
    base_meta = {'pod_name': self.pod_name}
    if called_process_error is not None:
      base_meta['failed_command'] = called_process_error.cmd
      base_meta['failed_return_code'] = called_process_error.returncode
    if missing_metrics:
      base_meta['missing_metrics'] = ','.join(sorted(missing_metrics))

    observation_meta = base_meta.copy()
    observation_meta.update(metadata)
    self.log_observation(
      suggestion=suggestion_id,
      values=values,
      failed=failed,
      metadata=observation_meta,
    )
    try:
      self.report_observation(
        suggestion=suggestion_id,
        values=values,
        failed=failed,
        metadata=observation_meta,
      )
    except ApiException as api_exception:
      if api_exception.status_code == 400:
        observation_meta = base_meta.copy()
        observation_meta['metadata_report_failed'] = True
        try:
          obs = self.report_observation(
            suggestion=suggestion_id,
            values=values,
            failed=failed,
            metadata=observation_meta,
          )
        except Exception as e:
          self.handle_failed_observation(suggestion_id, safe_format(
            "SigOpt api call failed twice: {}",
            str(e),
          ))
          six.raise_from(e, api_exception)
        else:
          self.handle_failed_metadata(obs.id, str(api_exception))
      else:
        self.handle_failed_observation(suggestion_id, str(api_exception))
        raise

  def handle_failed_observation(self, suggestion_id, reason):
    warnings.warn(safe_format(
      "The observation report for suggestion {} failed: {}",
      suggestion_id,
      reason,
    ), RuntimeWarning)

  def handle_failed_metadata(self, observation_id, reason):
    warnings.warn(safe_format(
      "The report for observation {} with metadata failed: {}",
      observation_id,
      reason,
    ), RuntimeWarning)

  def is_experiment_running(self):
    raise NotImplementedError()

  def get_suggestion_json(self):
    raise NotImplementedError()

  def report_observation(self, **kwargs):
    raise NotImplementedError()

class SigOptOptimizer(BaseOptimizer):
  def __init__(self, config, suggestion_path, log_path, pod_name, experiment_id):
    super(SigOptOptimizer, self).__init__(config, suggestion_path, log_path, pod_name)
    self.conn = Connection()
    self.experiment_id = experiment_id

  def is_experiment_running(self):
    experiment = self.conn.experiments(self.experiment_id).fetch()
    return experiment.progress.observation_count < experiment.observation_budget

  def get_suggestion_json(self):
    return self.conn.experiments(self.experiment_id).suggestions().create().to_json()

  def report_observation(self, **kwargs):
    self.conn.experiments(self.experiment_id).observations().create(**kwargs)
