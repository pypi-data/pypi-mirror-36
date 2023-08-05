from __future__ import print_function
import os
import six

from botocore.exceptions import NoRegionError
from cement.core.foundation import CementApp
from cement.ext.ext_argparse import ArgparseController
import yaml

from orchestrate.version import VERSION

from orchestrate.common import safe_format
from orchestrate.core.cement_utils import ArgparseArgumentHandler, expose
from orchestrate.core.paths import (
  check_iam_authenticator_executable,
  check_kubectl_executable,
)
from orchestrate.core.services.orchestrate_bag import OrchestrateServiceBag
from orchestrate.core.kubernetes.service import KubernetesError

class OrchestrateController(ArgparseController):
  class Meta(object):
    label = 'base'
    description = 'A machine learning training and tuning management tool built for parameter optimization'

  def default(self):
    print('run sigopt -h to see a list of commands')

  @expose(help="Current version")
  def version(self):
    print(VERSION)

  def runner(self, local=False):
    directory = self.app.pargs.directory

    options = self.app.user_options
    self.app.services.options_validator_service.validate_orchestrate_options(**options)

    name = options.get('name')
    optimization_options = options.get('optimization')
    resource_options = options.get('resources_per_model')
    language = options.get('language')
    framework = options.get('framework')

    repository_name = options.get('aws', {}).get('ecr', {}).get('repository')

    if not local:
      self.app.services.aws_service.login_to_container_registry(repository_name)

    image_name = repository_name

    image = self.app.services.model_packer_service.build_image(
      image_name=image_name,
      directory=directory,
      install_commands=options.get('install'),
      run_commands=options.get('run'),
      optimization_options=optimization_options,
      language=language,
      framework=framework,
    )

    if local:
      return self.app.services.job_runner_service.run_local_job(
        name=name,
        image_name=repository_name,
        optimization_options=optimization_options,
      )
    else:
      descriptions = self.app.services.ecr_service.describe_repositories([repository_name])
      target = descriptions['repositories'][0]['repositoryUri']
      image.tag(repository=target)
      self.app.services.docker_service.push(target)
      return self.app.services.job_runner_service.run_job(
        name=name,
        image_name=target,
        optimization_options=optimization_options,
        resource_options=resource_options,
      )

  @expose(
    help="Initialize a directory for orchestrate. Use with sigopt init >> orchestrate.yml",
  )
  def init(self):
    print(
        """name: My Orchestrate Experiment
install:
  -  # Fill in install commands, such as pip install -r requirements.txt
run:
  -  # Fill in run command, such as python model.py
optimization:
  parameters:  # Fill in parameters to optimize
  parallel_bandwidth: 1
  observation_budget: 10
""")

  @expose(
    arguments=[
      (['--directory'], dict(help='orchestrate project directory, default: current directory', default='.')),
      (['-f', '--filename'], dict(help='orchestrate yaml file, default: orchestrate.yml', default='orchestrate.yml')),
      (['-q', '--quiet'], dict(help='only print the experiment id', action='store_true')),
    ],
    help="Run orchestrate experiment",
  )
  def run(self):
    experiment_id = self.runner(local=False)
    if self.app.pargs.quiet:
      print(experiment_id)
    else:
      print(safe_format('Started experiment "{}"', experiment_id))

  @expose(
    arguments=[
      (['--directory'], dict(help='orchestrate project directory, default: current directory', default='.')),
      (['-f', '--filename'], dict(help='orchestrate yaml file, default: orchestrate.yml', default='orchestrate.yml'))
    ],
    help="Run a orchestrate experiment in a local docker container",
  )
  def run_local(self):
    self.runner(local=True)

  @expose(
    arguments=[
      (['experiment'], dict(help='An experiment id')),
    ],
    help='Deletes an experiment on the cluster (experiment will still exist on sigopt.com)',
  )
  def delete(self):
    experiment_id = self.app.pargs.experiment

    job_name = self.app.services.job_runner_service.job_name(experiment_id)
    try:
      self.app.services.kubernetes_service.delete_jobs(job_name)
    except KubernetesError as e:
      if 'NotFound' in str(e):
        raise Exception(safe_format('We could not find an experiment {} running on your cluster', experiment_id))
      else:
        raise e

  @expose(
    arguments=[
      (['experiment'], dict(help='An experiment id')),
    ],
    help='Retrieve experiment status',
  )
  def status(self):
    experiment_id = self.app.pargs.experiment

    job_name = self.app.services.job_runner_service.job_name(experiment_id)
    try:
      job = self.app.services.kubernetes_service.get_jobs(job_name)
    except KubernetesError as e:
      if 'NotFound' in str(e):
        raise Exception(safe_format('We could not find an experiment {} running on your cluster', experiment_id))
      else:
        raise e

    parsed_job = self.app.services.job_status_service.parse_job(job)

    observations_by_pod = self.app.services.job_status_service.get_observations_by_pod(experiment_id)
    total_failures = sum(v['failed'] for v in observations_by_pod.values())
    parsed_pods = [
      self.app.services.job_status_service.parse_pod(pod, observations_by_pod)
      for pod
      in self.app.services.kubernetes_service.get_pods(job_name=job_name)['items']
    ]

    print(safe_format('Job Status: {status}', **parsed_job))
    print(safe_format(
      '\n{observation_count} / {observation_budget} Observations',
      **parsed_job
    ))
    print(safe_format('{} Observation(s) failed', total_failures))

    print('\nPod status:')
    print(safe_format(
      '\n{:20}\t{:25}\t{:20}\t{:20}',
      "Pod Name",
      "Status",
      "Success",
      "Failed",
    ))
    for parsed_pod in parsed_pods:
      print(safe_format(
        '{name:20}\t{status:25}\t{success:<20}\t{failed:<20}',
        **parsed_pod
      ))

    print(safe_format(
      '\nView more at: https://app.sigopt.com/experiment/{}',
      experiment_id
    ))

  @expose(
    help='Retrieve all experiments\' statuses',
  )
  def status_all(self):
    parsed_jobs = [
      self.app.services.job_status_service.parse_job(job)
      for job in
      self.app.services.kubernetes_service.get_jobs()['items']
    ]

    print(safe_format('Total Jobs: {}', len(parsed_jobs)))
    print(safe_format(
      '\n{:20}\t{:20}\t{:20}\t{:20}\t{:20}',
      "Experiment ID",
      "Job Name",
      "Job Status",
      "Observation Count",
      "Observation Budget",
    ))
    for parsed_job in parsed_jobs:
      print(safe_format(
        '{experiment_id:20}'
        '\t{name:20}'
        '\t{status:20}'
        '\t{observation_count:<20}'
        '\t{observation_budget:<20}',
        **parsed_job
      ))

  @expose(
    arguments=[
      (['experiment'], dict(help='An experiment id')),
      (['--tail', '-t'], dict(help='Option to tail all logs', action='store_true')),
      (['--color-off', '-c'], dict(help='Remove color from tailed logs', action='store_true')),
    ],
    help='Retrieve experiment logs',
  )
  def logs(self):
    if self.app.pargs.tail:
      self.app.services.job_logs_service.tail_logs(self.app.pargs.experiment, self.app.pargs.color_off)
    else:
      self.app.services.job_logs_service.get_logs(self.app.pargs.experiment)

  @expose(
    add_help=False,
    ignore_unknown_arguments=True,
  )
  def kubectl(self):
    cmd = self.app.services.kubernetes_service.kubectl_command
    args = [cmd] + self.app.args.unknown_args
    os.execvpe(
      cmd,
      args,
      self.app.services.kubernetes_service.kubectl_env(),
    )

  @expose(
    help='Check that Orchestrate is installed properly',
  )
  def test(self):
    failed = False
    for name, check, extra in [
      ('kubectl', check_kubectl_executable, None),
      ('aws-iam-authenticator', check_iam_authenticator_executable, None),
      ('docker', self.app.services.docker_service.check_connection, None),
      (
        'SigOpt connection',
        self.app.services.sigopt_service.check_connection,
        "You can get your API token from https://app.sigopt.com/tokens/info."
        " See https://app.sigopt.com/docs/overview/authentication for more information.",
      ),
    ]:
      try:
        check()
      except Exception as e:
        print(safe_format("{} error: {}", name, str(e)))
        if extra:
          print(extra)
        failed = True

    if failed:
      print(
        "One or more checks failed."
        " Correct the issues and run `sigopt test` again."
      )
    else:
      print("All checks passed, you can start using SigOpt Orchestrate!")


