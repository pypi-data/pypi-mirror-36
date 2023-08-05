import datetime
import typing
from autoboto import ShapeBase, OutputShapeBase, TypeInfo
from enum import Enum
import dataclasses


@dataclasses.dataclass
class AbortEnvironmentUpdateMessage(ShapeBase):
    """

    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "environment_id",
                "EnvironmentId",
                TypeInfo(str),
            ),
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
        ]

    # This specifies the ID of the environment with the in-progress update that
    # you want to cancel.
    environment_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # This specifies the name of the environment with the in-progress update that
    # you want to cancel.
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )


class ActionHistoryStatus(Enum):
    Completed = "Completed"
    Failed = "Failed"
    Unknown = "Unknown"


class ActionStatus(Enum):
    Scheduled = "Scheduled"
    Pending = "Pending"
    Running = "Running"
    Unknown = "Unknown"


class ActionType(Enum):
    InstanceRefresh = "InstanceRefresh"
    PlatformUpdate = "PlatformUpdate"
    Unknown = "Unknown"


@dataclasses.dataclass
class ApplicationDescription(ShapeBase):
    """
    Describes the properties of an application.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "application_arn",
                "ApplicationArn",
                TypeInfo(str),
            ),
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "description",
                "Description",
                TypeInfo(str),
            ),
            (
                "date_created",
                "DateCreated",
                TypeInfo(datetime.datetime),
            ),
            (
                "date_updated",
                "DateUpdated",
                TypeInfo(datetime.datetime),
            ),
            (
                "versions",
                "Versions",
                TypeInfo(typing.List[str]),
            ),
            (
                "configuration_templates",
                "ConfigurationTemplates",
                TypeInfo(typing.List[str]),
            ),
            (
                "resource_lifecycle_config",
                "ResourceLifecycleConfig",
                TypeInfo(ApplicationResourceLifecycleConfig),
            ),
        ]

    # The Amazon Resource Name (ARN) of the application.
    application_arn: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the application.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # User-defined description of the application.
    description: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The date when the application was created.
    date_created: datetime.datetime = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The date when the application was last modified.
    date_updated: datetime.datetime = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The names of the versions for this application.
    versions: typing.List[str] = dataclasses.field(default_factory=list, )

    # The names of the configuration templates associated with this application.
    configuration_templates: typing.List[str] = dataclasses.field(
        default_factory=list,
    )

    # The lifecycle settings for the application.
    resource_lifecycle_config: "ApplicationResourceLifecycleConfig" = dataclasses.field(
        default_factory=dict,
    )


@dataclasses.dataclass
class ApplicationDescriptionMessage(OutputShapeBase):
    """
    Result message containing a single description of an application.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "application",
                "Application",
                TypeInfo(ApplicationDescription),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The ApplicationDescription of the application.
    application: "ApplicationDescription" = dataclasses.field(
        default_factory=dict,
    )


@dataclasses.dataclass
class ApplicationDescriptionsMessage(OutputShapeBase):
    """
    Result message containing a list of application descriptions.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "applications",
                "Applications",
                TypeInfo(typing.List[ApplicationDescription]),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # This parameter contains a list of ApplicationDescription.
    applications: typing.List["ApplicationDescription"] = dataclasses.field(
        default_factory=list,
    )


@dataclasses.dataclass
class ApplicationMetrics(ShapeBase):
    """
    Application request metrics for an AWS Elastic Beanstalk environment.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "duration",
                "Duration",
                TypeInfo(int),
            ),
            (
                "request_count",
                "RequestCount",
                TypeInfo(int),
            ),
            (
                "status_codes",
                "StatusCodes",
                TypeInfo(StatusCodes),
            ),
            (
                "latency",
                "Latency",
                TypeInfo(Latency),
            ),
        ]

    # The amount of time that the metrics cover (usually 10 seconds). For
    # example, you might have 5 requests (`request_count`) within the most recent
    # time slice of 10 seconds (`duration`).
    duration: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Average number of requests handled by the web server per second over the
    # last 10 seconds.
    request_count: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Represents the percentage of requests over the last 10 seconds that
    # resulted in each type of status code response.
    status_codes: "StatusCodes" = dataclasses.field(default_factory=dict, )

    # Represents the average latency for the slowest X percent of requests over
    # the last 10 seconds. Latencies are in seconds with one millisecond
    # resolution.
    latency: "Latency" = dataclasses.field(default_factory=dict, )


@dataclasses.dataclass
class ApplicationResourceLifecycleConfig(ShapeBase):
    """
    The resource lifecycle configuration for an application. Defines lifecycle
    settings for resources that belong to the application, and the service role that
    Elastic Beanstalk assumes in order to apply lifecycle settings. The version
    lifecycle configuration defines lifecycle settings for application versions.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "service_role",
                "ServiceRole",
                TypeInfo(str),
            ),
            (
                "version_lifecycle_config",
                "VersionLifecycleConfig",
                TypeInfo(ApplicationVersionLifecycleConfig),
            ),
        ]

    # The ARN of an IAM service role that Elastic Beanstalk has permission to
    # assume.

    # The `ServiceRole` property is required the first time that you provide a
    # `VersionLifecycleConfig` for the application in one of the supporting calls
    # (`CreateApplication` or `UpdateApplicationResourceLifecycle`). After you
    # provide it once, in either one of the calls, Elastic Beanstalk persists the
    # Service Role with the application, and you don't need to specify it again
    # in subsequent `UpdateApplicationResourceLifecycle` calls. You can, however,
    # specify it in subsequent calls to change the Service Role to another value.
    service_role: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The application version lifecycle configuration.
    version_lifecycle_config: "ApplicationVersionLifecycleConfig" = dataclasses.field(
        default_factory=dict,
    )


@dataclasses.dataclass
class ApplicationResourceLifecycleDescriptionMessage(OutputShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "resource_lifecycle_config",
                "ResourceLifecycleConfig",
                TypeInfo(ApplicationResourceLifecycleConfig),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The name of the application.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The lifecycle configuration.
    resource_lifecycle_config: "ApplicationResourceLifecycleConfig" = dataclasses.field(
        default_factory=dict,
    )


@dataclasses.dataclass
class ApplicationVersionDescription(ShapeBase):
    """
    Describes the properties of an application version.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "application_version_arn",
                "ApplicationVersionArn",
                TypeInfo(str),
            ),
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "description",
                "Description",
                TypeInfo(str),
            ),
            (
                "version_label",
                "VersionLabel",
                TypeInfo(str),
            ),
            (
                "source_build_information",
                "SourceBuildInformation",
                TypeInfo(SourceBuildInformation),
            ),
            (
                "build_arn",
                "BuildArn",
                TypeInfo(str),
            ),
            (
                "source_bundle",
                "SourceBundle",
                TypeInfo(S3Location),
            ),
            (
                "date_created",
                "DateCreated",
                TypeInfo(datetime.datetime),
            ),
            (
                "date_updated",
                "DateUpdated",
                TypeInfo(datetime.datetime),
            ),
            (
                "status",
                "Status",
                TypeInfo(ApplicationVersionStatus),
            ),
        ]

    # The Amazon Resource Name (ARN) of the application version.
    application_version_arn: str = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The name of the application to which the application version belongs.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The description of the application version.
    description: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A unique identifier for the application version.
    version_label: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If the version's source code was retrieved from AWS CodeCommit, the
    # location of the source code for the application version.
    source_build_information: "SourceBuildInformation" = dataclasses.field(
        default_factory=dict,
    )

    # Reference to the artifact from the AWS CodeBuild build.
    build_arn: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The storage location of the application version's source bundle in Amazon
    # S3.
    source_bundle: "S3Location" = dataclasses.field(default_factory=dict, )

    # The creation date of the application version.
    date_created: datetime.datetime = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The last modified date of the application version.
    date_updated: datetime.datetime = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The processing status of the application version. Reflects the state of the
    # application version during its creation. Many of the values are only
    # applicable if you specified `True` for the `Process` parameter of the
    # `CreateApplicationVersion` action. The following list describes the
    # possible values.

    #   * `Unprocessed` – Application version wasn't pre-processed or validated. Elastic Beanstalk will validate configuration files during deployment of the application version to an environment.

    #   * `Processing` – Elastic Beanstalk is currently processing the application version.

    #   * `Building` – Application version is currently undergoing an AWS CodeBuild build.

    #   * `Processed` – Elastic Beanstalk was successfully pre-processed and validated.

    #   * `Failed` – Either the AWS CodeBuild build failed or configuration files didn't pass validation. This application version isn't usable.
    status: "ApplicationVersionStatus" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


@dataclasses.dataclass
class ApplicationVersionDescriptionMessage(OutputShapeBase):
    """
    Result message wrapping a single description of an application version.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "application_version",
                "ApplicationVersion",
                TypeInfo(ApplicationVersionDescription),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The ApplicationVersionDescription of the application version.
    application_version: "ApplicationVersionDescription" = dataclasses.field(
        default_factory=dict,
    )


@dataclasses.dataclass
class ApplicationVersionDescriptionsMessage(OutputShapeBase):
    """
    Result message wrapping a list of application version descriptions.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "application_versions",
                "ApplicationVersions",
                TypeInfo(typing.List[ApplicationVersionDescription]),
            ),
            (
                "next_token",
                "NextToken",
                TypeInfo(str),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # List of `ApplicationVersionDescription` objects sorted in order of
    # creation.
    application_versions: typing.List["ApplicationVersionDescription"
                                     ] = dataclasses.field(
                                         default_factory=list,
                                     )

    # In a paginated request, the token that you can pass in a subsequent request
    # to get the next response page.
    next_token: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ApplicationVersionLifecycleConfig(ShapeBase):
    """
    The application version lifecycle settings for an application. Defines the rules
    that Elastic Beanstalk applies to an application's versions in order to avoid
    hitting the per-region limit for application versions.

    When Elastic Beanstalk deletes an application version from its database, you can
    no longer deploy that version to an environment. The source bundle remains in S3
    unless you configure the rule to delete it.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "max_count_rule",
                "MaxCountRule",
                TypeInfo(MaxCountRule),
            ),
            (
                "max_age_rule",
                "MaxAgeRule",
                TypeInfo(MaxAgeRule),
            ),
        ]

    # Specify a max count rule to restrict the number of application versions
    # that are retained for an application.
    max_count_rule: "MaxCountRule" = dataclasses.field(default_factory=dict, )

    # Specify a max age rule to restrict the length of time that application
    # versions are retained for an application.
    max_age_rule: "MaxAgeRule" = dataclasses.field(default_factory=dict, )


class ApplicationVersionStatus(Enum):
    Processed = "Processed"
    Unprocessed = "Unprocessed"
    Failed = "Failed"
    Processing = "Processing"
    Building = "Building"


@dataclasses.dataclass
class ApplyEnvironmentManagedActionRequest(ShapeBase):
    """
    Request to execute a scheduled managed action immediately.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "action_id",
                "ActionId",
                TypeInfo(str),
            ),
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
            (
                "environment_id",
                "EnvironmentId",
                TypeInfo(str),
            ),
        ]

    # The action ID of the scheduled managed action to execute.
    action_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the target environment.
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The environment ID of the target environment.
    environment_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ApplyEnvironmentManagedActionResult(OutputShapeBase):
    """
    The result message containing information about the managed action.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "action_id",
                "ActionId",
                TypeInfo(str),
            ),
            (
                "action_description",
                "ActionDescription",
                TypeInfo(str),
            ),
            (
                "action_type",
                "ActionType",
                TypeInfo(ActionType),
            ),
            (
                "status",
                "Status",
                TypeInfo(str),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The action ID of the managed action.
    action_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A description of the managed action.
    action_description: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The type of managed action.
    action_type: "ActionType" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The status of the managed action.
    status: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class AutoScalingGroup(ShapeBase):
    """
    Describes an Auto Scaling launch configuration.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "name",
                "Name",
                TypeInfo(str),
            ),
        ]

    # The name of the `AutoScalingGroup` .
    name: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class BuildConfiguration(ShapeBase):
    """
    Settings for an AWS CodeBuild build.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "code_build_service_role",
                "CodeBuildServiceRole",
                TypeInfo(str),
            ),
            (
                "image",
                "Image",
                TypeInfo(str),
            ),
            (
                "artifact_name",
                "ArtifactName",
                TypeInfo(str),
            ),
            (
                "compute_type",
                "ComputeType",
                TypeInfo(ComputeType),
            ),
            (
                "timeout_in_minutes",
                "TimeoutInMinutes",
                TypeInfo(int),
            ),
        ]

    # The Amazon Resource Name (ARN) of the AWS Identity and Access Management
    # (IAM) role that enables AWS CodeBuild to interact with dependent AWS
    # services on behalf of the AWS account.
    code_build_service_role: str = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The ID of the Docker image to use for this build project.
    image: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the artifact of the CodeBuild build. If provided, Elastic
    # Beanstalk stores the build artifact in the S3 location _S3-bucket_
    # /resources/ _application-name_ /codebuild/codebuild- _version-label_ -
    # _artifact-name_.zip. If not provided, Elastic Beanstalk stores the build
    # artifact in the S3 location _S3-bucket_ /resources/ _application-name_
    # /codebuild/codebuild- _version-label_.zip.
    artifact_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Information about the compute resources the build project will use.

    #   * `BUILD_GENERAL1_SMALL: Use up to 3 GB memory and 2 vCPUs for builds`

    #   * `BUILD_GENERAL1_MEDIUM: Use up to 7 GB memory and 4 vCPUs for builds`

    #   * `BUILD_GENERAL1_LARGE: Use up to 15 GB memory and 8 vCPUs for builds`
    compute_type: "ComputeType" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # How long in minutes, from 5 to 480 (8 hours), for AWS CodeBuild to wait
    # until timing out any related build that does not get marked as completed.
    # The default is 60 minutes.
    timeout_in_minutes: int = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class Builder(ShapeBase):
    """
    The builder used to build the custom platform.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "arn",
                "ARN",
                TypeInfo(str),
            ),
        ]

    # The ARN of the builder.
    arn: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class CPUUtilization(ShapeBase):
    """
    CPU utilization metrics for an instance.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "user",
                "User",
                TypeInfo(float),
            ),
            (
                "nice",
                "Nice",
                TypeInfo(float),
            ),
            (
                "system",
                "System",
                TypeInfo(float),
            ),
            (
                "idle",
                "Idle",
                TypeInfo(float),
            ),
            (
                "io_wait",
                "IOWait",
                TypeInfo(float),
            ),
            (
                "irq",
                "IRQ",
                TypeInfo(float),
            ),
            (
                "soft_irq",
                "SoftIRQ",
                TypeInfo(float),
            ),
            (
                "privileged",
                "Privileged",
                TypeInfo(float),
            ),
        ]

    # Percentage of time that the CPU has spent in the `User` state over the last
    # 10 seconds.
    user: float = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Available on Linux environments only.

    # Percentage of time that the CPU has spent in the `Nice` state over the last
    # 10 seconds.
    nice: float = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Available on Linux environments only.

    # Percentage of time that the CPU has spent in the `System` state over the
    # last 10 seconds.
    system: float = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Percentage of time that the CPU has spent in the `Idle` state over the last
    # 10 seconds.
    idle: float = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Available on Linux environments only.

    # Percentage of time that the CPU has spent in the `I/O Wait` state over the
    # last 10 seconds.
    io_wait: float = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Available on Linux environments only.

    # Percentage of time that the CPU has spent in the `IRQ` state over the last
    # 10 seconds.
    irq: float = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Available on Linux environments only.

    # Percentage of time that the CPU has spent in the `SoftIRQ` state over the
    # last 10 seconds.
    soft_irq: float = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Available on Windows environments only.

    # Percentage of time that the CPU has spent in the `Privileged` state over
    # the last 10 seconds.
    privileged: float = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class CheckDNSAvailabilityMessage(ShapeBase):
    """
    Results message indicating whether a CNAME is available.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "cname_prefix",
                "CNAMEPrefix",
                TypeInfo(str),
            ),
        ]

    # The prefix used when this CNAME is reserved.
    cname_prefix: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class CheckDNSAvailabilityResultMessage(OutputShapeBase):
    """
    Indicates if the specified CNAME is available.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "available",
                "Available",
                TypeInfo(bool),
            ),
            (
                "fully_qualified_cname",
                "FullyQualifiedCNAME",
                TypeInfo(str),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # Indicates if the specified CNAME is available:

    #   * `true` : The CNAME is available.

    #   * `false` : The CNAME is not available.
    available: bool = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The fully qualified CNAME to reserve when CreateEnvironment is called with
    # the provided prefix.
    fully_qualified_cname: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class CodeBuildNotInServiceRegionException(ShapeBase):
    """
    AWS CodeBuild is not available in the specified region.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return []


@dataclasses.dataclass
class ComposeEnvironmentsMessage(ShapeBase):
    """
    Request to create or update a group of environments.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "group_name",
                "GroupName",
                TypeInfo(str),
            ),
            (
                "version_labels",
                "VersionLabels",
                TypeInfo(typing.List[str]),
            ),
        ]

    # The name of the application to which the specified source bundles belong.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the group to which the target environments belong. Specify a
    # group name only if the environment name defined in each target
    # environment's manifest ends with a + (plus) character. See [Environment
    # Manifest
    # (env.yaml)](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environment-
    # cfg-manifest.html) for details.
    group_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A list of version labels, specifying one or more application source bundles
    # that belong to the target application. Each source bundle must include an
    # environment manifest that specifies the name of the environment and the
    # name of the solution stack to use, and optionally can specify environment
    # links to create.
    version_labels: typing.List[str] = dataclasses.field(default_factory=list, )


