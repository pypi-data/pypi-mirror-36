from orchestrate.core.services.bag import ServiceBag

from orchestrate.core.aws.service import AwsService
from orchestrate.core.autoscaling.service import AwsAutoScalingService
from orchestrate.core.cloudformation.service import AwsCloudFormationService
from orchestrate.core.docker.service import DockerService
from orchestrate.core.ec2.service import AwsEc2Service
from orchestrate.core.ecr.service import AwsEcrService
from orchestrate.core.eks.service import AwsEksService
from orchestrate.core.iam.service import AwsIamService
from orchestrate.core.job_logs.service import JobLogsService
from orchestrate.core.job_runner.service import JobRunnerService
from orchestrate.core.job_status.service import JobStatusService
from orchestrate.core.kubernetes.service import KubernetesService
from orchestrate.core.model_packer.service import ModelPackerService
from orchestrate.core.options_validator.service import OptionsValidatorService
from orchestrate.core.resource.service import ResourceService
from orchestrate.core.template.service import TemplateService
from orchestrate.core.sigopt.service import SigOptService


class OrchestrateServiceBag(ServiceBag):
  def __init__(self, options):
    self._options = options
    super(OrchestrateServiceBag, self).__init__()

  @property
  def options(self):
    return self._options

  def get_option(self, name):
    parts = name.split('.')
    options = self.options

    for part in parts:
      try:
        options = options[part]
      except (KeyError, TypeError):
        return None
    return options

  def _create_services(self):
    super(OrchestrateServiceBag, self)._create_services()
    self.resource_service = ResourceService(self)
    self.aws_service = AwsService(self)
    self.autoscaling_service = AwsAutoScalingService(
      self,
      aws_access_key_id=self.get_option('aws.aws_access_key_id'),
      aws_secret_access_key=self.get_option('aws.aws_secret_access_key'),
      region_name=self.get_option('aws.region'),
    )
    self.cloudformation_service = AwsCloudFormationService(
      self,
      aws_access_key_id=self.get_option('aws.aws_access_key_id'),
      aws_secret_access_key=self.get_option('aws.aws_secret_access_key'),
      region_name=self.get_option('aws.region'),
    )
    self.docker_service = DockerService(self)
    self.ec2_service = AwsEc2Service(
      self,
      aws_access_key_id=self.get_option('aws.aws_access_key_id'),
      aws_secret_access_key=self.get_option('aws.aws_secret_access_key'),
      region_name=self.get_option('aws.region'),
    )
    self.ecr_service = AwsEcrService(
      self,
      aws_access_key_id=self.get_option('aws.aws_access_key_id'),
      aws_secret_access_key=self.get_option('aws.aws_secret_access_key'),
      region_name=self.get_option('aws.region'),
    )
    self.eks_service = AwsEksService(
      self,
      aws_access_key_id=self.get_option('aws.aws_access_key_id'),
      aws_secret_access_key=self.get_option('aws.aws_secret_access_key'),
      region_name=self.get_option('aws.region'),
    )
    self.iam_service = AwsIamService(
      self,
      aws_access_key_id=self.get_option('aws.aws_access_key_id'),
      aws_secret_access_key=self.get_option('aws.aws_secret_access_key'),
      region_name=self.get_option('aws.region'),
    )
    self.job_runner_service = JobRunnerService(self)
    self.job_logs_service = JobLogsService(self)
    self.job_status_service = JobStatusService(self)
    self.kubernetes_service = KubernetesService(self)
    self.model_packer_service = ModelPackerService(self)
    self.options_validator_service = OptionsValidatorService(self)
    self.template_service = TemplateService(self)
    self.sigopt_service = SigOptService(self, api_token=self.get_option('sigopt.api_token'))

  def _warmup_services(self):
    super(OrchestrateServiceBag, self)._warmup_services()
    self.kubernetes_service.warmup()