class OrchestrateClusterController(ArgparseController):
  class Meta(object):
    label = 'cluster'
    stacked_on = 'base'
    stacked_type = 'nested'
    description = 'Handle the cluster interface'

  def default(self):
    print('run sigopt cluster -h to see a list of commands')

  @expose(
    help='create a cluster',
    arguments=[
      (['-f', '--filename'], dict(help='cluster config yaml file, default: cluster.yml', default='cluster.yml')),
    ],
  )
  def create(self):
    config = self.app.services.kubernetes_service.kube_config
    if config is not None:
      cluster_name = self.app.services.kubernetes_service.cluster_name_from_config(config)
      raise Exception(safe_format("Please disconnect from cluster: {} before creating a new cluster", cluster_name))

    options = self.app.user_options
    self.app.services.options_validator_service.validate_cluster_options(**options)
    self.app.services.aws_service.create_kubernetes_cluster(options)
    print(safe_format('Successfully created kubernetes cluster: {}', options['cluster_name']))

  @expose(
    help='destroy a cluster',
    arguments=[
      (['--cluster-name', '-n'], dict(help='cluster name', required=True)),
    ],
  )
  def destroy(self):
    cluster_name = self.app.pargs.cluster_name
    self.app.services.aws_service.destroy_kubernetes_cluster(cluster_name=cluster_name)
    print(safe_format('Successfully destroyed kubernetes cluster: {}', cluster_name))

  @expose(
    help='connect to a cluster',
    arguments=[
      (['--cluster-name', '-n'], dict(help='cluster name', required=True)),
    ],
  )
  def connect(self):
    cluster_name = self.app.pargs.cluster_name

    config = self.app.services.kubernetes_service.kube_config
    if config is not None:
      current_cluster_name = self.app.services.kubernetes_service.cluster_name_from_config(config)
      if cluster_name != current_cluster_name:
        raise Exception(
          safe_format("Please disconnect from cluster: {} before connecting to a new cluster", current_cluster_name)
        )

    self.app.services.aws_service.connect_kubernetes_cluster(cluster_name=cluster_name)
    print(safe_format('Successfully connected to kubernetes cluster: {}', cluster_name))

  @expose(
    help='disconnect from a cluster',
    arguments=[
      (['--cluster-name', '-n'], dict(help='cluster name')),
      (['--all', '-a'], dict(help='disconnect from all connected clusters', action='store_true')),
    ],
  )
  def disconnect(self):
    config_map = self.app.services.kubernetes_service.get_config_map()
    cluster_name = self.app.pargs.cluster_name
    disconnect_all = self.app.pargs.all

    if (cluster_name and disconnect_all) or (not cluster_name and not disconnect_all):
      raise Exception('Must provide exactly one of --cluster-name <cluster_name> and --all')

    if cluster_name:
      if cluster_name not in config_map:
        raise Exception(safe_format('You are not currently connected to cluster {}', cluster_name))
      cluster_names = [cluster_name]
    else:
      cluster_names = config_map.keys()

    if not cluster_names:
      raise Exception('No connected clusters to disconnect from')

    for cluster_name in cluster_names:
      try:
        self.app.services.aws_service.disconnect_kubernetes_cluster(cluster_name=cluster_name)
        print(safe_format('Successfully disconnected from kubernetes cluster: {}', cluster_name))
      except Exception as e:
        six.raise_from(Exception(safe_format(
          'Looks like an error occured while attempting to disconnect from cluster "{}".',
          cluster_name
        )), e)

  @expose(help='test your current cluster connection')
  def test(self):
    config_map = self.app.services.kubernetes_service.get_config_map()
    if not config_map:
      raise Exception("You are not currently connected to any clusters")
    if len(config_map) > 1:
      raise Exception(safe_format(
        "You are currently connected to more than one cluster:\n\t{}", "\n\t".join(config_map.keys())
      ))

    self.app.services.aws_service.test_kubernetes_cluster()
    cluster_name = list(config_map.keys())[0]
    print(safe_format('Successfully connected to kubernetes cluster: {}', cluster_name))


def load_options(app):
  try:
    with open(app.pargs.filename) as f:
      options = yaml.safe_load(f) or {}
    app.extend('user_options', options)
  except AttributeError:
    app.extend('user_options', None)


# TODO(alexandra): accept credentials as command line arguments for SigOpt and AWS
def extend_app_services(app):
  try:
    services = OrchestrateServiceBag(app.user_options)
  except NoRegionError as e:
    six.raise_from(
      Exception("No default region is selected, please run `aws configure`"),
      e,
    )
  app.extend('services', services)

class OrchestrateApp(CementApp):
  class Meta(object):
    label = 'sigopt'
    base_controller = 'base'
    argument_handler = ArgparseArgumentHandler
    handlers = [
      OrchestrateController,
      OrchestrateClusterController,
    ]
    hooks = [
      ('post_argument_parsing', load_options),
      ('post_argument_parsing', extend_app_services),
    ]

def main():
  with OrchestrateApp() as app:
    app.run()