class ComputeType(Enum):
    BUILD_GENERAL1_SMALL = "BUILD_GENERAL1_SMALL"
    BUILD_GENERAL1_MEDIUM = "BUILD_GENERAL1_MEDIUM"
    BUILD_GENERAL1_LARGE = "BUILD_GENERAL1_LARGE"


class ConfigurationDeploymentStatus(Enum):
    deployed = "deployed"
    pending = "pending"
    failed = "failed"


@dataclasses.dataclass
class ConfigurationOptionDescription(ShapeBase):
    """
    Describes the possible values for a configuration option.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "namespace",
                "Namespace",
                TypeInfo(str),
            ),
            (
                "name",
                "Name",
                TypeInfo(str),
            ),
            (
                "default_value",
                "DefaultValue",
                TypeInfo(str),
            ),
            (
                "change_severity",
                "ChangeSeverity",
                TypeInfo(str),
            ),
            (
                "user_defined",
                "UserDefined",
                TypeInfo(bool),
            ),
            (
                "value_type",
                "ValueType",
                TypeInfo(ConfigurationOptionValueType),
            ),
            (
                "value_options",
                "ValueOptions",
                TypeInfo(typing.List[str]),
            ),
            (
                "min_value",
                "MinValue",
                TypeInfo(int),
            ),
            (
                "max_value",
                "MaxValue",
                TypeInfo(int),
            ),
            (
                "max_length",
                "MaxLength",
                TypeInfo(int),
            ),
            (
                "regex",
                "Regex",
                TypeInfo(OptionRestrictionRegex),
            ),
        ]

    # A unique namespace identifying the option's associated AWS resource.
    namespace: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the configuration option.
    name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The default value for this configuration option.
    default_value: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # An indication of which action is required if the value for this
    # configuration option changes:

    #   * `NoInterruption` : There is no interruption to the environment or application availability.

    #   * `RestartEnvironment` : The environment is entirely restarted, all AWS resources are deleted and recreated, and the environment is unavailable during the process.

    #   * `RestartApplicationServer` : The environment is available the entire time. However, a short application outage occurs when the application servers on the running Amazon EC2 instances are restarted.
    change_severity: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # An indication of whether the user defined this configuration option:

    #   * `true` : This configuration option was defined by the user. It is a valid choice for specifying if this as an `Option to Remove` when updating configuration settings.

    #   * `false` : This configuration was not defined by the user.

    # Constraint: You can remove only `UserDefined` options from a configuration.

    # Valid Values: `true` | `false`
    user_defined: bool = dataclasses.field(default=ShapeBase.NOT_SET, )

    # An indication of which type of values this option has and whether it is
    # allowable to select one or more than one of the possible values:

    #   * `Scalar` : Values for this option are a single selection from the possible values, or an unformatted string, or numeric value governed by the `MIN/MAX/Regex` constraints.

    #   * `List` : Values for this option are multiple selections from the possible values.

    #   * `Boolean` : Values for this option are either `true` or `false` .

    #   * `Json` : Values for this option are a JSON representation of a `ConfigDocument`.
    value_type: "ConfigurationOptionValueType" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # If specified, values for the configuration option are selected from this
    # list.
    value_options: typing.List[str] = dataclasses.field(default_factory=list, )

    # If specified, the configuration option must be a numeric value greater than
    # this value.
    min_value: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If specified, the configuration option must be a numeric value less than
    # this value.
    max_value: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If specified, the configuration option must be a string value no longer
    # than this value.
    max_length: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If specified, the configuration option must be a string value that
    # satisfies this regular expression.
    regex: "OptionRestrictionRegex" = dataclasses.field(default_factory=dict, )


@dataclasses.dataclass
class ConfigurationOptionSetting(ShapeBase):
    """
    A specification identifying an individual configuration option along with its
    current value. For a list of possible option values, go to [Option
    Values](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-
    options.html) in the _AWS Elastic Beanstalk Developer Guide_.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "resource_name",
                "ResourceName",
                TypeInfo(str),
            ),
            (
                "namespace",
                "Namespace",
                TypeInfo(str),
            ),
            (
                "option_name",
                "OptionName",
                TypeInfo(str),
            ),
            (
                "value",
                "Value",
                TypeInfo(str),
            ),
        ]

    # A unique resource name for a time-based scaling configuration option.
    resource_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A unique namespace identifying the option's associated AWS resource.
    namespace: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the configuration option.
    option_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The current value for the configuration option.
    value: str = dataclasses.field(default=ShapeBase.NOT_SET, )


class ConfigurationOptionValueType(Enum):
    Scalar = "Scalar"
    List = "List"


@dataclasses.dataclass
class ConfigurationOptionsDescription(OutputShapeBase):
    """
    Describes the settings for a specified configuration set.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "solution_stack_name",
                "SolutionStackName",
                TypeInfo(str),
            ),
            (
                "platform_arn",
                "PlatformArn",
                TypeInfo(str),
            ),
            (
                "options",
                "Options",
                TypeInfo(typing.List[ConfigurationOptionDescription]),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The name of the solution stack these configuration options belong to.
    solution_stack_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The ARN of the platform.
    platform_arn: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A list of ConfigurationOptionDescription.
    options: typing.List["ConfigurationOptionDescription"] = dataclasses.field(
        default_factory=list,
    )


@dataclasses.dataclass
class ConfigurationSettingsDescription(OutputShapeBase):
    """
    Describes the settings for a configuration set.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "solution_stack_name",
                "SolutionStackName",
                TypeInfo(str),
            ),
            (
                "platform_arn",
                "PlatformArn",
                TypeInfo(str),
            ),
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "template_name",
                "TemplateName",
                TypeInfo(str),
            ),
            (
                "description",
                "Description",
                TypeInfo(str),
            ),
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
            (
                "deployment_status",
                "DeploymentStatus",
                TypeInfo(ConfigurationDeploymentStatus),
            ),
            (
                "date_created",
                "DateCreated",
                TypeInfo(datetime.datetime),
            ),
            (
                "date_updated",
                "DateUpdated",
                TypeInfo(datetime.datetime),
            ),
            (
                "option_settings",
                "OptionSettings",
                TypeInfo(typing.List[ConfigurationOptionSetting]),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The name of the solution stack this configuration set uses.
    solution_stack_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The ARN of the platform.
    platform_arn: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the application associated with this configuration set.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If not `null`, the name of the configuration template for this
    # configuration set.
    template_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Describes this configuration set.
    description: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If not `null`, the name of the environment for this configuration set.
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If this configuration set is associated with an environment, the
    # `DeploymentStatus` parameter indicates the deployment status of this
    # configuration set:

    #   * `null`: This configuration is not associated with a running environment.

    #   * `pending`: This is a draft configuration that is not deployed to the associated environment but is in the process of deploying.

    #   * `deployed`: This is the configuration that is currently deployed to the associated running environment.

    #   * `failed`: This is a draft configuration that failed to successfully deploy.
    deployment_status: "ConfigurationDeploymentStatus" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The date (in UTC time) when this configuration set was created.
    date_created: datetime.datetime = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The date (in UTC time) when this configuration set was last modified.
    date_updated: datetime.datetime = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A list of the configuration options and their values in this configuration
    # set.
    option_settings: typing.List["ConfigurationOptionSetting"
                                ] = dataclasses.field(
                                    default_factory=list,
                                )


@dataclasses.dataclass
class ConfigurationSettingsDescriptions(OutputShapeBase):
    """
    The results from a request to change the configuration settings of an
    environment.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "configuration_settings",
                "ConfigurationSettings",
                TypeInfo(typing.List[ConfigurationSettingsDescription]),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A list of ConfigurationSettingsDescription.
    configuration_settings: typing.List["ConfigurationSettingsDescription"
                                       ] = dataclasses.field(
                                           default_factory=list,
                                       )


@dataclasses.dataclass
class ConfigurationSettingsValidationMessages(OutputShapeBase):
    """
    Provides a list of validation messages.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "messages",
                "Messages",
                TypeInfo(typing.List[ValidationMessage]),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A list of ValidationMessage.
    messages: typing.List["ValidationMessage"] = dataclasses.field(
        default_factory=list,
    )


@dataclasses.dataclass
class CreateApplicationMessage(ShapeBase):
    """
    Request to create an application.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "description",
                "Description",
                TypeInfo(str),
            ),
            (
                "resource_lifecycle_config",
                "ResourceLifecycleConfig",
                TypeInfo(ApplicationResourceLifecycleConfig),
            ),
        ]

    # The name of the application.

    # Constraint: This name must be unique within your account. If the specified
    # name already exists, the action returns an `InvalidParameterValue` error.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Describes the application.
    description: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Specify an application resource lifecycle configuration to prevent your
    # application from accumulating too many versions.
    resource_lifecycle_config: "ApplicationResourceLifecycleConfig" = dataclasses.field(
        default_factory=dict,
    )


@dataclasses.dataclass
class CreateApplicationVersionMessage(ShapeBase):
    """

    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "version_label",
                "VersionLabel",
                TypeInfo(str),
            ),
            (
                "description",
                "Description",
                TypeInfo(str),
            ),
            (
                "source_build_information",
                "SourceBuildInformation",
                TypeInfo(SourceBuildInformation),
            ),
            (
                "source_bundle",
                "SourceBundle",
                TypeInfo(S3Location),
            ),
            (
                "build_configuration",
                "BuildConfiguration",
                TypeInfo(BuildConfiguration),
            ),
            (
                "auto_create_application",
                "AutoCreateApplication",
                TypeInfo(bool),
            ),
            (
                "process",
                "Process",
                TypeInfo(bool),
            ),
        ]

    # The name of the application. If no application is found with this name, and
    # `AutoCreateApplication` is `false`, returns an `InvalidParameterValue`
    # error.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A label identifying this version.

    # Constraint: Must be unique per application. If an application version
    # already exists with this label for the specified application, AWS Elastic
    # Beanstalk returns an `InvalidParameterValue` error.
    version_label: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Describes this version.
    description: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Specify a commit in an AWS CodeCommit Git repository to use as the source
    # code for the application version.
    source_build_information: "SourceBuildInformation" = dataclasses.field(
        default_factory=dict,
    )

    # The Amazon S3 bucket and key that identify the location of the source
    # bundle for this version.

    # The Amazon S3 bucket must be in the same region as the environment.

    # Specify a source bundle in S3 or a commit in an AWS CodeCommit repository
    # (with `SourceBuildInformation`), but not both. If neither `SourceBundle`
    # nor `SourceBuildInformation` are provided, Elastic Beanstalk uses a sample
    # application.
    source_bundle: "S3Location" = dataclasses.field(default_factory=dict, )

    # Settings for an AWS CodeBuild build.
    build_configuration: "BuildConfiguration" = dataclasses.field(
        default_factory=dict,
    )

    # Set to `true` to create an application with the specified name if it
    # doesn't already exist.
    auto_create_application: bool = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # Pre-processes and validates the environment manifest (`env.yaml`) and
    # configuration files (`*.config` files in the `.ebextensions` folder) in the
    # source bundle. Validating configuration files can identify issues prior to
    # deploying the application version to an environment.

    # You must turn processing on for application versions that you create using
    # AWS CodeBuild or AWS CodeCommit. For application versions built from a
    # source bundle in Amazon S3, processing is optional.

    # The `Process` option validates Elastic Beanstalk configuration files. It
    # doesn't validate your application's configuration files, like proxy server
    # or Docker configuration.
    process: bool = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class CreateConfigurationTemplateMessage(ShapeBase):
    """
    Request to create a configuration template.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "template_name",
                "TemplateName",
                TypeInfo(str),
            ),
            (
                "solution_stack_name",
                "SolutionStackName",
                TypeInfo(str),
            ),
            (
                "platform_arn",
                "PlatformArn",
                TypeInfo(str),
            ),
            (
                "source_configuration",
                "SourceConfiguration",
                TypeInfo(SourceConfiguration),
            ),
            (
                "environment_id",
                "EnvironmentId",
                TypeInfo(str),
            ),
            (
                "description",
                "Description",
                TypeInfo(str),
            ),
            (
                "option_settings",
                "OptionSettings",
                TypeInfo(typing.List[ConfigurationOptionSetting]),
            ),
        ]

    # The name of the application to associate with this configuration template.
    # If no application is found with this name, AWS Elastic Beanstalk returns an
    # `InvalidParameterValue` error.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the configuration template.

    # Constraint: This name must be unique per application.

    # Default: If a configuration template already exists with this name, AWS
    # Elastic Beanstalk returns an `InvalidParameterValue` error.
    template_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the solution stack used by this configuration. The solution
    # stack specifies the operating system, architecture, and application server
    # for a configuration template. It determines the set of configuration
    # options as well as the possible and default values.

    # Use ListAvailableSolutionStacks to obtain a list of available solution
    # stacks.

    # A solution stack name or a source configuration parameter must be
    # specified, otherwise AWS Elastic Beanstalk returns an
    # `InvalidParameterValue` error.

    # If a solution stack name is not specified and the source configuration
    # parameter is specified, AWS Elastic Beanstalk uses the same solution stack
    # as the source configuration template.
    solution_stack_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The ARN of the custom platform.
    platform_arn: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If specified, AWS Elastic Beanstalk uses the configuration values from the
    # specified configuration template to create a new configuration.

    # Values specified in the `OptionSettings` parameter of this call overrides
    # any values obtained from the `SourceConfiguration`.

    # If no configuration template is found, returns an `InvalidParameterValue`
    # error.

    # Constraint: If both the solution stack name parameter and the source
    # configuration parameters are specified, the solution stack of the source
    # configuration template must match the specified solution stack name or else
    # AWS Elastic Beanstalk returns an `InvalidParameterCombination` error.
    source_configuration: "SourceConfiguration" = dataclasses.field(
        default_factory=dict,
    )

    # The ID of the environment used with this configuration template.
    environment_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Describes this configuration.
    description: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If specified, AWS Elastic Beanstalk sets the specified configuration option
    # to the requested value. The new value overrides the value obtained from the
    # solution stack or the source configuration template.
    option_settings: typing.List["ConfigurationOptionSetting"
                                ] = dataclasses.field(
                                    default_factory=list,
                                )


@dataclasses.dataclass
class CreateEnvironmentMessage(ShapeBase):
    """

    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
            (
                "group_name",
                "GroupName",
                TypeInfo(str),
            ),
            (
                "description",
                "Description",
                TypeInfo(str),
            ),
            (
                "cname_prefix",
                "CNAMEPrefix",
                TypeInfo(str),
            ),
            (
                "tier",
                "Tier",
                TypeInfo(EnvironmentTier),
            ),
            (
                "tags",
                "Tags",
                TypeInfo(typing.List[Tag]),
            ),
            (
                "version_label",
                "VersionLabel",
                TypeInfo(str),
            ),
            (
                "template_name",
                "TemplateName",
                TypeInfo(str),
            ),
            (
                "solution_stack_name",
                "SolutionStackName",
                TypeInfo(str),
            ),
            (
                "platform_arn",
                "PlatformArn",
                TypeInfo(str),
            ),
            (
                "option_settings",
                "OptionSettings",
                TypeInfo(typing.List[ConfigurationOptionSetting]),
            ),
            (
                "options_to_remove",
                "OptionsToRemove",
                TypeInfo(typing.List[OptionSpecification]),
            ),
        ]

    # The name of the application that contains the version to be deployed.

    # If no application is found with this name, `CreateEnvironment` returns an
    # `InvalidParameterValue` error.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A unique name for the deployment environment. Used in the application URL.

    # Constraint: Must be from 4 to 40 characters in length. The name can contain
    # only letters, numbers, and hyphens. It cannot start or end with a hyphen.
    # This name must be unique within a region in your account. If the specified
    # name already exists in the region, AWS Elastic Beanstalk returns an
    # `InvalidParameterValue` error.

    # Default: If the CNAME parameter is not specified, the environment name
    # becomes part of the CNAME, and therefore part of the visible URL for your
    # application.
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the group to which the target environment belongs. Specify a
    # group name only if the environment's name is specified in an environment
    # manifest and not with the environment name parameter. See [Environment
    # Manifest
    # (env.yaml)](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environment-
    # cfg-manifest.html) for details.
    group_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Describes this environment.
    description: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If specified, the environment attempts to use this value as the prefix for
    # the CNAME. If not specified, the CNAME is generated automatically by
    # appending a random alphanumeric string to the environment name.
    cname_prefix: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # This specifies the tier to use for creating this environment.
    tier: "EnvironmentTier" = dataclasses.field(default_factory=dict, )

    # This specifies the tags applied to resources in the environment.
    tags: typing.List["Tag"] = dataclasses.field(default_factory=list, )

    # The name of the application version to deploy.

    # If the specified application has no associated application versions, AWS
    # Elastic Beanstalk `UpdateEnvironment` returns an `InvalidParameterValue`
    # error.

    # Default: If not specified, AWS Elastic Beanstalk attempts to launch the
    # sample application in the container.
    version_label: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the configuration template to use in deployment. If no
    # configuration template is found with this name, AWS Elastic Beanstalk
    # returns an `InvalidParameterValue` error.
    template_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # This is an alternative to specifying a template name. If specified, AWS
    # Elastic Beanstalk sets the configuration values to the default values
    # associated with the specified solution stack.

    # For a list of current solution stacks, see [Elastic Beanstalk Supported
    # Platforms](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.platforms.html).
    solution_stack_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The ARN of the platform.
    platform_arn: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If specified, AWS Elastic Beanstalk sets the specified configuration
    # options to the requested value in the configuration set for the new
    # environment. These override the values obtained from the solution stack or
    # the configuration template.
    option_settings: typing.List["ConfigurationOptionSetting"
                                ] = dataclasses.field(
                                    default_factory=list,
                                )

    # A list of custom user-defined configuration options to remove from the
    # configuration set for this new environment.
    options_to_remove: typing.List["OptionSpecification"] = dataclasses.field(
        default_factory=list,
    )


@dataclasses.dataclass
class CreatePlatformVersionRequest(ShapeBase):
    """
    Request to create a new platform version.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "platform_name",
                "PlatformName",
                TypeInfo(str),
            ),
            (
                "platform_version",
                "PlatformVersion",
                TypeInfo(str),
            ),
            (
                "platform_definition_bundle",
                "PlatformDefinitionBundle",
                TypeInfo(S3Location),
            ),
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
            (
                "option_settings",
                "OptionSettings",
                TypeInfo(typing.List[ConfigurationOptionSetting]),
            ),
        ]

    # The name of your custom platform.
    platform_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The number, such as 1.0.2, for the new platform version.
    platform_version: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The location of the platform definition archive in Amazon S3.
    platform_definition_bundle: "S3Location" = dataclasses.field(
        default_factory=dict,
    )

    # The name of the builder environment.
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The configuration option settings to apply to the builder environment.
    option_settings: typing.List["ConfigurationOptionSetting"
                                ] = dataclasses.field(
                                    default_factory=list,
                                )


@dataclasses.dataclass
class CreatePlatformVersionResult(OutputShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "platform_summary",
                "PlatformSummary",
                TypeInfo(PlatformSummary),
            ),
            (
                "builder",
                "Builder",
                TypeInfo(Builder),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # Detailed information about the new version of the custom platform.
    platform_summary: "PlatformSummary" = dataclasses.field(
        default_factory=dict,
    )

    # The builder used to create the custom platform.
    builder: "Builder" = dataclasses.field(default_factory=dict, )


@dataclasses.dataclass
class CreateStorageLocationResultMessage(OutputShapeBase):
    """
    Results of a CreateStorageLocationResult call.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "s3_bucket",
                "S3Bucket",
                TypeInfo(str),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The name of the Amazon S3 bucket created.
    s3_bucket: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class CustomAmi(ShapeBase):
    """
    A custom AMI available to platforms.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "virtualization_type",
                "VirtualizationType",
                TypeInfo(str),
            ),
            (
                "image_id",
                "ImageId",
                TypeInfo(str),
            ),
        ]

    # The type of virtualization used to create the custom AMI.
    virtualization_type: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # THe ID of the image used to create the custom AMI.
    image_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DeleteApplicationMessage(ShapeBase):
    """
    Request to delete an application.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "terminate_env_by_force",
                "TerminateEnvByForce",
                TypeInfo(bool),
            ),
        ]

    # The name of the application to delete.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # When set to true, running environments will be terminated before deleting
    # the application.
    terminate_env_by_force: bool = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


@dataclasses.dataclass
class DeleteApplicationVersionMessage(ShapeBase):
    """
    Request to delete an application version.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "version_label",
                "VersionLabel",
                TypeInfo(str),
            ),
            (
                "delete_source_bundle",
                "DeleteSourceBundle",
                TypeInfo(bool),
            ),
        ]

    # The name of the application to which the version belongs.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The label of the version to delete.
    version_label: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Set to `true` to delete the source bundle from your storage bucket.
    # Otherwise, the application version is deleted only from Elastic Beanstalk
    # and the source bundle remains in Amazon S3.
    delete_source_bundle: bool = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DeleteConfigurationTemplateMessage(ShapeBase):
    """
    Request to delete a configuration template.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "template_name",
                "TemplateName",
                TypeInfo(str),
            ),
        ]

    # The name of the application to delete the configuration template from.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the configuration template to delete.
    template_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DeleteEnvironmentConfigurationMessage(ShapeBase):
    """
    Request to delete a draft environment configuration.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
        ]

    # The name of the application the environment is associated with.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the environment to delete the draft configuration from.
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DeletePlatformVersionRequest(ShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "platform_arn",
                "PlatformArn",
                TypeInfo(str),
            ),
        ]

    # The ARN of the version of the custom platform.
    platform_arn: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DeletePlatformVersionResult(OutputShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "platform_summary",
                "PlatformSummary",
                TypeInfo(PlatformSummary),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # Detailed information about the version of the custom platform.
    platform_summary: "PlatformSummary" = dataclasses.field(
        default_factory=dict,
    )


@dataclasses.dataclass
class Deployment(ShapeBase):
    """
    Information about an application version deployment.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "version_label",
                "VersionLabel",
                TypeInfo(str),
            ),
            (
                "deployment_id",
                "DeploymentId",
                TypeInfo(int),
            ),
            (
                "status",
                "Status",
                TypeInfo(str),
            ),
            (
                "deployment_time",
                "DeploymentTime",
                TypeInfo(datetime.datetime),
            ),
        ]

    # The version label of the application version in the deployment.
    version_label: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The ID of the deployment. This number increases by one each time that you
    # deploy source code or change instance configuration settings.
    deployment_id: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The status of the deployment:

    #   * `In Progress` : The deployment is in progress.

    #   * `Deployed` : The deployment succeeded.

    #   * `Failed` : The deployment failed.
    status: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # For in-progress deployments, the time that the deployment started.

    # For completed deployments, the time that the deployment ended.
    deployment_time: datetime.datetime = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


@dataclasses.dataclass
class DescribeAccountAttributesResult(OutputShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "resource_quotas",
                "ResourceQuotas",
                TypeInfo(ResourceQuotas),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The Elastic Beanstalk resource quotas associated with the calling AWS
    # account.
    resource_quotas: "ResourceQuotas" = dataclasses.field(
        default_factory=dict,
    )


@dataclasses.dataclass
class DescribeApplicationVersionsMessage(ShapeBase):
    """
    Request to describe application versions.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "version_labels",
                "VersionLabels",
                TypeInfo(typing.List[str]),
            ),
            (
                "max_records",
                "MaxRecords",
                TypeInfo(int),
            ),
            (
                "next_token",
                "NextToken",
                TypeInfo(str),
            ),
        ]

    # Specify an application name to show only application versions for that
    # application.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Specify a version label to show a specific application version.
    version_labels: typing.List[str] = dataclasses.field(default_factory=list, )

    # For a paginated request. Specify a maximum number of application versions
    # to include in each response.

    # If no `MaxRecords` is specified, all available application versions are
    # retrieved in a single response.
    max_records: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # For a paginated request. Specify a token from a previous response page to
    # retrieve the next response page. All other parameter values must be
    # identical to the ones specified in the initial request.

    # If no `NextToken` is specified, the first page is retrieved.
    next_token: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DescribeApplicationsMessage(ShapeBase):
    """
    Request to describe one or more applications.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "application_names",
                "ApplicationNames",
                TypeInfo(typing.List[str]),
            ),
        ]

    # If specified, AWS Elastic Beanstalk restricts the returned descriptions to
    # only include those with the specified names.
    application_names: typing.List[str] = dataclasses.field(
        default_factory=list,
    )


@dataclasses.dataclass
class DescribeConfigurationOptionsMessage(ShapeBase):
    """
    Result message containing a list of application version descriptions.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "template_name",
                "TemplateName",
                TypeInfo(str),
            ),
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
            (
                "solution_stack_name",
                "SolutionStackName",
                TypeInfo(str),
            ),
            (
                "platform_arn",
                "PlatformArn",
                TypeInfo(str),
            ),
            (
                "options",
                "Options",
                TypeInfo(typing.List[OptionSpecification]),
            ),
        ]

    # The name of the application associated with the configuration template or
    # environment. Only needed if you want to describe the configuration options
    # associated with either the configuration template or environment.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the configuration template whose configuration options you want
    # to describe.
    template_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the environment whose configuration options you want to
    # describe.
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the solution stack whose configuration options you want to
    # describe.
    solution_stack_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The ARN of the custom platform.
    platform_arn: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If specified, restricts the descriptions to only the specified options.
    options: typing.List["OptionSpecification"] = dataclasses.field(
        default_factory=list,
    )


@dataclasses.dataclass
class DescribeConfigurationSettingsMessage(ShapeBase):
    """
    Result message containing all of the configuration settings for a specified
    solution stack or configuration template.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "template_name",
                "TemplateName",
                TypeInfo(str),
            ),
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
        ]

    # The application for the environment or configuration template.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the configuration template to describe.

    # Conditional: You must specify either this parameter or an EnvironmentName,
    # but not both. If you specify both, AWS Elastic Beanstalk returns an
    # `InvalidParameterCombination` error. If you do not specify either, AWS
    # Elastic Beanstalk returns a `MissingRequiredParameter` error.
    template_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the environment to describe.

    # Condition: You must specify either this or a TemplateName, but not both. If
    # you specify both, AWS Elastic Beanstalk returns an
    # `InvalidParameterCombination` error. If you do not specify either, AWS
    # Elastic Beanstalk returns `MissingRequiredParameter` error.
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DescribeEnvironmentHealthRequest(ShapeBase):
    """
    See the example below to learn how to create a request body.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
            (
                "environment_id",
                "EnvironmentId",
                TypeInfo(str),
            ),
            (
                "attribute_names",
                "AttributeNames",
                TypeInfo(typing.List[EnvironmentHealthAttribute]),
            ),
        ]

    # Specify the environment by name.

    # You must specify either this or an EnvironmentName, or both.
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Specify the environment by ID.

    # You must specify either this or an EnvironmentName, or both.
    environment_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Specify the response elements to return. To retrieve all attributes, set to
    # `All`. If no attribute names are specified, returns the name of the
    # environment.
    attribute_names: typing.List["EnvironmentHealthAttribute"
                                ] = dataclasses.field(
                                    default_factory=list,
                                )


@dataclasses.dataclass
class DescribeEnvironmentHealthResult(OutputShapeBase):
    """
    Health details for an AWS Elastic Beanstalk environment.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
            (
                "health_status",
                "HealthStatus",
                TypeInfo(str),
            ),
            (
                "status",
                "Status",
                TypeInfo(EnvironmentHealth),
            ),
            (
                "color",
                "Color",
                TypeInfo(str),
            ),
            (
                "causes",
                "Causes",
                TypeInfo(typing.List[str]),
            ),
            (
                "application_metrics",
                "ApplicationMetrics",
                TypeInfo(ApplicationMetrics),
            ),
            (
                "instances_health",
                "InstancesHealth",
                TypeInfo(InstanceHealthSummary),
            ),
            (
                "refreshed_at",
                "RefreshedAt",
                TypeInfo(datetime.datetime),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The environment's name.
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The [health
    # status](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/health-
    # enhanced-status.html) of the environment. For example, `Ok`.
    health_status: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The environment's operational status. `Ready`, `Launching`, `Updating`,
    # `Terminating`, or `Terminated`.
    status: "EnvironmentHealth" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The [health
    # color](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/health-
    # enhanced-status.html) of the environment.
    color: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Descriptions of the data that contributed to the environment's current
    # health status.
    causes: typing.List[str] = dataclasses.field(default_factory=list, )

    # Application request metrics for the environment.
    application_metrics: "ApplicationMetrics" = dataclasses.field(
        default_factory=dict,
    )

    # Summary health information for the instances in the environment.
    instances_health: "InstanceHealthSummary" = dataclasses.field(
        default_factory=dict,
    )

    # The date and time that the health information was retrieved.
    refreshed_at: datetime.datetime = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


@dataclasses.dataclass
class DescribeEnvironmentManagedActionHistoryRequest(ShapeBase):
    """
    Request to list completed and failed managed actions.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "environment_id",
                "EnvironmentId",
                TypeInfo(str),
            ),
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
            (
                "next_token",
                "NextToken",
                TypeInfo(str),
            ),
            (
                "max_items",
                "MaxItems",
                TypeInfo(int),
            ),
        ]

    # The environment ID of the target environment.
    environment_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the target environment.
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The pagination token returned by a previous request.
    next_token: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The maximum number of items to return for a single request.
    max_items: int = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DescribeEnvironmentManagedActionHistoryResult(OutputShapeBase):
    """
    A result message containing a list of completed and failed managed actions.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "managed_action_history_items",
                "ManagedActionHistoryItems",
                TypeInfo(typing.List[ManagedActionHistoryItem]),
            ),
            (
                "next_token",
                "NextToken",
                TypeInfo(str),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A list of completed and failed managed actions.
    managed_action_history_items: typing.List["ManagedActionHistoryItem"
                                             ] = dataclasses.field(
                                                 default_factory=list,
                                             )

    # A pagination token that you pass to DescribeEnvironmentManagedActionHistory
    # to get the next page of results.
    next_token: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DescribeEnvironmentManagedActionsRequest(ShapeBase):
    """
    Request to list an environment's upcoming and in-progress managed actions.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
            (
                "environment_id",
                "EnvironmentId",
                TypeInfo(str),
            ),
            (
                "status",
                "Status",
                TypeInfo(ActionStatus),
            ),
        ]

    # The name of the target environment.
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The environment ID of the target environment.
    environment_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # To show only actions with a particular status, specify a status.
    status: "ActionStatus" = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DescribeEnvironmentManagedActionsResult(OutputShapeBase):
    """
    The result message containing a list of managed actions.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "managed_actions",
                "ManagedActions",
                TypeInfo(typing.List[ManagedAction]),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A list of upcoming and in-progress managed actions.
    managed_actions: typing.List["ManagedAction"] = dataclasses.field(
        default_factory=list,
    )


@dataclasses.dataclass
class DescribeEnvironmentResourcesMessage(ShapeBase):
    """
    Request to describe the resources in an environment.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "environment_id",
                "EnvironmentId",
                TypeInfo(str),
            ),
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
        ]

    # The ID of the environment to retrieve AWS resource usage data.

    # Condition: You must specify either this or an EnvironmentName, or both. If
    # you do not specify either, AWS Elastic Beanstalk returns
    # `MissingRequiredParameter` error.
    environment_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the environment to retrieve AWS resource usage data.

    # Condition: You must specify either this or an EnvironmentId, or both. If
    # you do not specify either, AWS Elastic Beanstalk returns
    # `MissingRequiredParameter` error.
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DescribeEnvironmentsMessage(ShapeBase):
    """
    Request to describe one or more environments.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "version_label",
                "VersionLabel",
                TypeInfo(str),
            ),
            (
                "environment_ids",
                "EnvironmentIds",
                TypeInfo(typing.List[str]),
            ),
            (
                "environment_names",
                "EnvironmentNames",
                TypeInfo(typing.List[str]),
            ),
            (
                "include_deleted",
                "IncludeDeleted",
                TypeInfo(bool),
            ),
            (
                "included_deleted_back_to",
                "IncludedDeletedBackTo",
                TypeInfo(datetime.datetime),
            ),
            (
                "max_records",
                "MaxRecords",
                TypeInfo(int),
            ),
            (
                "next_token",
                "NextToken",
                TypeInfo(str),
            ),
        ]

    # If specified, AWS Elastic Beanstalk restricts the returned descriptions to
    # include only those that are associated with this application.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If specified, AWS Elastic Beanstalk restricts the returned descriptions to
    # include only those that are associated with this application version.
    version_label: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If specified, AWS Elastic Beanstalk restricts the returned descriptions to
    # include only those that have the specified IDs.
    environment_ids: typing.List[str] = dataclasses.field(
        default_factory=list,
    )

    # If specified, AWS Elastic Beanstalk restricts the returned descriptions to
    # include only those that have the specified names.
    environment_names: typing.List[str] = dataclasses.field(
        default_factory=list,
    )

    # Indicates whether to include deleted environments:

    # `true`: Environments that have been deleted after `IncludedDeletedBackTo`
    # are displayed.

    # `false`: Do not include deleted environments.
    include_deleted: bool = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If specified when `IncludeDeleted` is set to `true`, then environments
    # deleted after this date are displayed.
    included_deleted_back_to: datetime.datetime = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # For a paginated request. Specify a maximum number of environments to
    # include in each response.

    # If no `MaxRecords` is specified, all available environments are retrieved
    # in a single response.
    max_records: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # For a paginated request. Specify a token from a previous response page to
    # retrieve the next response page. All other parameter values must be
    # identical to the ones specified in the initial request.

    # If no `NextToken` is specified, the first page is retrieved.
    next_token: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DescribeEventsMessage(ShapeBase):
    """
    Request to retrieve a list of events for an environment.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "version_label",
                "VersionLabel",
                TypeInfo(str),
            ),
            (
                "template_name",
                "TemplateName",
                TypeInfo(str),
            ),
            (
                "environment_id",
                "EnvironmentId",
                TypeInfo(str),
            ),
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
            (
                "platform_arn",
                "PlatformArn",
                TypeInfo(str),
            ),
            (
                "request_id",
                "RequestId",
                TypeInfo(str),
            ),
            (
                "severity",
                "Severity",
                TypeInfo(EventSeverity),
            ),
            (
                "start_time",
                "StartTime",
                TypeInfo(datetime.datetime),
            ),
            (
                "end_time",
                "EndTime",
                TypeInfo(datetime.datetime),
            ),
            (
                "max_records",
                "MaxRecords",
                TypeInfo(int),
            ),
            (
                "next_token",
                "NextToken",
                TypeInfo(str),
            ),
        ]

    # If specified, AWS Elastic Beanstalk restricts the returned descriptions to
    # include only those associated with this application.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If specified, AWS Elastic Beanstalk restricts the returned descriptions to
    # those associated with this application version.
    version_label: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If specified, AWS Elastic Beanstalk restricts the returned descriptions to
    # those that are associated with this environment configuration.
    template_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If specified, AWS Elastic Beanstalk restricts the returned descriptions to
    # those associated with this environment.
    environment_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If specified, AWS Elastic Beanstalk restricts the returned descriptions to
    # those associated with this environment.
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The ARN of the version of the custom platform.
    platform_arn: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If specified, AWS Elastic Beanstalk restricts the described events to
    # include only those associated with this request ID.
    request_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If specified, limits the events returned from this call to include only
    # those with the specified severity or higher.
    severity: "EventSeverity" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If specified, AWS Elastic Beanstalk restricts the returned descriptions to
    # those that occur on or after this time.
    start_time: datetime.datetime = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # If specified, AWS Elastic Beanstalk restricts the returned descriptions to
    # those that occur up to, but not including, the `EndTime`.
    end_time: datetime.datetime = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Specifies the maximum number of events that can be returned, beginning with
    # the most recent event.
    max_records: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Pagination token. If specified, the events return the next batch of
    # results.
    next_token: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DescribeInstancesHealthRequest(ShapeBase):
    """
    Parameters for a call to `DescribeInstancesHealth`.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
            (
                "environment_id",
                "EnvironmentId",
                TypeInfo(str),
            ),
            (
                "attribute_names",
                "AttributeNames",
                TypeInfo(typing.List[InstancesHealthAttribute]),
            ),
            (
                "next_token",
                "NextToken",
                TypeInfo(str),
            ),
        ]

    # Specify the AWS Elastic Beanstalk environment by name.
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Specify the AWS Elastic Beanstalk environment by ID.
    environment_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Specifies the response elements you wish to receive. To retrieve all
    # attributes, set to `All`. If no attribute names are specified, returns a
    # list of instances.
    attribute_names: typing.List["InstancesHealthAttribute"
                                ] = dataclasses.field(
                                    default_factory=list,
                                )

    # Specify the pagination token returned by a previous call.
    next_token: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DescribeInstancesHealthResult(OutputShapeBase):
    """
    Detailed health information about the Amazon EC2 instances in an AWS Elastic
    Beanstalk environment.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "instance_health_list",
                "InstanceHealthList",
                TypeInfo(typing.List[SingleInstanceHealth]),
            ),
            (
                "refreshed_at",
                "RefreshedAt",
                TypeInfo(datetime.datetime),
            ),
            (
                "next_token",
                "NextToken",
                TypeInfo(str),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # Detailed health information about each instance.

    # The output differs slightly between Linux and Windows environments. There
    # is a difference in the members that are supported under the
    # `<CPUUtilization>` type.
    instance_health_list: typing.List["SingleInstanceHealth"
                                     ] = dataclasses.field(
                                         default_factory=list,
                                     )

    # The date and time that the health information was retrieved.
    refreshed_at: datetime.datetime = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # Pagination token for the next page of results, if available.
    next_token: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DescribePlatformVersionRequest(ShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "platform_arn",
                "PlatformArn",
                TypeInfo(str),
            ),
        ]

    # The ARN of the version of the platform.
    platform_arn: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DescribePlatformVersionResult(OutputShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "platform_description",
                "PlatformDescription",
                TypeInfo(PlatformDescription),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # Detailed information about the version of the platform.
    platform_description: "PlatformDescription" = dataclasses.field(
        default_factory=dict,
    )


@dataclasses.dataclass
class ElasticBeanstalkServiceException(ShapeBase):
    """
    A generic service exception has occurred.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "message",
                "message",
                TypeInfo(str),
            ),
        ]

    # The exception error message.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class EnvironmentDescription(OutputShapeBase):
    """
    Describes the properties of an environment.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
            (
                "environment_id",
                "EnvironmentId",
                TypeInfo(str),
            ),
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "version_label",
                "VersionLabel",
                TypeInfo(str),
            ),
            (
                "solution_stack_name",
                "SolutionStackName",
                TypeInfo(str),
            ),
            (
                "platform_arn",
                "PlatformArn",
                TypeInfo(str),
            ),
            (
                "template_name",
                "TemplateName",
                TypeInfo(str),
            ),
            (
                "description",
                "Description",
                TypeInfo(str),
            ),
            (
                "endpoint_url",
                "EndpointURL",
                TypeInfo(str),
            ),
            (
                "cname",
                "CNAME",
                TypeInfo(str),
            ),
            (
                "date_created",
                "DateCreated",
                TypeInfo(datetime.datetime),
            ),
            (
                "date_updated",
                "DateUpdated",
                TypeInfo(datetime.datetime),
            ),
            (
                "status",
                "Status",
                TypeInfo(EnvironmentStatus),
            ),
            (
                "abortable_operation_in_progress",
                "AbortableOperationInProgress",
                TypeInfo(bool),
            ),
            (
                "health",
                "Health",
                TypeInfo(EnvironmentHealth),
            ),
            (
                "health_status",
                "HealthStatus",
                TypeInfo(EnvironmentHealthStatus),
            ),
            (
                "resources",
                "Resources",
                TypeInfo(EnvironmentResourcesDescription),
            ),
            (
                "tier",
                "Tier",
                TypeInfo(EnvironmentTier),
            ),
            (
                "environment_links",
                "EnvironmentLinks",
                TypeInfo(typing.List[EnvironmentLink]),
            ),
            (
                "environment_arn",
                "EnvironmentArn",
                TypeInfo(str),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The name of this environment.
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The ID of this environment.
    environment_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the application associated with this environment.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The application version deployed in this environment.
    version_label: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the `SolutionStack` deployed with this environment.
    solution_stack_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The ARN of the platform.
    platform_arn: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the configuration template used to originally launch this
    # environment.
    template_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Describes this environment.
    description: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # For load-balanced, autoscaling environments, the URL to the LoadBalancer.
    # For single-instance environments, the IP address of the instance.
    endpoint_url: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The URL to the CNAME for this environment.
    cname: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The creation date for this environment.
    date_created: datetime.datetime = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The last modified date for this environment.
    date_updated: datetime.datetime = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The current operational status of the environment:

    #   * `Launching`: Environment is in the process of initial deployment.

    #   * `Updating`: Environment is in the process of updating its configuration settings or application version.

    #   * `Ready`: Environment is available to have an action performed on it, such as update or terminate.

    #   * `Terminating`: Environment is in the shut-down process.

    #   * `Terminated`: Environment is not running.
    status: "EnvironmentStatus" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Indicates if there is an in-progress environment configuration update or
    # application version deployment that you can cancel.

    # `true:` There is an update in progress.

    # `false:` There are no updates currently in progress.
    abortable_operation_in_progress: bool = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # Describes the health status of the environment. AWS Elastic Beanstalk
    # indicates the failure levels for a running environment:

    #   * `Red`: Indicates the environment is not responsive. Occurs when three or more consecutive failures occur for an environment.

    #   * `Yellow`: Indicates that something is wrong. Occurs when two consecutive failures occur for an environment.

    #   * `Green`: Indicates the environment is healthy and fully functional.

    #   * `Grey`: Default health for a new environment. The environment is not fully launched and health checks have not started or health checks are suspended during an `UpdateEnvironment` or `RestartEnvironement` request.

    # Default: `Grey`
    health: "EnvironmentHealth" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Returns the health status of the application running in your environment.
    # For more information, see [Health Colors and
    # Statuses](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/health-
    # enhanced-status.html).
    health_status: "EnvironmentHealthStatus" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The description of the AWS resources used by this environment.
    resources: "EnvironmentResourcesDescription" = dataclasses.field(
        default_factory=dict,
    )

    # Describes the current tier of this environment.
    tier: "EnvironmentTier" = dataclasses.field(default_factory=dict, )

    # A list of links to other environments in the same group.
    environment_links: typing.List["EnvironmentLink"] = dataclasses.field(
        default_factory=list,
    )

    # The environment's Amazon Resource Name (ARN), which can be used in other
    # API requests that require an ARN.
    environment_arn: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class EnvironmentDescriptionsMessage(OutputShapeBase):
    """
    Result message containing a list of environment descriptions.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "environments",
                "Environments",
                TypeInfo(typing.List[EnvironmentDescription]),
            ),
            (
                "next_token",
                "NextToken",
                TypeInfo(str),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # Returns an EnvironmentDescription list.
    environments: typing.List["EnvironmentDescription"] = dataclasses.field(
        default_factory=list,
    )

    # In a paginated request, the token that you can pass in a subsequent request
    # to get the next response page.
    next_token: str = dataclasses.field(default=ShapeBase.NOT_SET, )


class EnvironmentHealth(Enum):
    Green = "Green"
    Yellow = "Yellow"
    Red = "Red"
    Grey = "Grey"


class EnvironmentHealthAttribute(Enum):
    Status = "Status"
    Color = "Color"
    Causes = "Causes"
    ApplicationMetrics = "ApplicationMetrics"
    InstancesHealth = "InstancesHealth"
    All = "All"
    HealthStatus = "HealthStatus"
    RefreshedAt = "RefreshedAt"


class EnvironmentHealthStatus(Enum):
    NoData = "NoData"
    Unknown = "Unknown"
    Pending = "Pending"
    Ok = "Ok"
    Info = "Info"
    Warning = "Warning"
    Degraded = "Degraded"
    Severe = "Severe"
    Suspended = "Suspended"


@dataclasses.dataclass
class EnvironmentInfoDescription(ShapeBase):
    """
    The information retrieved from the Amazon EC2 instances.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "info_type",
                "InfoType",
                TypeInfo(EnvironmentInfoType),
            ),
            (
                "ec2_instance_id",
                "Ec2InstanceId",
                TypeInfo(str),
            ),
            (
                "sample_timestamp",
                "SampleTimestamp",
                TypeInfo(datetime.datetime),
            ),
            (
                "message",
                "Message",
                TypeInfo(str),
            ),
        ]

    # The type of information retrieved.
    info_type: "EnvironmentInfoType" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The Amazon EC2 Instance ID for this information.
    ec2_instance_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The time stamp when this information was retrieved.
    sample_timestamp: datetime.datetime = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The retrieved information.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


class EnvironmentInfoType(Enum):
    tail = "tail"
    bundle = "bundle"


@dataclasses.dataclass
class EnvironmentLink(ShapeBase):
    """
    A link to another environment, defined in the environment's manifest. Links
    provide connection information in system properties that can be used to connect
    to another environment in the same group. See [Environment Manifest
    (env.yaml)](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environment-
    cfg-manifest.html) for details.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "link_name",
                "LinkName",
                TypeInfo(str),
            ),
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
        ]

    # The name of the link.
    link_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the linked environment (the dependency).
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class EnvironmentResourceDescription(ShapeBase):
    """
    Describes the AWS resources in use by this environment. This data is live.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
            (
                "auto_scaling_groups",
                "AutoScalingGroups",
                TypeInfo(typing.List[AutoScalingGroup]),
            ),
            (
                "instances",
                "Instances",
                TypeInfo(typing.List[Instance]),
            ),
            (
                "launch_configurations",
                "LaunchConfigurations",
                TypeInfo(typing.List[LaunchConfiguration]),
            ),
            (
                "load_balancers",
                "LoadBalancers",
                TypeInfo(typing.List[LoadBalancer]),
            ),
            (
                "triggers",
                "Triggers",
                TypeInfo(typing.List[Trigger]),
            ),
            (
                "queues",
                "Queues",
                TypeInfo(typing.List[Queue]),
            ),
        ]

    # The name of the environment.
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The `AutoScalingGroups` used by this environment.
    auto_scaling_groups: typing.List["AutoScalingGroup"] = dataclasses.field(
        default_factory=list,
    )

    # The Amazon EC2 instances used by this environment.
    instances: typing.List["Instance"] = dataclasses.field(
        default_factory=list,
    )

    # The Auto Scaling launch configurations in use by this environment.
    launch_configurations: typing.List["LaunchConfiguration"
                                      ] = dataclasses.field(
                                          default_factory=list,
                                      )

    # The LoadBalancers in use by this environment.
    load_balancers: typing.List["LoadBalancer"] = dataclasses.field(
        default_factory=list,
    )

    # The `AutoScaling` triggers in use by this environment.
    triggers: typing.List["Trigger"] = dataclasses.field(default_factory=list, )

    # The queues used by this environment.
    queues: typing.List["Queue"] = dataclasses.field(default_factory=list, )


@dataclasses.dataclass
class EnvironmentResourceDescriptionsMessage(OutputShapeBase):
    """
    Result message containing a list of environment resource descriptions.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "environment_resources",
                "EnvironmentResources",
                TypeInfo(EnvironmentResourceDescription),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A list of EnvironmentResourceDescription.
    environment_resources: "EnvironmentResourceDescription" = dataclasses.field(
        default_factory=dict,
    )


@dataclasses.dataclass
class EnvironmentResourcesDescription(ShapeBase):
    """
    Describes the AWS resources in use by this environment. This data is not live
    data.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "load_balancer",
                "LoadBalancer",
                TypeInfo(LoadBalancerDescription),
            ),
        ]

    # Describes the LoadBalancer.
    load_balancer: "LoadBalancerDescription" = dataclasses.field(
        default_factory=dict,
    )


class EnvironmentStatus(Enum):
    Launching = "Launching"
    Updating = "Updating"
    Ready = "Ready"
    Terminating = "Terminating"
    Terminated = "Terminated"


@dataclasses.dataclass
class EnvironmentTier(ShapeBase):
    """
    Describes the properties of an environment tier
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "name",
                "Name",
                TypeInfo(str),
            ),
            (
                "type",
                "Type",
                TypeInfo(str),
            ),
            (
                "version",
                "Version",
                TypeInfo(str),
            ),
        ]

    # The name of this environment tier.
    name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The type of this environment tier.
    type: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The version of this environment tier. When you don't set a value to it,
    # Elastic Beanstalk uses the latest compatible worker tier version.

    # This member is deprecated. Any specific version that you set may become out
    # of date. We recommend leaving it unspecified.
    version: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class EventDescription(ShapeBase):
    """
    Describes an event.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "event_date",
                "EventDate",
                TypeInfo(datetime.datetime),
            ),
            (
                "message",
                "Message",
                TypeInfo(str),
            ),
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "version_label",
                "VersionLabel",
                TypeInfo(str),
            ),
            (
                "template_name",
                "TemplateName",
                TypeInfo(str),
            ),
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
            (
                "platform_arn",
                "PlatformArn",
                TypeInfo(str),
            ),
            (
                "request_id",
                "RequestId",
                TypeInfo(str),
            ),
            (
                "severity",
                "Severity",
                TypeInfo(EventSeverity),
            ),
        ]

    # The date when the event occurred.
    event_date: datetime.datetime = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The event message.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The application associated with the event.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The release label for the application version associated with this event.
    version_label: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the configuration associated with this event.
    template_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the environment associated with this event.
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The ARN of the platform.
    platform_arn: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The web service request ID for the activity of this event.
    request_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The severity level of this event.
    severity: "EventSeverity" = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class EventDescriptionsMessage(OutputShapeBase):
    """
    Result message wrapping a list of event descriptions.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "events",
                "Events",
                TypeInfo(typing.List[EventDescription]),
            ),
            (
                "next_token",
                "NextToken",
                TypeInfo(str),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A list of EventDescription.
    events: typing.List["EventDescription"] = dataclasses.field(
        default_factory=list,
    )

    # If returned, this indicates that there are more results to obtain. Use this
    # token in the next DescribeEvents call to get the next batch of events.
    next_token: str = dataclasses.field(default=ShapeBase.NOT_SET, )


class EventSeverity(Enum):
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    FATAL = "FATAL"


class FailureType(Enum):
    UpdateCancelled = "UpdateCancelled"
    CancellationFailed = "CancellationFailed"
    RollbackFailed = "RollbackFailed"
    RollbackSuccessful = "RollbackSuccessful"
    InternalFailure = "InternalFailure"
    InvalidEnvironmentState = "InvalidEnvironmentState"
    PermissionsError = "PermissionsError"


@dataclasses.dataclass
class Instance(ShapeBase):
    """
    The description of an Amazon EC2 instance.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "id",
                "Id",
                TypeInfo(str),
            ),
        ]

    # The ID of the Amazon EC2 instance.
    id: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class InstanceHealthSummary(ShapeBase):
    """
    Represents summary information about the health of an instance. For more
    information, see [Health Colors and
    Statuses](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/health-enhanced-
    status.html).
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "no_data",
                "NoData",
                TypeInfo(int),
            ),
            (
                "unknown",
                "Unknown",
                TypeInfo(int),
            ),
            (
                "pending",
                "Pending",
                TypeInfo(int),
            ),
            (
                "ok",
                "Ok",
                TypeInfo(int),
            ),
            (
                "info",
                "Info",
                TypeInfo(int),
            ),
            (
                "warning",
                "Warning",
                TypeInfo(int),
            ),
            (
                "degraded",
                "Degraded",
                TypeInfo(int),
            ),
            (
                "severe",
                "Severe",
                TypeInfo(int),
            ),
        ]

    # **Grey.** AWS Elastic Beanstalk and the health agent are reporting no data
    # on an instance.
    no_data: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # **Grey.** AWS Elastic Beanstalk and the health agent are reporting an
    # insufficient amount of data on an instance.
    unknown: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # **Grey.** An operation is in progress on an instance within the command
    # timeout.
    pending: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # **Green.** An instance is passing health checks and the health agent is not
    # reporting any problems.
    ok: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # **Green.** An operation is in progress on an instance.
    info: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # **Yellow.** The health agent is reporting a moderate number of request
    # failures or other issues for an instance or environment.
    warning: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # **Red.** The health agent is reporting a high number of request failures or
    # other issues for an instance or environment.
    degraded: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # **Red.** The health agent is reporting a very high number of request
    # failures or other issues for an instance or environment.
    severe: int = dataclasses.field(default=ShapeBase.NOT_SET, )


class InstancesHealthAttribute(Enum):
    HealthStatus = "HealthStatus"
    Color = "Color"
    Causes = "Causes"
    ApplicationMetrics = "ApplicationMetrics"
    RefreshedAt = "RefreshedAt"
    LaunchedAt = "LaunchedAt"
    System = "System"
    Deployment = "Deployment"
    AvailabilityZone = "AvailabilityZone"
    InstanceType = "InstanceType"
    All = "All"


@dataclasses.dataclass
class InsufficientPrivilegesException(ShapeBase):
    """
    The specified account does not have sufficient privileges for one or more AWS
    services.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return []


@dataclasses.dataclass
class InvalidRequestException(ShapeBase):
    """
    One or more input parameters is not valid. Please correct the input parameters
    and try the operation again.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return []


@dataclasses.dataclass
class Latency(ShapeBase):
    """
    Represents the average latency for the slowest X percent of requests over the
    last 10 seconds.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "p999",
                "P999",
                TypeInfo(float),
            ),
            (
                "p99",
                "P99",
                TypeInfo(float),
            ),
            (
                "p95",
                "P95",
                TypeInfo(float),
            ),
            (
                "p90",
                "P90",
                TypeInfo(float),
            ),
            (
                "p85",
                "P85",
                TypeInfo(float),
            ),
            (
                "p75",
                "P75",
                TypeInfo(float),
            ),
            (
                "p50",
                "P50",
                TypeInfo(float),
            ),
            (
                "p10",
                "P10",
                TypeInfo(float),
            ),
        ]

    # The average latency for the slowest 0.1 percent of requests over the last
    # 10 seconds.
    p999: float = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The average latency for the slowest 1 percent of requests over the last 10
    # seconds.
    p99: float = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The average latency for the slowest 5 percent of requests over the last 10
    # seconds.
    p95: float = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The average latency for the slowest 10 percent of requests over the last 10
    # seconds.
    p90: float = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The average latency for the slowest 15 percent of requests over the last 10
    # seconds.
    p85: float = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The average latency for the slowest 25 percent of requests over the last 10
    # seconds.
    p75: float = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The average latency for the slowest 50 percent of requests over the last 10
    # seconds.
    p50: float = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The average latency for the slowest 90 percent of requests over the last 10
    # seconds.
    p10: float = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class LaunchConfiguration(ShapeBase):
    """
    Describes an Auto Scaling launch configuration.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "name",
                "Name",
                TypeInfo(str),
            ),
        ]

    # The name of the launch configuration.
    name: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListAvailableSolutionStacksResultMessage(OutputShapeBase):
    """
    A list of available AWS Elastic Beanstalk solution stacks.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "solution_stacks",
                "SolutionStacks",
                TypeInfo(typing.List[str]),
            ),
            (
                "solution_stack_details",
                "SolutionStackDetails",
                TypeInfo(typing.List[SolutionStackDescription]),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A list of available solution stacks.
    solution_stacks: typing.List[str] = dataclasses.field(
        default_factory=list,
    )

    # A list of available solution stacks and their SolutionStackDescription.
    solution_stack_details: typing.List["SolutionStackDescription"
                                       ] = dataclasses.field(
                                           default_factory=list,
                                       )


@dataclasses.dataclass
class ListPlatformVersionsRequest(ShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "filters",
                "Filters",
                TypeInfo(typing.List[PlatformFilter]),
            ),
            (
                "max_records",
                "MaxRecords",
                TypeInfo(int),
            ),
            (
                "next_token",
                "NextToken",
                TypeInfo(str),
            ),
        ]

    # List only the platforms where the platform member value relates to one of
    # the supplied values.
    filters: typing.List["PlatformFilter"] = dataclasses.field(
        default_factory=list,
    )

    # The maximum number of platform values returned in one call.
    max_records: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The starting index into the remaining list of platforms. Use the
    # `NextToken` value from a previous `ListPlatformVersion` call.
    next_token: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListPlatformVersionsResult(OutputShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "platform_summary_list",
                "PlatformSummaryList",
                TypeInfo(typing.List[PlatformSummary]),
            ),
            (
                "next_token",
                "NextToken",
                TypeInfo(str),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # Detailed information about the platforms.
    platform_summary_list: typing.List["PlatformSummary"] = dataclasses.field(
        default_factory=list,
    )

    # The starting index into the remaining list of platforms. if this value is
    # not `null`, you can use it in a subsequent `ListPlatformVersion` call.
    next_token: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListTagsForResourceMessage(ShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "resource_arn",
                "ResourceArn",
                TypeInfo(str),
            ),
        ]

    # The Amazon Resource Name (ARN) of the resouce for which a tag list is
    # requested.

    # Must be the ARN of an Elastic Beanstalk environment.
    resource_arn: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class Listener(ShapeBase):
    """
    Describes the properties of a Listener for the LoadBalancer.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "protocol",
                "Protocol",
                TypeInfo(str),
            ),
            (
                "port",
                "Port",
                TypeInfo(int),
            ),
        ]

    # The protocol that is used by the Listener.
    protocol: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The port that is used by the Listener.
    port: int = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class LoadBalancer(ShapeBase):
    """
    Describes a LoadBalancer.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "name",
                "Name",
                TypeInfo(str),
            ),
        ]

    # The name of the LoadBalancer.
    name: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class LoadBalancerDescription(ShapeBase):
    """
    Describes the details of a LoadBalancer.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "load_balancer_name",
                "LoadBalancerName",
                TypeInfo(str),
            ),
            (
                "domain",
                "Domain",
                TypeInfo(str),
            ),
            (
                "listeners",
                "Listeners",
                TypeInfo(typing.List[Listener]),
            ),
        ]

    # The name of the LoadBalancer.
    load_balancer_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The domain name of the LoadBalancer.
    domain: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A list of Listeners used by the LoadBalancer.
    listeners: typing.List["Listener"] = dataclasses.field(
        default_factory=list,
    )


@dataclasses.dataclass
class ManagedAction(ShapeBase):
    """
    The record of an upcoming or in-progress managed action.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "action_id",
                "ActionId",
                TypeInfo(str),
            ),
            (
                "action_description",
                "ActionDescription",
                TypeInfo(str),
            ),
            (
                "action_type",
                "ActionType",
                TypeInfo(ActionType),
            ),
            (
                "status",
                "Status",
                TypeInfo(ActionStatus),
            ),
            (
                "window_start_time",
                "WindowStartTime",
                TypeInfo(datetime.datetime),
            ),
        ]

    # A unique identifier for the managed action.
    action_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A description of the managed action.
    action_description: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The type of managed action.
    action_type: "ActionType" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The status of the managed action. If the action is `Scheduled`, you can
    # apply it immediately with ApplyEnvironmentManagedAction.
    status: "ActionStatus" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The start time of the maintenance window in which the managed action will
    # execute.
    window_start_time: datetime.datetime = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


@dataclasses.dataclass
class ManagedActionHistoryItem(ShapeBase):
    """
    The record of a completed or failed managed action.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "action_id",
                "ActionId",
                TypeInfo(str),
            ),
            (
                "action_type",
                "ActionType",
                TypeInfo(ActionType),
            ),
            (
                "action_description",
                "ActionDescription",
                TypeInfo(str),
            ),
            (
                "failure_type",
                "FailureType",
                TypeInfo(FailureType),
            ),
            (
                "status",
                "Status",
                TypeInfo(ActionHistoryStatus),
            ),
            (
                "failure_description",
                "FailureDescription",
                TypeInfo(str),
            ),
            (
                "executed_time",
                "ExecutedTime",
                TypeInfo(datetime.datetime),
            ),
            (
                "finished_time",
                "FinishedTime",
                TypeInfo(datetime.datetime),
            ),
        ]

    # A unique identifier for the managed action.
    action_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The type of the managed action.
    action_type: "ActionType" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A description of the managed action.
    action_description: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If the action failed, the type of failure.
    failure_type: "FailureType" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The status of the action.
    status: "ActionHistoryStatus" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # If the action failed, a description of the failure.
    failure_description: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The date and time that the action started executing.
    executed_time: datetime.datetime = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The date and time that the action finished executing.
    finished_time: datetime.datetime = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


@dataclasses.dataclass
class ManagedActionInvalidStateException(ShapeBase):
    """
    Cannot modify the managed action in its current state.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return []


@dataclasses.dataclass
class MaxAgeRule(ShapeBase):
    """
    A lifecycle rule that deletes application versions after the specified number of
    days.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "enabled",
                "Enabled",
                TypeInfo(bool),
            ),
            (
                "max_age_in_days",
                "MaxAgeInDays",
                TypeInfo(int),
            ),
            (
                "delete_source_from_s3",
                "DeleteSourceFromS3",
                TypeInfo(bool),
            ),
        ]

    # Specify `true` to apply the rule, or `false` to disable it.
    enabled: bool = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Specify the number of days to retain an application versions.
    max_age_in_days: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Set to `true` to delete a version's source bundle from Amazon S3 when
    # Elastic Beanstalk deletes the application version.
    delete_source_from_s3: bool = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class MaxCountRule(ShapeBase):
    """
    A lifecycle rule that deletes the oldest application version when the maximum
    count is exceeded.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "enabled",
                "Enabled",
                TypeInfo(bool),
            ),
            (
                "max_count",
                "MaxCount",
                TypeInfo(int),
            ),
            (
                "delete_source_from_s3",
                "DeleteSourceFromS3",
                TypeInfo(bool),
            ),
        ]

    # Specify `true` to apply the rule, or `false` to disable it.
    enabled: bool = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Specify the maximum number of application versions to retain.
    max_count: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Set to `true` to delete a version's source bundle from Amazon S3 when
    # Elastic Beanstalk deletes the application version.
    delete_source_from_s3: bool = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class OperationInProgressException(ShapeBase):
    """
    Unable to perform the specified operation because another operation that effects
    an element in this activity is already in progress.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return []


@dataclasses.dataclass
class OptionRestrictionRegex(ShapeBase):
    """
    A regular expression representing a restriction on a string configuration option
    value.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "pattern",
                "Pattern",
                TypeInfo(str),
            ),
            (
                "label",
                "Label",
                TypeInfo(str),
            ),
        ]

    # The regular expression pattern that a string configuration option value
    # with this restriction must match.
    pattern: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A unique name representing this regular expression.
    label: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class OptionSpecification(ShapeBase):
    """
    A specification identifying an individual configuration option.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "resource_name",
                "ResourceName",
                TypeInfo(str),
            ),
            (
                "namespace",
                "Namespace",
                TypeInfo(str),
            ),
            (
                "option_name",
                "OptionName",
                TypeInfo(str),
            ),
        ]

    # A unique resource name for a time-based scaling configuration option.
    resource_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A unique namespace identifying the option's associated AWS resource.
    namespace: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the configuration option.
    option_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class PlatformDescription(ShapeBase):
    """
    Detailed information about a platform.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "platform_arn",
                "PlatformArn",
                TypeInfo(str),
            ),
            (
                "platform_owner",
                "PlatformOwner",
                TypeInfo(str),
            ),
            (
                "platform_name",
                "PlatformName",
                TypeInfo(str),
            ),
            (
                "platform_version",
                "PlatformVersion",
                TypeInfo(str),
            ),
            (
                "solution_stack_name",
                "SolutionStackName",
                TypeInfo(str),
            ),
            (
                "platform_status",
                "PlatformStatus",
                TypeInfo(PlatformStatus),
            ),
            (
                "date_created",
                "DateCreated",
                TypeInfo(datetime.datetime),
            ),
            (
                "date_updated",
                "DateUpdated",
                TypeInfo(datetime.datetime),
            ),
            (
                "platform_category",
                "PlatformCategory",
                TypeInfo(str),
            ),
            (
                "description",
                "Description",
                TypeInfo(str),
            ),
            (
                "maintainer",
                "Maintainer",
                TypeInfo(str),
            ),
            (
                "operating_system_name",
                "OperatingSystemName",
                TypeInfo(str),
            ),
            (
                "operating_system_version",
                "OperatingSystemVersion",
                TypeInfo(str),
            ),
            (
                "programming_languages",
                "ProgrammingLanguages",
                TypeInfo(typing.List[PlatformProgrammingLanguage]),
            ),
            (
                "frameworks",
                "Frameworks",
                TypeInfo(typing.List[PlatformFramework]),
            ),
            (
                "custom_ami_list",
                "CustomAmiList",
                TypeInfo(typing.List[CustomAmi]),
            ),
            (
                "supported_tier_list",
                "SupportedTierList",
                TypeInfo(typing.List[str]),
            ),
            (
                "supported_addon_list",
                "SupportedAddonList",
                TypeInfo(typing.List[str]),
            ),
        ]

    # The ARN of the platform.
    platform_arn: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The AWS account ID of the person who created the platform.
    platform_owner: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the platform.
    platform_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The version of the platform.
    platform_version: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the solution stack used by the platform.
    solution_stack_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The status of the platform.
    platform_status: "PlatformStatus" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The date when the platform was created.
    date_created: datetime.datetime = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The date when the platform was last updated.
    date_updated: datetime.datetime = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The category of the platform.
    platform_category: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The description of the platform.
    description: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Information about the maintainer of the platform.
    maintainer: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The operating system used by the platform.
    operating_system_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The version of the operating system used by the platform.
    operating_system_version: str = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The programming languages supported by the platform.
    programming_languages: typing.List["PlatformProgrammingLanguage"
                                      ] = dataclasses.field(
                                          default_factory=list,
                                      )

    # The frameworks supported by the platform.
    frameworks: typing.List["PlatformFramework"] = dataclasses.field(
        default_factory=list,
    )

    # The custom AMIs supported by the platform.
    custom_ami_list: typing.List["CustomAmi"] = dataclasses.field(
        default_factory=list,
    )

    # The tiers supported by the platform.
    supported_tier_list: typing.List[str] = dataclasses.field(
        default_factory=list,
    )

    # The additions supported by the platform.
    supported_addon_list: typing.List[str] = dataclasses.field(
        default_factory=list,
    )


@dataclasses.dataclass
class PlatformFilter(ShapeBase):
    """
    Specify criteria to restrict the results when listing custom platforms.

    The filter is evaluated as the expression:

    `Type` `Operator` `Values[i]`
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "type",
                "Type",
                TypeInfo(str),
            ),
            (
                "operator",
                "Operator",
                TypeInfo(str),
            ),
            (
                "values",
                "Values",
                TypeInfo(typing.List[str]),
            ),
        ]

    # The custom platform attribute to which the filter values are applied.

    # Valid Values: `PlatformName` | `PlatformVersion` | `PlatformStatus` |
    # `PlatformOwner`
    type: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The operator to apply to the `Type` with each of the `Values`.

    # Valid Values: `=` (equal to) | `!=` (not equal to) | `<` (less than) | `<=`
    # (less than or equal to) | `>` (greater than) | `>=` (greater than or equal
    # to) | `contains` | `begins_with` | `ends_with`
    operator: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The list of values applied to the custom platform attribute.
    values: typing.List[str] = dataclasses.field(default_factory=list, )


@dataclasses.dataclass
class PlatformFramework(ShapeBase):
    """
    A framework supported by the custom platform.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "name",
                "Name",
                TypeInfo(str),
            ),
            (
                "version",
                "Version",
                TypeInfo(str),
            ),
        ]

    # The name of the framework.
    name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The version of the framework.
    version: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class PlatformProgrammingLanguage(ShapeBase):
    """
    A programming language supported by the platform.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "name",
                "Name",
                TypeInfo(str),
            ),
            (
                "version",
                "Version",
                TypeInfo(str),
            ),
        ]

    # The name of the programming language.
    name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The version of the programming language.
    version: str = dataclasses.field(default=ShapeBase.NOT_SET, )


class PlatformStatus(Enum):
    Creating = "Creating"
    Failed = "Failed"
    Ready = "Ready"
    Deleting = "Deleting"
    Deleted = "Deleted"


@dataclasses.dataclass
class PlatformSummary(ShapeBase):
    """
    Detailed information about a platform.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "platform_arn",
                "PlatformArn",
                TypeInfo(str),
            ),
            (
                "platform_owner",
                "PlatformOwner",
                TypeInfo(str),
            ),
            (
                "platform_status",
                "PlatformStatus",
                TypeInfo(PlatformStatus),
            ),
            (
                "platform_category",
                "PlatformCategory",
                TypeInfo(str),
            ),
            (
                "operating_system_name",
                "OperatingSystemName",
                TypeInfo(str),
            ),
            (
                "operating_system_version",
                "OperatingSystemVersion",
                TypeInfo(str),
            ),
            (
                "supported_tier_list",
                "SupportedTierList",
                TypeInfo(typing.List[str]),
            ),
            (
                "supported_addon_list",
                "SupportedAddonList",
                TypeInfo(typing.List[str]),
            ),
        ]

    # The ARN of the platform.
    platform_arn: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The AWS account ID of the person who created the platform.
    platform_owner: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The status of the platform. You can create an environment from the platform
    # once it is ready.
    platform_status: "PlatformStatus" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The category of platform.
    platform_category: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The operating system used by the platform.
    operating_system_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The version of the operating system used by the platform.
    operating_system_version: str = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The tiers in which the platform runs.
    supported_tier_list: typing.List[str] = dataclasses.field(
        default_factory=list,
    )

    # The additions associated with the platform.
    supported_addon_list: typing.List[str] = dataclasses.field(
        default_factory=list,
    )


@dataclasses.dataclass
class PlatformVersionStillReferencedException(ShapeBase):
    """
    You cannot delete the platform version because there are still environments
    running on it.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return []


@dataclasses.dataclass
class Queue(ShapeBase):
    """
    Describes a queue.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "name",
                "Name",
                TypeInfo(str),
            ),
            (
                "url",
                "URL",
                TypeInfo(str),
            ),
        ]

    # The name of the queue.
    name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The URL of the queue.
    url: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class RebuildEnvironmentMessage(ShapeBase):
    """

    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "environment_id",
                "EnvironmentId",
                TypeInfo(str),
            ),
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
        ]

    # The ID of the environment to rebuild.

    # Condition: You must specify either this or an EnvironmentName, or both. If
    # you do not specify either, AWS Elastic Beanstalk returns
    # `MissingRequiredParameter` error.
    environment_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the environment to rebuild.

    # Condition: You must specify either this or an EnvironmentId, or both. If
    # you do not specify either, AWS Elastic Beanstalk returns
    # `MissingRequiredParameter` error.
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class RequestEnvironmentInfoMessage(ShapeBase):
    """
    Request to retrieve logs from an environment and store them in your Elastic
    Beanstalk storage bucket.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "info_type",
                "InfoType",
                TypeInfo(EnvironmentInfoType),
            ),
            (
                "environment_id",
                "EnvironmentId",
                TypeInfo(str),
            ),
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
        ]

    # The type of information to request.
    info_type: "EnvironmentInfoType" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The ID of the environment of the requested data.

    # If no such environment is found, `RequestEnvironmentInfo` returns an
    # `InvalidParameterValue` error.

    # Condition: You must specify either this or an EnvironmentName, or both. If
    # you do not specify either, AWS Elastic Beanstalk returns
    # `MissingRequiredParameter` error.
    environment_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the environment of the requested data.

    # If no such environment is found, `RequestEnvironmentInfo` returns an
    # `InvalidParameterValue` error.

    # Condition: You must specify either this or an EnvironmentId, or both. If
    # you do not specify either, AWS Elastic Beanstalk returns
    # `MissingRequiredParameter` error.
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ResourceNotFoundException(ShapeBase):
    """
    A resource doesn't exist for the specified Amazon Resource Name (ARN).
    """

    @classmethod
    def _get_boto_mapping(cls):
        return []


@dataclasses.dataclass
class ResourceQuota(ShapeBase):
    """
    The AWS Elastic Beanstalk quota information for a single resource type in an AWS
    account. It reflects the resource's limits for this account.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "maximum",
                "Maximum",
                TypeInfo(int),
            ),
        ]

    # The maximum number of instances of this Elastic Beanstalk resource type
    # that an AWS account can use.
    maximum: int = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ResourceQuotas(ShapeBase):
    """
    A set of per-resource AWS Elastic Beanstalk quotas associated with an AWS
    account. They reflect Elastic Beanstalk resource limits for this account.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "application_quota",
                "ApplicationQuota",
                TypeInfo(ResourceQuota),
            ),
            (
                "application_version_quota",
                "ApplicationVersionQuota",
                TypeInfo(ResourceQuota),
            ),
            (
                "environment_quota",
                "EnvironmentQuota",
                TypeInfo(ResourceQuota),
            ),
            (
                "configuration_template_quota",
                "ConfigurationTemplateQuota",
                TypeInfo(ResourceQuota),
            ),
            (
                "custom_platform_quota",
                "CustomPlatformQuota",
                TypeInfo(ResourceQuota),
            ),
        ]

    # The quota for applications in the AWS account.
    application_quota: "ResourceQuota" = dataclasses.field(
        default_factory=dict,
    )

    # The quota for application versions in the AWS account.
    application_version_quota: "ResourceQuota" = dataclasses.field(
        default_factory=dict,
    )

    # The quota for environments in the AWS account.
    environment_quota: "ResourceQuota" = dataclasses.field(
        default_factory=dict,
    )

    # The quota for configuration templates in the AWS account.
    configuration_template_quota: "ResourceQuota" = dataclasses.field(
        default_factory=dict,
    )

    # The quota for custom platforms in the AWS account.
    custom_platform_quota: "ResourceQuota" = dataclasses.field(
        default_factory=dict,
    )


@dataclasses.dataclass
class ResourceTagsDescriptionMessage(OutputShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "resource_arn",
                "ResourceArn",
                TypeInfo(str),
            ),
            (
                "resource_tags",
                "ResourceTags",
                TypeInfo(typing.List[Tag]),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The Amazon Resource Name (ARN) of the resouce for which a tag list was
    # requested.
    resource_arn: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A list of tag key-value pairs.
    resource_tags: typing.List["Tag"] = dataclasses.field(
        default_factory=list,
    )


@dataclasses.dataclass
class ResourceTypeNotSupportedException(ShapeBase):
    """
    The type of the specified Amazon Resource Name (ARN) isn't supported for this
    operation.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return []


@dataclasses.dataclass
class RestartAppServerMessage(ShapeBase):
    """

    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "environment_id",
                "EnvironmentId",
                TypeInfo(str),
            ),
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
        ]

    # The ID of the environment to restart the server for.

    # Condition: You must specify either this or an EnvironmentName, or both. If
    # you do not specify either, AWS Elastic Beanstalk returns
    # `MissingRequiredParameter` error.
    environment_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the environment to restart the server for.

    # Condition: You must specify either this or an EnvironmentId, or both. If
    # you do not specify either, AWS Elastic Beanstalk returns
    # `MissingRequiredParameter` error.
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class RetrieveEnvironmentInfoMessage(ShapeBase):
    """
    Request to download logs retrieved with RequestEnvironmentInfo.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "info_type",
                "InfoType",
                TypeInfo(EnvironmentInfoType),
            ),
            (
                "environment_id",
                "EnvironmentId",
                TypeInfo(str),
            ),
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
        ]

    # The type of information to retrieve.
    info_type: "EnvironmentInfoType" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The ID of the data's environment.

    # If no such environment is found, returns an `InvalidParameterValue` error.

    # Condition: You must specify either this or an EnvironmentName, or both. If
    # you do not specify either, AWS Elastic Beanstalk returns
    # `MissingRequiredParameter` error.
    environment_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the data's environment.

    # If no such environment is found, returns an `InvalidParameterValue` error.

    # Condition: You must specify either this or an EnvironmentId, or both. If
    # you do not specify either, AWS Elastic Beanstalk returns
    # `MissingRequiredParameter` error.
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class RetrieveEnvironmentInfoResultMessage(OutputShapeBase):
    """
    Result message containing a description of the requested environment info.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "environment_info",
                "EnvironmentInfo",
                TypeInfo(typing.List[EnvironmentInfoDescription]),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The EnvironmentInfoDescription of the environment.
    environment_info: typing.List["EnvironmentInfoDescription"
                                 ] = dataclasses.field(
                                     default_factory=list,
                                 )


@dataclasses.dataclass
class S3Location(ShapeBase):
    """
    The bucket and key of an item stored in Amazon S3.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "s3_bucket",
                "S3Bucket",
                TypeInfo(str),
            ),
            (
                "s3_key",
                "S3Key",
                TypeInfo(str),
            ),
        ]

    # The Amazon S3 bucket where the data is located.
    s3_bucket: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The Amazon S3 key where the data is located.
    s3_key: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class S3LocationNotInServiceRegionException(ShapeBase):
    """
    The specified S3 bucket does not belong to the S3 region in which the service is
    running. The following regions are supported:

      * IAD/us-east-1

      * PDX/us-west-2

      * DUB/eu-west-1
    """

    @classmethod
    def _get_boto_mapping(cls):
        return []


@dataclasses.dataclass
class S3SubscriptionRequiredException(ShapeBase):
    """
    The specified account does not have a subscription to Amazon S3.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return []


@dataclasses.dataclass
class SingleInstanceHealth(ShapeBase):
    """
    Detailed health information about an Amazon EC2 instance in your Elastic
    Beanstalk environment.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "instance_id",
                "InstanceId",
                TypeInfo(str),
            ),
            (
                "health_status",
                "HealthStatus",
                TypeInfo(str),
            ),
            (
                "color",
                "Color",
                TypeInfo(str),
            ),
            (
                "causes",
                "Causes",
                TypeInfo(typing.List[str]),
            ),
            (
                "launched_at",
                "LaunchedAt",
                TypeInfo(datetime.datetime),
            ),
            (
                "application_metrics",
                "ApplicationMetrics",
                TypeInfo(ApplicationMetrics),
            ),
            (
                "system",
                "System",
                TypeInfo(SystemStatus),
            ),
            (
                "deployment",
                "Deployment",
                TypeInfo(Deployment),
            ),
            (
                "availability_zone",
                "AvailabilityZone",
                TypeInfo(str),
            ),
            (
                "instance_type",
                "InstanceType",
                TypeInfo(str),
            ),
        ]

    # The ID of the Amazon EC2 instance.
    instance_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Returns the health status of the specified instance. For more information,
    # see [Health Colors and
    # Statuses](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/health-
    # enhanced-status.html).
    health_status: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Represents the color indicator that gives you information about the health
    # of the EC2 instance. For more information, see [Health Colors and
    # Statuses](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/health-
    # enhanced-status.html).
    color: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Represents the causes, which provide more information about the current
    # health status.
    causes: typing.List[str] = dataclasses.field(default_factory=list, )

    # The time at which the EC2 instance was launched.
    launched_at: datetime.datetime = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # Request metrics from your application.
    application_metrics: "ApplicationMetrics" = dataclasses.field(
        default_factory=dict,
    )

    # Operating system metrics from the instance.
    system: "SystemStatus" = dataclasses.field(default_factory=dict, )

    # Information about the most recent deployment to an instance.
    deployment: "Deployment" = dataclasses.field(default_factory=dict, )

    # The availability zone in which the instance runs.
    availability_zone: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The instance's type.
    instance_type: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class SolutionStackDescription(ShapeBase):
    """
    Describes the solution stack.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "solution_stack_name",
                "SolutionStackName",
                TypeInfo(str),
            ),
            (
                "permitted_file_types",
                "PermittedFileTypes",
                TypeInfo(typing.List[str]),
            ),
        ]

    # The name of the solution stack.
    solution_stack_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The permitted file types allowed for a solution stack.
    permitted_file_types: typing.List[str] = dataclasses.field(
        default_factory=list,
    )


@dataclasses.dataclass
class SourceBuildInformation(ShapeBase):
    """
    Location of the source code for an application version.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "source_type",
                "SourceType",
                TypeInfo(SourceType),
            ),
            (
                "source_repository",
                "SourceRepository",
                TypeInfo(SourceRepository),
            ),
            (
                "source_location",
                "SourceLocation",
                TypeInfo(str),
            ),
        ]

    # The type of repository.

    #   * `Git`

    #   * `Zip`
    source_type: "SourceType" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Location where the repository is stored.

    #   * `CodeCommit`

    #   * `S3`
    source_repository: "SourceRepository" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The location of the source code, as a formatted string, depending on the
    # value of `SourceRepository`

    #   * For `CodeCommit`, the format is the repository name and commit ID, separated by a forward slash. For example, `my-git-repo/265cfa0cf6af46153527f55d6503ec030551f57a`.

    #   * For `S3`, the format is the S3 bucket name and object key, separated by a forward slash. For example, `my-s3-bucket/Folders/my-source-file`.
    source_location: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class SourceBundleDeletionException(ShapeBase):
    """
    Unable to delete the Amazon S3 source bundle associated with the application
    version. The application version was deleted successfully.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return []


@dataclasses.dataclass
class SourceConfiguration(ShapeBase):
    """
    A specification for an environment configuration
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "template_name",
                "TemplateName",
                TypeInfo(str),
            ),
        ]

    # The name of the application associated with the configuration.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the configuration template.
    template_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )


class SourceRepository(Enum):
    CodeCommit = "CodeCommit"
    S3 = "S3"


class SourceType(Enum):
    Git = "Git"
    Zip = "Zip"


@dataclasses.dataclass
class StatusCodes(ShapeBase):
    """
    Represents the percentage of requests over the last 10 seconds that resulted in
    each type of status code response. For more information, see [Status Code
    Definitions](http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html).
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "status2xx",
                "Status2xx",
                TypeInfo(int),
            ),
            (
                "status3xx",
                "Status3xx",
                TypeInfo(int),
            ),
            (
                "status4xx",
                "Status4xx",
                TypeInfo(int),
            ),
            (
                "status5xx",
                "Status5xx",
                TypeInfo(int),
            ),
        ]

    # The percentage of requests over the last 10 seconds that resulted in a 2xx
    # (200, 201, etc.) status code.
    status2xx: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The percentage of requests over the last 10 seconds that resulted in a 3xx
    # (300, 301, etc.) status code.
    status3xx: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The percentage of requests over the last 10 seconds that resulted in a 4xx
    # (400, 401, etc.) status code.
    status4xx: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The percentage of requests over the last 10 seconds that resulted in a 5xx
    # (500, 501, etc.) status code.
    status5xx: int = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class SwapEnvironmentCNAMEsMessage(ShapeBase):
    """
    Swaps the CNAMEs of two environments.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "source_environment_id",
                "SourceEnvironmentId",
                TypeInfo(str),
            ),
            (
                "source_environment_name",
                "SourceEnvironmentName",
                TypeInfo(str),
            ),
            (
                "destination_environment_id",
                "DestinationEnvironmentId",
                TypeInfo(str),
            ),
            (
                "destination_environment_name",
                "DestinationEnvironmentName",
                TypeInfo(str),
            ),
        ]

    # The ID of the source environment.

    # Condition: You must specify at least the `SourceEnvironmentID` or the
    # `SourceEnvironmentName`. You may also specify both. If you specify the
    # `SourceEnvironmentId`, you must specify the `DestinationEnvironmentId`.
    source_environment_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the source environment.

    # Condition: You must specify at least the `SourceEnvironmentID` or the
    # `SourceEnvironmentName`. You may also specify both. If you specify the
    # `SourceEnvironmentName`, you must specify the `DestinationEnvironmentName`.
    source_environment_name: str = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The ID of the destination environment.

    # Condition: You must specify at least the `DestinationEnvironmentID` or the
    # `DestinationEnvironmentName`. You may also specify both. You must specify
    # the `SourceEnvironmentId` with the `DestinationEnvironmentId`.
    destination_environment_id: str = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The name of the destination environment.

    # Condition: You must specify at least the `DestinationEnvironmentID` or the
    # `DestinationEnvironmentName`. You may also specify both. You must specify
    # the `SourceEnvironmentName` with the `DestinationEnvironmentName`.
    destination_environment_name: str = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


@dataclasses.dataclass
class SystemStatus(ShapeBase):
    """
    CPU utilization and load average metrics for an Amazon EC2 instance.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "cpu_utilization",
                "CPUUtilization",
                TypeInfo(CPUUtilization),
            ),
            (
                "load_average",
                "LoadAverage",
                TypeInfo(typing.List[float]),
            ),
        ]

    # CPU utilization metrics for the instance.
    cpu_utilization: "CPUUtilization" = dataclasses.field(
        default_factory=dict,
    )

    # Load average in the last 1-minute, 5-minute, and 15-minute periods. For
    # more information, see [Operating System
    # Metrics](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/health-
    # enhanced-metrics.html#health-enhanced-metrics-os).
    load_average: typing.List[float] = dataclasses.field(default_factory=list, )


@dataclasses.dataclass
class Tag(ShapeBase):
    """
    Describes a tag applied to a resource in an environment.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "key",
                "Key",
                TypeInfo(str),
            ),
            (
                "value",
                "Value",
                TypeInfo(str),
            ),
        ]

    # The key of the tag.
    key: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The value of the tag.
    value: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class TerminateEnvironmentMessage(ShapeBase):
    """
    Request to terminate an environment.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "environment_id",
                "EnvironmentId",
                TypeInfo(str),
            ),
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
            (
                "terminate_resources",
                "TerminateResources",
                TypeInfo(bool),
            ),
            (
                "force_terminate",
                "ForceTerminate",
                TypeInfo(bool),
            ),
        ]

    # The ID of the environment to terminate.

    # Condition: You must specify either this or an EnvironmentName, or both. If
    # you do not specify either, AWS Elastic Beanstalk returns
    # `MissingRequiredParameter` error.
    environment_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the environment to terminate.

    # Condition: You must specify either this or an EnvironmentId, or both. If
    # you do not specify either, AWS Elastic Beanstalk returns
    # `MissingRequiredParameter` error.
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Indicates whether the associated AWS resources should shut down when the
    # environment is terminated:

    #   * `true`: The specified environment as well as the associated AWS resources, such as Auto Scaling group and LoadBalancer, are terminated.

    #   * `false`: AWS Elastic Beanstalk resource management is removed from the environment, but the AWS resources continue to operate.

    # For more information, see the [ AWS Elastic Beanstalk User Guide.
    # ](http://docs.aws.amazon.com/elasticbeanstalk/latest/ug/)

    # Default: `true`

    # Valid Values: `true` | `false`
    terminate_resources: bool = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Terminates the target environment even if another environment in the same
    # group is dependent on it.
    force_terminate: bool = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class TooManyApplicationVersionsException(ShapeBase):
    """
    The specified account has reached its limit of application versions.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return []


@dataclasses.dataclass
class TooManyApplicationsException(ShapeBase):
    """
    The specified account has reached its limit of applications.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return []


@dataclasses.dataclass
class TooManyBucketsException(ShapeBase):
    """
    The specified account has reached its limit of Amazon S3 buckets.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return []


@dataclasses.dataclass
class TooManyConfigurationTemplatesException(ShapeBase):
    """
    The specified account has reached its limit of configuration templates.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return []


@dataclasses.dataclass
class TooManyEnvironmentsException(ShapeBase):
    """
    The specified account has reached its limit of environments.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return []


@dataclasses.dataclass
class TooManyPlatformsException(ShapeBase):
    """
    You have exceeded the maximum number of allowed platforms associated with the
    account.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return []


@dataclasses.dataclass
class TooManyTagsException(ShapeBase):
    """
    The number of tags in the resource would exceed the number of tags that each
    resource can have.

    To calculate this, the operation considers both the number of tags the resource
    already has and the tags this operation would add if it succeeded.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return []


@dataclasses.dataclass
class Trigger(ShapeBase):
    """
    Describes a trigger.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "name",
                "Name",
                TypeInfo(str),
            ),
        ]

    # The name of the trigger.
    name: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class UpdateApplicationMessage(ShapeBase):
    """
    Request to update an application.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "description",
                "Description",
                TypeInfo(str),
            ),
        ]

    # The name of the application to update. If no such application is found,
    # `UpdateApplication` returns an `InvalidParameterValue` error.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A new description for the application.

    # Default: If not specified, AWS Elastic Beanstalk does not update the
    # description.
    description: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class UpdateApplicationResourceLifecycleMessage(ShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "resource_lifecycle_config",
                "ResourceLifecycleConfig",
                TypeInfo(ApplicationResourceLifecycleConfig),
            ),
        ]

    # The name of the application.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The lifecycle configuration.
    resource_lifecycle_config: "ApplicationResourceLifecycleConfig" = dataclasses.field(
        default_factory=dict,
    )


@dataclasses.dataclass
class UpdateApplicationVersionMessage(ShapeBase):
    """

    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "version_label",
                "VersionLabel",
                TypeInfo(str),
            ),
            (
                "description",
                "Description",
                TypeInfo(str),
            ),
        ]

    # The name of the application associated with this version.

    # If no application is found with this name, `UpdateApplication` returns an
    # `InvalidParameterValue` error.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the version to update.

    # If no application version is found with this label, `UpdateApplication`
    # returns an `InvalidParameterValue` error.
    version_label: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A new description for this version.
    description: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class UpdateConfigurationTemplateMessage(ShapeBase):
    """
    The result message containing the options for the specified solution stack.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "template_name",
                "TemplateName",
                TypeInfo(str),
            ),
            (
                "description",
                "Description",
                TypeInfo(str),
            ),
            (
                "option_settings",
                "OptionSettings",
                TypeInfo(typing.List[ConfigurationOptionSetting]),
            ),
            (
                "options_to_remove",
                "OptionsToRemove",
                TypeInfo(typing.List[OptionSpecification]),
            ),
        ]

    # The name of the application associated with the configuration template to
    # update.

    # If no application is found with this name, `UpdateConfigurationTemplate`
    # returns an `InvalidParameterValue` error.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the configuration template to update.

    # If no configuration template is found with this name,
    # `UpdateConfigurationTemplate` returns an `InvalidParameterValue` error.
    template_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A new description for the configuration.
    description: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A list of configuration option settings to update with the new specified
    # option value.
    option_settings: typing.List["ConfigurationOptionSetting"
                                ] = dataclasses.field(
                                    default_factory=list,
                                )

    # A list of configuration options to remove from the configuration set.

    # Constraint: You can remove only `UserDefined` configuration options.
    options_to_remove: typing.List["OptionSpecification"] = dataclasses.field(
        default_factory=list,
    )


@dataclasses.dataclass
class UpdateEnvironmentMessage(ShapeBase):
    """
    Request to update an environment.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "environment_id",
                "EnvironmentId",
                TypeInfo(str),
            ),
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
            (
                "group_name",
                "GroupName",
                TypeInfo(str),
            ),
            (
                "description",
                "Description",
                TypeInfo(str),
            ),
            (
                "tier",
                "Tier",
                TypeInfo(EnvironmentTier),
            ),
            (
                "version_label",
                "VersionLabel",
                TypeInfo(str),
            ),
            (
                "template_name",
                "TemplateName",
                TypeInfo(str),
            ),
            (
                "solution_stack_name",
                "SolutionStackName",
                TypeInfo(str),
            ),
            (
                "platform_arn",
                "PlatformArn",
                TypeInfo(str),
            ),
            (
                "option_settings",
                "OptionSettings",
                TypeInfo(typing.List[ConfigurationOptionSetting]),
            ),
            (
                "options_to_remove",
                "OptionsToRemove",
                TypeInfo(typing.List[OptionSpecification]),
            ),
        ]

    # The name of the application with which the environment is associated.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The ID of the environment to update.

    # If no environment with this ID exists, AWS Elastic Beanstalk returns an
    # `InvalidParameterValue` error.

    # Condition: You must specify either this or an EnvironmentName, or both. If
    # you do not specify either, AWS Elastic Beanstalk returns
    # `MissingRequiredParameter` error.
    environment_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the environment to update. If no environment with this name
    # exists, AWS Elastic Beanstalk returns an `InvalidParameterValue` error.

    # Condition: You must specify either this or an EnvironmentId, or both. If
    # you do not specify either, AWS Elastic Beanstalk returns
    # `MissingRequiredParameter` error.
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the group to which the target environment belongs. Specify a
    # group name only if the environment's name is specified in an environment
    # manifest and not with the environment name or environment ID parameters.
    # See [Environment Manifest
    # (env.yaml)](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environment-
    # cfg-manifest.html) for details.
    group_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If this parameter is specified, AWS Elastic Beanstalk updates the
    # description of this environment.
    description: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # This specifies the tier to use to update the environment.

    # Condition: At this time, if you change the tier version, name, or type, AWS
    # Elastic Beanstalk returns `InvalidParameterValue` error.
    tier: "EnvironmentTier" = dataclasses.field(default_factory=dict, )

    # If this parameter is specified, AWS Elastic Beanstalk deploys the named
    # application version to the environment. If no such application version is
    # found, returns an `InvalidParameterValue` error.
    version_label: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If this parameter is specified, AWS Elastic Beanstalk deploys this
    # configuration template to the environment. If no such configuration
    # template is found, AWS Elastic Beanstalk returns an `InvalidParameterValue`
    # error.
    template_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # This specifies the platform version that the environment will run after the
    # environment is updated.
    solution_stack_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The ARN of the platform, if used.
    platform_arn: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If specified, AWS Elastic Beanstalk updates the configuration set
    # associated with the running environment and sets the specified
    # configuration options to the requested value.
    option_settings: typing.List["ConfigurationOptionSetting"
                                ] = dataclasses.field(
                                    default_factory=list,
                                )

    # A list of custom user-defined configuration options to remove from the
    # configuration set for this environment.
    options_to_remove: typing.List["OptionSpecification"] = dataclasses.field(
        default_factory=list,
    )


@dataclasses.dataclass
class UpdateTagsForResourceMessage(ShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "resource_arn",
                "ResourceArn",
                TypeInfo(str),
            ),
            (
                "tags_to_add",
                "TagsToAdd",
                TypeInfo(typing.List[Tag]),
            ),
            (
                "tags_to_remove",
                "TagsToRemove",
                TypeInfo(typing.List[str]),
            ),
        ]

    # The Amazon Resource Name (ARN) of the resouce to be updated.

    # Must be the ARN of an Elastic Beanstalk environment.
    resource_arn: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A list of tags to add or update.

    # If a key of an existing tag is added, the tag's value is updated.
    tags_to_add: typing.List["Tag"] = dataclasses.field(default_factory=list, )

    # A list of tag keys to remove.

    # If a tag key doesn't exist, it is silently ignored.
    tags_to_remove: typing.List[str] = dataclasses.field(default_factory=list, )


@dataclasses.dataclass
class ValidateConfigurationSettingsMessage(ShapeBase):
    """
    A list of validation messages for a specified configuration template.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "application_name",
                "ApplicationName",
                TypeInfo(str),
            ),
            (
                "option_settings",
                "OptionSettings",
                TypeInfo(typing.List[ConfigurationOptionSetting]),
            ),
            (
                "template_name",
                "TemplateName",
                TypeInfo(str),
            ),
            (
                "environment_name",
                "EnvironmentName",
                TypeInfo(str),
            ),
        ]

    # The name of the application that the configuration template or environment
    # belongs to.
    application_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A list of the options and desired values to evaluate.
    option_settings: typing.List["ConfigurationOptionSetting"
                                ] = dataclasses.field(
                                    default_factory=list,
                                )

    # The name of the configuration template to validate the settings against.

    # Condition: You cannot specify both this and an environment name.
    template_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the environment to validate the settings against.

    # Condition: You cannot specify both this and a configuration template name.
    environment_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ValidationMessage(ShapeBase):
    """
    An error or warning for a desired configuration option value.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "message",
                "Message",
                TypeInfo(str),
            ),
            (
                "severity",
                "Severity",
                TypeInfo(ValidationSeverity),
            ),
            (
                "namespace",
                "Namespace",
                TypeInfo(str),
            ),
            (
                "option_name",
                "OptionName",
                TypeInfo(str),
            ),
        ]

    # A message describing the error or warning.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # An indication of the severity of this message:

    #   * `error`: This message indicates that this is not a valid setting for an option.

    #   * `warning`: This message is providing information you should take into account.
    severity: "ValidationSeverity" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The namespace to which the option belongs.
    namespace: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the option.
    option_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )


class ValidationSeverity(Enum):
    error = "error"
    warning = "warning"
