import datetime
import typing
from autoboto import ShapeBase, OutputShapeBase, TypeInfo
from enum import Enum
import dataclasses


@dataclasses.dataclass
class AccountLimit(ShapeBase):
    """
    A complex type that contains the type of limit that you specified in the request
    and the current value for that limit.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "type",
                "Type",
                TypeInfo(AccountLimitType),
            ),
            (
                "value",
                "Value",
                TypeInfo(int),
            ),
        ]

    # The limit that you requested. Valid values include the following:

    #   * **MAX_HEALTH_CHECKS_BY_OWNER** : The maximum number of health checks that you can create using the current account.

    #   * **MAX_HOSTED_ZONES_BY_OWNER** : The maximum number of hosted zones that you can create using the current account.

    #   * **MAX_REUSABLE_DELEGATION_SETS_BY_OWNER** : The maximum number of reusable delegation sets that you can create using the current account.

    #   * **MAX_TRAFFIC_POLICIES_BY_OWNER** : The maximum number of traffic policies that you can create using the current account.

    #   * **MAX_TRAFFIC_POLICY_INSTANCES_BY_OWNER** : The maximum number of traffic policy instances that you can create using the current account. (Traffic policy instances are referred to as traffic flow policy records in the Amazon Route 53 console.)
    type: "AccountLimitType" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The current value for the limit that is specified by AccountLimit$Type.
    value: int = dataclasses.field(default=ShapeBase.NOT_SET, )


class AccountLimitType(Enum):
    MAX_HEALTH_CHECKS_BY_OWNER = "MAX_HEALTH_CHECKS_BY_OWNER"
    MAX_HOSTED_ZONES_BY_OWNER = "MAX_HOSTED_ZONES_BY_OWNER"
    MAX_TRAFFIC_POLICY_INSTANCES_BY_OWNER = "MAX_TRAFFIC_POLICY_INSTANCES_BY_OWNER"
    MAX_REUSABLE_DELEGATION_SETS_BY_OWNER = "MAX_REUSABLE_DELEGATION_SETS_BY_OWNER"
    MAX_TRAFFIC_POLICIES_BY_OWNER = "MAX_TRAFFIC_POLICIES_BY_OWNER"


@dataclasses.dataclass
class AlarmIdentifier(ShapeBase):
    """
    A complex type that identifies the CloudWatch alarm that you want Amazon Route
    53 health checkers to use to determine whether this health check is healthy.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "region",
                "Region",
                TypeInfo(CloudWatchRegion),
            ),
            (
                "name",
                "Name",
                TypeInfo(str),
            ),
        ]

    # A complex type that identifies the CloudWatch alarm that you want Amazon
    # Route 53 health checkers to use to determine whether this health check is
    # healthy.

    # For the current list of CloudWatch regions, see [Amazon
    # CloudWatch](http://docs.aws.amazon.com/general/latest/gr/rande.html#cw_region)
    # in the _AWS Regions and Endpoints_ chapter of the _Amazon Web Services
    # General Reference_.
    region: "CloudWatchRegion" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the CloudWatch alarm that you want Amazon Route 53 health
    # checkers to use to determine whether this health check is healthy.
    name: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class AliasTarget(ShapeBase):
    """
    _Alias resource record sets only:_ Information about the CloudFront
    distribution, Elastic Beanstalk environment, ELB load balancer, Amazon S3
    bucket, or Amazon Route 53 resource record set that you're redirecting queries
    to. An Elastic Beanstalk environment must have a regionalized subdomain.

    When creating resource record sets for a private hosted zone, note the
    following:

      * Resource record sets can't be created for CloudFront distributions in a private hosted zone.

      * Creating geolocation alias resource record sets or latency alias resource record sets in a private hosted zone is unsupported.

      * For information about creating failover resource record sets in a private hosted zone, see [Configuring Failover in a Private Hosted Zone](http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-private-hosted-zones.html).
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "hosted_zone_id",
                "HostedZoneId",
                TypeInfo(str),
            ),
            (
                "dns_name",
                "DNSName",
                TypeInfo(str),
            ),
            (
                "evaluate_target_health",
                "EvaluateTargetHealth",
                TypeInfo(bool),
            ),
        ]

    # _Alias resource records sets only_ : The value used depends on where you
    # want to route traffic:

    # CloudFront distribution

    # Specify `Z2FDTNDATAQYW2`.

    # Alias resource record sets for CloudFront can't be created in a private
    # zone.

    # Elastic Beanstalk environment

    # Specify the hosted zone ID for the region in which you created the
    # environment. The environment must have a regionalized subdomain. For a list
    # of regions and the corresponding hosted zone IDs, see [AWS Elastic
    # Beanstalk](http://docs.aws.amazon.com/general/latest/gr/rande.html#elasticbeanstalk_region)
    # in the "AWS Regions and Endpoints" chapter of the _Amazon Web Services
    # General Reference_.

    # ELB load balancer

    # Specify the value of the hosted zone ID for the load balancer. Use the
    # following methods to get the hosted zone ID:

    #   * [Elastic Load Balancing](http://docs.aws.amazon.com/general/latest/gr/rande.html#elb_region) table in the "AWS Regions and Endpoints" chapter of the _Amazon Web Services General Reference_ : Use the value that corresponds with the region that you created your load balancer in. Note that there are separate columns for Application and Classic Load Balancers and for Network Load Balancers.

    #   * **AWS Management Console** : Go to the Amazon EC2 page, choose **Load Balancers** in the navigation pane, select the load balancer, and get the value of the **Hosted zone** field on the **Description** tab.

    #   * **Elastic Load Balancing API** : Use `DescribeLoadBalancers` to get the applicable value. For more information, see the applicable guide:

    #     * Classic Load Balancers: Use [DescribeLoadBalancers](http://docs.aws.amazon.com/elasticloadbalancing/2012-06-01/APIReference/API_DescribeLoadBalancers.html) to get the value of `CanonicalHostedZoneNameId`.

    #     * Application and Network Load Balancers: Use [DescribeLoadBalancers](http://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeLoadBalancers.html) to get the value of `CanonicalHostedZoneId`.

    #   * **AWS CLI** : Use `describe-load-balancers` to get the applicable value. For more information, see the applicable guide:

    #     * Classic Load Balancers: Use [describe-load-balancers](http://docs.aws.amazon.com/cli/latest/reference/elb/describe-load-balancers.html) to get the value of `CanonicalHostedZoneNameId`.

    #     * Application and Network Load Balancers: Use [describe-load-balancers](http://docs.aws.amazon.com/cli/latest/reference/elbv2/describe-load-balancers.html) to get the value of `CanonicalHostedZoneId`.

    # An Amazon S3 bucket configured as a static website

    # Specify the hosted zone ID for the region that you created the bucket in.
    # For more information about valid values, see the [Amazon Simple Storage
    # Service Website
    # Endpoints](http://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region)
    # table in the "AWS Regions and Endpoints" chapter of the _Amazon Web
    # Services General Reference_.

    # Another Amazon Route 53 resource record set in your hosted zone

    # Specify the hosted zone ID of your hosted zone. (An alias resource record
    # set can't reference a resource record set in a different hosted zone.)
    hosted_zone_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # _Alias resource record sets only:_ The value that you specify depends on
    # where you want to route queries:

    # CloudFront distribution

    # Specify the domain name that CloudFront assigned when you created your
    # distribution.

    # Your CloudFront distribution must include an alternate domain name that
    # matches the name of the resource record set. For example, if the name of
    # the resource record set is _acme.example.com_ , your CloudFront
    # distribution must include _acme.example.com_ as one of the alternate domain
    # names. For more information, see [Using Alternate Domain Names
    # (CNAMEs)](http://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/CNAMEs.html)
    # in the _Amazon CloudFront Developer Guide_.

    # Elastic Beanstalk environment

    # Specify the `CNAME` attribute for the environment. (The environment must
    # have a regionalized domain name.) You can use the following methods to get
    # the value of the CNAME attribute:

    #   * _AWS Management Console_ : For information about how to get the value by using the console, see [Using Custom Domains with AWS Elastic Beanstalk](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/customdomains.html) in the _AWS Elastic Beanstalk Developer Guide_.

    #   * _Elastic Beanstalk API_ : Use the `DescribeEnvironments` action to get the value of the `CNAME` attribute. For more information, see [DescribeEnvironments](http://docs.aws.amazon.com/elasticbeanstalk/latest/api/API_DescribeEnvironments.html) in the _AWS Elastic Beanstalk API Reference_.

    #   * _AWS CLI_ : Use the `describe-environments` command to get the value of the `CNAME` attribute. For more information, see [describe-environments](http://docs.aws.amazon.com/cli/latest/reference/elasticbeanstalk/describe-environments.html) in the _AWS Command Line Interface Reference_.

    # ELB load balancer

    # Specify the DNS name that is associated with the load balancer. Get the DNS
    # name by using the AWS Management Console, the ELB API, or the AWS CLI.

    #   * **AWS Management Console** : Go to the EC2 page, choose **Load Balancers** in the navigation pane, choose the load balancer, choose the **Description** tab, and get the value of the **DNS name** field. (If you're routing traffic to a Classic Load Balancer, get the value that begins with **dualstack**.)

    #   * **Elastic Load Balancing API** : Use `DescribeLoadBalancers` to get the value of `DNSName`. For more information, see the applicable guide:

    #     * Classic Load Balancers: [DescribeLoadBalancers](http://docs.aws.amazon.com/elasticloadbalancing/2012-06-01/APIReference/API_DescribeLoadBalancers.html)

    #     * Application and Network Load Balancers: [DescribeLoadBalancers](http://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_DescribeLoadBalancers.html)

    #   * **AWS CLI** : Use `describe-load-balancers` to get the value of `DNSName`. For more information, see the applicable guide:

    #     * Classic Load Balancers: [describe-load-balancers](http://docs.aws.amazon.com/cli/latest/reference/elb/describe-load-balancers.html)

    #     * Application and Network Load Balancers: [describe-load-balancers](http://docs.aws.amazon.com/cli/latest/reference/elbv2/describe-load-balancers.html)

    # Amazon S3 bucket that is configured as a static website

    # Specify the domain name of the Amazon S3 website endpoint in which you
    # created the bucket, for example, `s3-website-us-east-2.amazonaws.com`. For
    # more information about valid values, see the table [Amazon Simple Storage
    # Service (S3) Website
    # Endpoints](http://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region)
    # in the _Amazon Web Services General Reference_. For more information about
    # using S3 buckets for websites, see [Getting Started with Amazon Route
    # 53](http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/getting-
    # started.html) in the _Amazon Route 53 Developer Guide._

    # Another Amazon Route 53 resource record set

    # Specify the value of the `Name` element for a resource record set in the
    # current hosted zone.
    dns_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # _Applies only to alias, failover alias, geolocation alias, latency alias,
    # and weighted alias resource record sets:_ When `EvaluateTargetHealth` is
    # `true`, an alias resource record set inherits the health of the referenced
    # AWS resource, such as an ELB load balancer, or the referenced resource
    # record set.

    # Note the following:

    #   * You can't set `EvaluateTargetHealth` to `true` when the alias target is a CloudFront distribution.

    #   * If the AWS resource that you specify in `AliasTarget` is a resource record set or a group of resource record sets (for example, a group of weighted resource record sets), but it is not another alias resource record set, we recommend that you associate a health check with all of the resource record sets in the alias target. For more information, see [What Happens When You Omit Health Checks?](http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-complex-configs.html#dns-failover-complex-configs-hc-omitting) in the _Amazon Route 53 Developer Guide_.

    #   * If you specify an Elastic Beanstalk environment in `HostedZoneId` and `DNSName`, and if the environment contains an ELB load balancer, Elastic Load Balancing routes queries only to the healthy Amazon EC2 instances that are registered with the load balancer. (An environment automatically contains an ELB load balancer if it includes more than one EC2 instance.) If you set `EvaluateTargetHealth` to `true` and either no EC2 instances are healthy or the load balancer itself is unhealthy, Amazon Route 53 routes queries to other available resources that are healthy, if any.

    # If the environment contains a single EC2 instance, there are no special
    # requirements.

    #   * If you specify an ELB load balancer in ` AliasTarget `, ELB routes queries only to the healthy EC2 instances that are registered with the load balancer. If no EC2 instances are healthy or if the load balancer itself is unhealthy, and if `EvaluateTargetHealth` is true for the corresponding alias resource record set, Amazon Route 53 routes queries to other resources. When you create a load balancer, you configure settings for ELB health checks; they're not Amazon Route 53 health checks, but they perform a similar function. Do not create Amazon Route 53 health checks for the EC2 instances that you register with an ELB load balancer.

    # For more information, see [How Health Checks Work in More Complex Amazon
    # Route 53
    # Configurations](http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-
    # failover-complex-configs.html) in the _Amazon Route 53 Developer Guide_.

    #   * We recommend that you set `EvaluateTargetHealth` to true only when you have enough idle capacity to handle the failure of one or more endpoints.

    # For more information and examples, see [Amazon Route 53 Health Checks and
    # DNS Failover](http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-
    # failover.html) in the _Amazon Route 53 Developer Guide_.
    evaluate_target_health: bool = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


@dataclasses.dataclass
class AssociateVPCWithHostedZoneRequest(ShapeBase):
    """
    A complex type that contains information about the request to associate a VPC
    with a private hosted zone.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "hosted_zone_id",
                "HostedZoneId",
                TypeInfo(str),
            ),
            (
                "vpc",
                "VPC",
                TypeInfo(VPC),
            ),
            (
                "comment",
                "Comment",
                TypeInfo(str),
            ),
        ]

    # The ID of the private hosted zone that you want to associate an Amazon VPC
    # with.

    # Note that you can't associate a VPC with a hosted zone that doesn't have an
    # existing VPC association.
    hosted_zone_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A complex type that contains information about the VPC that you want to
    # associate with a private hosted zone.
    vpc: "VPC" = dataclasses.field(default_factory=dict, )

    # _Optional:_ A comment about the association request.
    comment: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class AssociateVPCWithHostedZoneResponse(OutputShapeBase):
    """
    A complex type that contains the response information for the
    `AssociateVPCWithHostedZone` request.
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
                "change_info",
                "ChangeInfo",
                TypeInfo(ChangeInfo),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that describes the changes made to your hosted zone.
    change_info: "ChangeInfo" = dataclasses.field(default_factory=dict, )


@dataclasses.dataclass
class Change(ShapeBase):
    """
    The information for each resource record set that you want to change.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "action",
                "Action",
                TypeInfo(ChangeAction),
            ),
            (
                "resource_record_set",
                "ResourceRecordSet",
                TypeInfo(ResourceRecordSet),
            ),
        ]

    # The action to perform:

    #   * `CREATE`: Creates a resource record set that has the specified values.

    #   * `DELETE`: Deletes a existing resource record set.

    # To delete the resource record set that is associated with a traffic policy
    # instance, use ` DeleteTrafficPolicyInstance `. Amazon Route 53 will delete
    # the resource record set automatically. If you delete the resource record
    # set by using `ChangeResourceRecordSets`, Amazon Route 53 doesn't
    # automatically delete the traffic policy instance, and you'll continue to be
    # charged for it even though it's no longer in use.

    #   * `UPSERT`: If a resource record set doesn't already exist, Amazon Route 53 creates it. If a resource record set does exist, Amazon Route 53 updates it with the values in the request.
    action: "ChangeAction" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Information about the resource record set to create, delete, or update.
    resource_record_set: "ResourceRecordSet" = dataclasses.field(
        default_factory=dict,
    )


class ChangeAction(Enum):
    CREATE = "CREATE"
    DELETE = "DELETE"
    UPSERT = "UPSERT"


@dataclasses.dataclass
class ChangeBatch(ShapeBase):
    """
    The information for a change request.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "changes",
                "Changes",
                TypeInfo(typing.List[Change]),
            ),
            (
                "comment",
                "Comment",
                TypeInfo(str),
            ),
        ]

    # Information about the changes to make to the record sets.
    changes: typing.List["Change"] = dataclasses.field(default_factory=list, )

    # _Optional:_ Any comments you want to include about a change batch request.
    comment: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ChangeInfo(ShapeBase):
    """
    A complex type that describes change information about changes made to your
    hosted zone.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "id",
                "Id",
                TypeInfo(str),
            ),
            (
                "status",
                "Status",
                TypeInfo(ChangeStatus),
            ),
            (
                "submitted_at",
                "SubmittedAt",
                TypeInfo(datetime.datetime),
            ),
            (
                "comment",
                "Comment",
                TypeInfo(str),
            ),
        ]

    # The ID of the request.
    id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The current state of the request. `PENDING` indicates that this request has
    # not yet been applied to all Amazon Route 53 DNS servers.
    status: "ChangeStatus" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The date and time that the change request was submitted in [ISO 8601
    # format](https://en.wikipedia.org/wiki/ISO_8601) and Coordinated Universal
    # Time (UTC). For example, the value `2017-03-27T17:48:16.751Z` represents
    # March 27, 2017 at 17:48:16.751 UTC.
    submitted_at: datetime.datetime = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that describes change information about changes made to your
    # hosted zone.

    # This element contains an ID that you use when performing a GetChange action
    # to get detailed information about the change.
    comment: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ChangeResourceRecordSetsRequest(ShapeBase):
    """
    A complex type that contains change information for the resource record set.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "hosted_zone_id",
                "HostedZoneId",
                TypeInfo(str),
            ),
            (
                "change_batch",
                "ChangeBatch",
                TypeInfo(ChangeBatch),
            ),
        ]

    # The ID of the hosted zone that contains the resource record sets that you
    # want to change.
    hosted_zone_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A complex type that contains an optional comment and the `Changes` element.
    change_batch: "ChangeBatch" = dataclasses.field(default_factory=dict, )


@dataclasses.dataclass
class ChangeResourceRecordSetsResponse(OutputShapeBase):
    """
    A complex type containing the response for the request.
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
                "change_info",
                "ChangeInfo",
                TypeInfo(ChangeInfo),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains information about changes made to your hosted
    # zone.

    # This element contains an ID that you use when performing a GetChange action
    # to get detailed information about the change.
    change_info: "ChangeInfo" = dataclasses.field(default_factory=dict, )


class ChangeStatus(Enum):
    PENDING = "PENDING"
    INSYNC = "INSYNC"


@dataclasses.dataclass
class ChangeTagsForResourceRequest(ShapeBase):
    """
    A complex type that contains information about the tags that you want to add,
    edit, or delete.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "resource_type",
                "ResourceType",
                TypeInfo(TagResourceType),
            ),
            (
                "resource_id",
                "ResourceId",
                TypeInfo(str),
            ),
            (
                "add_tags",
                "AddTags",
                TypeInfo(typing.List[Tag]),
            ),
            (
                "remove_tag_keys",
                "RemoveTagKeys",
                TypeInfo(typing.List[str]),
            ),
        ]

    # The type of the resource.

    #   * The resource type for health checks is `healthcheck`.

    #   * The resource type for hosted zones is `hostedzone`.
    resource_type: "TagResourceType" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The ID of the resource for which you want to add, change, or delete tags.
    resource_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A complex type that contains a list of the tags that you want to add to the
    # specified health check or hosted zone and/or the tags that you want to edit
    # `Value` for.

    # You can add a maximum of 10 tags to a health check or a hosted zone.
    add_tags: typing.List["Tag"] = dataclasses.field(default_factory=list, )

    # A complex type that contains a list of the tags that you want to delete
    # from the specified health check or hosted zone. You can specify up to 10
    # keys.
    remove_tag_keys: typing.List[str] = dataclasses.field(
        default_factory=list,
    )


@dataclasses.dataclass
class ChangeTagsForResourceResponse(OutputShapeBase):
    """
    Empty response for the request.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


@dataclasses.dataclass
class CloudWatchAlarmConfiguration(ShapeBase):
    """
    A complex type that contains information about the CloudWatch alarm that Amazon
    Route 53 is monitoring for this health check.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "evaluation_periods",
                "EvaluationPeriods",
                TypeInfo(int),
            ),
            (
                "threshold",
                "Threshold",
                TypeInfo(float),
            ),
            (
                "comparison_operator",
                "ComparisonOperator",
                TypeInfo(ComparisonOperator),
            ),
            (
                "period",
                "Period",
                TypeInfo(int),
            ),
            (
                "metric_name",
                "MetricName",
                TypeInfo(str),
            ),
            (
                "namespace",
                "Namespace",
                TypeInfo(str),
            ),
            (
                "statistic",
                "Statistic",
                TypeInfo(Statistic),
            ),
            (
                "dimensions",
                "Dimensions",
                TypeInfo(typing.List[Dimension]),
            ),
        ]

    # For the metric that the CloudWatch alarm is associated with, the number of
    # periods that the metric is compared to the threshold.
    evaluation_periods: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # For the metric that the CloudWatch alarm is associated with, the value the
    # metric is compared with.
    threshold: float = dataclasses.field(default=ShapeBase.NOT_SET, )

    # For the metric that the CloudWatch alarm is associated with, the arithmetic
    # operation that is used for the comparison.
    comparison_operator: "ComparisonOperator" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # For the metric that the CloudWatch alarm is associated with, the duration
    # of one evaluation period in seconds.
    period: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the CloudWatch metric that the alarm is associated with.
    metric_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The namespace of the metric that the alarm is associated with. For more
    # information, see [Amazon CloudWatch Namespaces, Dimensions, and Metrics
    # Reference](http://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/CW_Support_For_AWS.html)
    # in the _Amazon CloudWatch User Guide_.
    namespace: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # For the metric that the CloudWatch alarm is associated with, the statistic
    # that is applied to the metric.
    statistic: "Statistic" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # For the metric that the CloudWatch alarm is associated with, a complex type
    # that contains information about the dimensions for the metric. For
    # information, see [Amazon CloudWatch Namespaces, Dimensions, and Metrics
    # Reference](http://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/CW_Support_For_AWS.html)
    # in the _Amazon CloudWatch User Guide_.
    dimensions: typing.List["Dimension"] = dataclasses.field(
        default_factory=list,
    )


class CloudWatchRegion(Enum):
    us_east_1 = "us-east-1"
    us_east_2 = "us-east-2"
    us_west_1 = "us-west-1"
    us_west_2 = "us-west-2"
    ca_central_1 = "ca-central-1"
    eu_central_1 = "eu-central-1"
    eu_west_1 = "eu-west-1"
    eu_west_2 = "eu-west-2"
    eu_west_3 = "eu-west-3"
    ap_south_1 = "ap-south-1"
    ap_southeast_1 = "ap-southeast-1"
    ap_southeast_2 = "ap-southeast-2"
    ap_northeast_1 = "ap-northeast-1"
    ap_northeast_2 = "ap-northeast-2"
    ap_northeast_3 = "ap-northeast-3"
    sa_east_1 = "sa-east-1"


class ComparisonOperator(Enum):
    GreaterThanOrEqualToThreshold = "GreaterThanOrEqualToThreshold"
    GreaterThanThreshold = "GreaterThanThreshold"
    LessThanThreshold = "LessThanThreshold"
    LessThanOrEqualToThreshold = "LessThanOrEqualToThreshold"


@dataclasses.dataclass
class ConcurrentModification(ShapeBase):
    """
    Another user submitted a request to create, update, or delete the object at the
    same time that you did. Retry the request.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ConflictingDomainExists(ShapeBase):
    """
    The cause of this error depends on whether you're trying to create a public or a
    private hosted zone:

      * **Public hosted zone:** Two hosted zones that have the same name or that have a parent/child relationship (example.com and test.example.com) can't have any common name servers. You tried to create a hosted zone that has the same name as an existing hosted zone or that's the parent or child of an existing hosted zone, and you specified a delegation set that shares one or more name servers with the existing hosted zone. For more information, see CreateReusableDelegationSet.

      * **Private hosted zone:** You specified an Amazon VPC that you're already using for another hosted zone, and the domain that you specified for one of the hosted zones is a subdomain of the domain that you specified for the other hosted zone. For example, you can't use the same Amazon VPC for the hosted zones for example.com and test.example.com.
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

    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ConflictingTypes(ShapeBase):
    """
    You tried to update a traffic policy instance by using a traffic policy version
    that has a different DNS type than the current type for the instance. You
    specified the type in the JSON document in the `CreateTrafficPolicy` or
    `CreateTrafficPolicyVersion`request.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class CreateHealthCheckRequest(ShapeBase):
    """
    A complex type that contains the health check request information.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "caller_reference",
                "CallerReference",
                TypeInfo(str),
            ),
            (
                "health_check_config",
                "HealthCheckConfig",
                TypeInfo(HealthCheckConfig),
            ),
        ]

    # A unique string that identifies the request and that allows you to retry a
    # failed `CreateHealthCheck` request without the risk of creating two
    # identical health checks:

    #   * If you send a `CreateHealthCheck` request with the same `CallerReference` and settings as a previous request, and if the health check doesn't exist, Amazon Route 53 creates the health check. If the health check does exist, Amazon Route 53 returns the settings for the existing health check.

    #   * If you send a `CreateHealthCheck` request with the same `CallerReference` as a deleted health check, regardless of the settings, Amazon Route 53 returns a `HealthCheckAlreadyExists` error.

    #   * If you send a `CreateHealthCheck` request with the same `CallerReference` as an existing health check but with different settings, Amazon Route 53 returns a `HealthCheckAlreadyExists` error.

    #   * If you send a `CreateHealthCheck` request with a unique `CallerReference` but settings identical to an existing health check, Amazon Route 53 creates the health check.
    caller_reference: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A complex type that contains the response to a `CreateHealthCheck` request.
    health_check_config: "HealthCheckConfig" = dataclasses.field(
        default_factory=dict,
    )


@dataclasses.dataclass
class CreateHealthCheckResponse(OutputShapeBase):
    """
    A complex type containing the response information for the new health check.
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
                "health_check",
                "HealthCheck",
                TypeInfo(HealthCheck),
            ),
            (
                "location",
                "Location",
                TypeInfo(str),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains identifying information about the health
    # check.
    health_check: "HealthCheck" = dataclasses.field(default_factory=dict, )

    # The unique URL representing the new health check.
    location: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class CreateHostedZoneRequest(ShapeBase):
    """
    A complex type that contains information about the request to create a hosted
    zone.
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
                "caller_reference",
                "CallerReference",
                TypeInfo(str),
            ),
            (
                "vpc",
                "VPC",
                TypeInfo(VPC),
            ),
            (
                "hosted_zone_config",
                "HostedZoneConfig",
                TypeInfo(HostedZoneConfig),
            ),
            (
                "delegation_set_id",
                "DelegationSetId",
                TypeInfo(str),
            ),
        ]

    # The name of the domain. For resource record types that include a domain
    # name, specify a fully qualified domain name, for example,
    # _www.example.com_. The trailing dot is optional; Amazon Route 53 assumes
    # that the domain name is fully qualified. This means that Amazon Route 53
    # treats _www.example.com_ (without a trailing dot) and _www.example.com._
    # (with a trailing dot) as identical.

    # If you're creating a public hosted zone, this is the name you have
    # registered with your DNS registrar. If your domain name is registered with
    # a registrar other than Amazon Route 53, change the name servers for your
    # domain to the set of `NameServers` that `CreateHostedZone` returns in
    # `DelegationSet`.
    name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A unique string that identifies the request and that allows failed
    # `CreateHostedZone` requests to be retried without the risk of executing the
    # operation twice. You must use a unique `CallerReference` string every time
    # you submit a `CreateHostedZone` request. `CallerReference` can be any
    # unique string, for example, a date/time stamp.
    caller_reference: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # (Private hosted zones only) A complex type that contains information about
    # the Amazon VPC that you're associating with this hosted zone.

    # You can specify only one Amazon VPC when you create a private hosted zone.
    # To associate additional Amazon VPCs with the hosted zone, use
    # AssociateVPCWithHostedZone after you create a hosted zone.
    vpc: "VPC" = dataclasses.field(default_factory=dict, )

    # (Optional) A complex type that contains the following optional values:

    #   * For public and private hosted zones, an optional comment

    #   * For private hosted zones, an optional `PrivateZone` element

    # If you don't specify a comment or the `PrivateZone` element, omit
    # `HostedZoneConfig` and the other elements.
    hosted_zone_config: "HostedZoneConfig" = dataclasses.field(
        default_factory=dict,
    )

    # If you want to associate a reusable delegation set with this hosted zone,
    # the ID that Amazon Route 53 assigned to the reusable delegation set when
    # you created it. For more information about reusable delegation sets, see
    # CreateReusableDelegationSet.
    delegation_set_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class CreateHostedZoneResponse(OutputShapeBase):
    """
    A complex type containing the response information for the hosted zone.
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
                "hosted_zone",
                "HostedZone",
                TypeInfo(HostedZone),
            ),
            (
                "change_info",
                "ChangeInfo",
                TypeInfo(ChangeInfo),
            ),
            (
                "delegation_set",
                "DelegationSet",
                TypeInfo(DelegationSet),
            ),
            (
                "location",
                "Location",
                TypeInfo(str),
            ),
            (
                "vpc",
                "VPC",
                TypeInfo(VPC),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains general information about the hosted zone.
    hosted_zone: "HostedZone" = dataclasses.field(default_factory=dict, )

    # A complex type that contains information about the `CreateHostedZone`
    # request.
    change_info: "ChangeInfo" = dataclasses.field(default_factory=dict, )

    # A complex type that describes the name servers for this hosted zone.
    delegation_set: "DelegationSet" = dataclasses.field(default_factory=dict, )

    # The unique URL representing the new hosted zone.
    location: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A complex type that contains information about an Amazon VPC that you
    # associated with this hosted zone.
    vpc: "VPC" = dataclasses.field(default_factory=dict, )


@dataclasses.dataclass
class CreateQueryLoggingConfigRequest(ShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "hosted_zone_id",
                "HostedZoneId",
                TypeInfo(str),
            ),
            (
                "cloud_watch_logs_log_group_arn",
                "CloudWatchLogsLogGroupArn",
                TypeInfo(str),
            ),
        ]

    # The ID of the hosted zone that you want to log queries for. You can log
    # queries only for public hosted zones.
    hosted_zone_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The Amazon Resource Name (ARN) for the log group that you want to Amazon
    # Route 53 to send query logs to. This is the format of the ARN:

    # arn:aws:logs: _region_ : _account-id_ :log-group: _log_group_name_

    # To get the ARN for a log group, you can use the CloudWatch console, the
    # [DescribeLogGroups](http://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_DescribeLogGroups.html)
    # API action, the [describe-log-
    # groups](http://docs.aws.amazon.com/cli/latest/reference/logs/describe-log-
    # groups.html) command, or the applicable command in one of the AWS SDKs.
    cloud_watch_logs_log_group_arn: str = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


@dataclasses.dataclass
class CreateQueryLoggingConfigResponse(OutputShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "query_logging_config",
                "QueryLoggingConfig",
                TypeInfo(QueryLoggingConfig),
            ),
            (
                "location",
                "Location",
                TypeInfo(str),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains the ID for a query logging configuration, the
    # ID of the hosted zone that you want to log queries for, and the ARN for the
    # log group that you want Amazon Route 53 to send query logs to.
    query_logging_config: "QueryLoggingConfig" = dataclasses.field(
        default_factory=dict,
    )

    # The unique URL representing the new query logging configuration.
    location: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class CreateReusableDelegationSetRequest(ShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "caller_reference",
                "CallerReference",
                TypeInfo(str),
            ),
            (
                "hosted_zone_id",
                "HostedZoneId",
                TypeInfo(str),
            ),
        ]

    # A unique string that identifies the request, and that allows you to retry
    # failed `CreateReusableDelegationSet` requests without the risk of executing
    # the operation twice. You must use a unique `CallerReference` string every
    # time you submit a `CreateReusableDelegationSet` request. `CallerReference`
    # can be any unique string, for example a date/time stamp.
    caller_reference: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If you want to mark the delegation set for an existing hosted zone as
    # reusable, the ID for that hosted zone.
    hosted_zone_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class CreateReusableDelegationSetResponse(OutputShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "delegation_set",
                "DelegationSet",
                TypeInfo(DelegationSet),
            ),
            (
                "location",
                "Location",
                TypeInfo(str),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains name server information.
    delegation_set: "DelegationSet" = dataclasses.field(default_factory=dict, )

    # The unique URL representing the new reusable delegation set.
    location: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class CreateTrafficPolicyInstanceRequest(ShapeBase):
    """
    A complex type that contains information about the resource record sets that you
    want to create based on a specified traffic policy.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "hosted_zone_id",
                "HostedZoneId",
                TypeInfo(str),
            ),
            (
                "name",
                "Name",
                TypeInfo(str),
            ),
            (
                "ttl",
                "TTL",
                TypeInfo(int),
            ),
            (
                "traffic_policy_id",
                "TrafficPolicyId",
                TypeInfo(str),
            ),
            (
                "traffic_policy_version",
                "TrafficPolicyVersion",
                TypeInfo(int),
            ),
        ]

    # The ID of the hosted zone in which you want Amazon Route 53 to create
    # resource record sets by using the configuration in a traffic policy.
    hosted_zone_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The domain name (such as example.com) or subdomain name (such as
    # www.example.com) for which Amazon Route 53 responds to DNS queries by using
    # the resource record sets that Amazon Route 53 creates for this traffic
    # policy instance.
    name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # (Optional) The TTL that you want Amazon Route 53 to assign to all of the
    # resource record sets that it creates in the specified hosted zone.
    ttl: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The ID of the traffic policy that you want to use to create resource record
    # sets in the specified hosted zone.
    traffic_policy_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The version of the traffic policy that you want to use to create resource
    # record sets in the specified hosted zone.
    traffic_policy_version: int = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class CreateTrafficPolicyInstanceResponse(OutputShapeBase):
    """
    A complex type that contains the response information for the
    `CreateTrafficPolicyInstance` request.
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
                "traffic_policy_instance",
                "TrafficPolicyInstance",
                TypeInfo(TrafficPolicyInstance),
            ),
            (
                "location",
                "Location",
                TypeInfo(str),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains settings for the new traffic policy instance.
    traffic_policy_instance: "TrafficPolicyInstance" = dataclasses.field(
        default_factory=dict,
    )

    # A unique URL that represents a new traffic policy instance.
    location: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class CreateTrafficPolicyRequest(ShapeBase):
    """
    A complex type that contains information about the traffic policy that you want
    to create.
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
                "document",
                "Document",
                TypeInfo(str),
            ),
            (
                "comment",
                "Comment",
                TypeInfo(str),
            ),
        ]

    # The name of the traffic policy.
    name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The definition of this traffic policy in JSON format. For more information,
    # see [Traffic Policy Document
    # Format](http://docs.aws.amazon.com/Route53/latest/APIReference/api-
    # policies-traffic-policy-document-format.html).
    document: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # (Optional) Any comments that you want to include about the traffic policy.
    comment: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class CreateTrafficPolicyResponse(OutputShapeBase):
    """
    A complex type that contains the response information for the
    `CreateTrafficPolicy` request.
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
                "traffic_policy",
                "TrafficPolicy",
                TypeInfo(TrafficPolicy),
            ),
            (
                "location",
                "Location",
                TypeInfo(str),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains settings for the new traffic policy.
    traffic_policy: "TrafficPolicy" = dataclasses.field(default_factory=dict, )

    # A unique URL that represents a new traffic policy.
    location: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class CreateTrafficPolicyVersionRequest(ShapeBase):
    """
    A complex type that contains information about the traffic policy that you want
    to create a new version for.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "id",
                "Id",
                TypeInfo(str),
            ),
            (
                "document",
                "Document",
                TypeInfo(str),
            ),
            (
                "comment",
                "Comment",
                TypeInfo(str),
            ),
        ]

    # The ID of the traffic policy for which you want to create a new version.
    id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The definition of this version of the traffic policy, in JSON format. You
    # specified the JSON in the `CreateTrafficPolicyVersion` request. For more
    # information about the JSON format, see CreateTrafficPolicy.
    document: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The comment that you specified in the `CreateTrafficPolicyVersion` request,
    # if any.
    comment: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class CreateTrafficPolicyVersionResponse(OutputShapeBase):
    """
    A complex type that contains the response information for the
    `CreateTrafficPolicyVersion` request.
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
                "traffic_policy",
                "TrafficPolicy",
                TypeInfo(TrafficPolicy),
            ),
            (
                "location",
                "Location",
                TypeInfo(str),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains settings for the new version of the traffic
    # policy.
    traffic_policy: "TrafficPolicy" = dataclasses.field(default_factory=dict, )

    # A unique URL that represents a new traffic policy version.
    location: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class CreateVPCAssociationAuthorizationRequest(ShapeBase):
    """
    A complex type that contains information about the request to authorize
    associating a VPC with your private hosted zone. Authorization is only required
    when a private hosted zone and a VPC were created by using different accounts.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "hosted_zone_id",
                "HostedZoneId",
                TypeInfo(str),
            ),
            (
                "vpc",
                "VPC",
                TypeInfo(VPC),
            ),
        ]

    # The ID of the private hosted zone that you want to authorize associating a
    # VPC with.
    hosted_zone_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A complex type that contains the VPC ID and region for the VPC that you
    # want to authorize associating with your hosted zone.
    vpc: "VPC" = dataclasses.field(default_factory=dict, )


@dataclasses.dataclass
class CreateVPCAssociationAuthorizationResponse(OutputShapeBase):
    """
    A complex type that contains the response information from a
    `CreateVPCAssociationAuthorization` request.
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
                "hosted_zone_id",
                "HostedZoneId",
                TypeInfo(str),
            ),
            (
                "vpc",
                "VPC",
                TypeInfo(VPC),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The ID of the hosted zone that you authorized associating a VPC with.
    hosted_zone_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The VPC that you authorized associating with a hosted zone.
    vpc: "VPC" = dataclasses.field(default_factory=dict, )


@dataclasses.dataclass
class DelegationSet(ShapeBase):
    """
    A complex type that lists the name servers in a delegation set, as well as the
    `CallerReference` and the `ID` for the delegation set.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "name_servers",
                "NameServers",
                TypeInfo(typing.List[str]),
            ),
            (
                "id",
                "Id",
                TypeInfo(str),
            ),
            (
                "caller_reference",
                "CallerReference",
                TypeInfo(str),
            ),
        ]

    # A complex type that contains a list of the authoritative name servers for a
    # hosted zone or for a reusable delegation set.
    name_servers: typing.List[str] = dataclasses.field(default_factory=list, )

    # The ID that Amazon Route 53 assigns to a reusable delegation set.
    id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The value that you specified for `CallerReference` when you created the
    # reusable delegation set.
    caller_reference: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DelegationSetAlreadyCreated(ShapeBase):
    """
    A delegation set with the same owner and caller reference combination has
    already been created.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DelegationSetAlreadyReusable(ShapeBase):
    """
    The specified delegation set has already been marked as reusable.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DelegationSetInUse(ShapeBase):
    """
    The specified delegation contains associated hosted zones which must be deleted
    before the reusable delegation set can be deleted.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DelegationSetNotAvailable(ShapeBase):
    """
    You can create a hosted zone that has the same name as an existing hosted zone
    (example.com is common), but there is a limit to the number of hosted zones that
    have the same name. If you get this error, Amazon Route 53 has reached that
    limit. If you own the domain name and Amazon Route 53 generates this error,
    contact Customer Support.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DelegationSetNotReusable(ShapeBase):
    """
    A reusable delegation set with the specified ID does not exist.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DeleteHealthCheckRequest(ShapeBase):
    """
    This action deletes a health check.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "health_check_id",
                "HealthCheckId",
                TypeInfo(str),
            ),
        ]

    # The ID of the health check that you want to delete.
    health_check_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DeleteHealthCheckResponse(OutputShapeBase):
    """
    An empty element.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


@dataclasses.dataclass
class DeleteHostedZoneRequest(ShapeBase):
    """
    A request to delete a hosted zone.
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

    # The ID of the hosted zone you want to delete.
    id: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DeleteHostedZoneResponse(OutputShapeBase):
    """
    A complex type that contains the response to a `DeleteHostedZone` request.
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
                "change_info",
                "ChangeInfo",
                TypeInfo(ChangeInfo),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains the ID, the status, and the date and time of a
    # request to delete a hosted zone.
    change_info: "ChangeInfo" = dataclasses.field(default_factory=dict, )


@dataclasses.dataclass
class DeleteQueryLoggingConfigRequest(ShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "id",
                "Id",
                TypeInfo(str),
            ),
        ]

    # The ID of the configuration that you want to delete.
    id: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DeleteQueryLoggingConfigResponse(OutputShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


@dataclasses.dataclass
class DeleteReusableDelegationSetRequest(ShapeBase):
    """
    A request to delete a reusable delegation set.
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

    # The ID of the reusable delegation set that you want to delete.
    id: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DeleteReusableDelegationSetResponse(OutputShapeBase):
    """
    An empty element.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


@dataclasses.dataclass
class DeleteTrafficPolicyInstanceRequest(ShapeBase):
    """
    A request to delete a specified traffic policy instance.
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

    # The ID of the traffic policy instance that you want to delete.

    # When you delete a traffic policy instance, Amazon Route 53 also deletes all
    # of the resource record sets that were created when you created the traffic
    # policy instance.
    id: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DeleteTrafficPolicyInstanceResponse(OutputShapeBase):
    """
    An empty element.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


@dataclasses.dataclass
class DeleteTrafficPolicyRequest(ShapeBase):
    """
    A request to delete a specified traffic policy version.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "id",
                "Id",
                TypeInfo(str),
            ),
            (
                "version",
                "Version",
                TypeInfo(int),
            ),
        ]

    # The ID of the traffic policy that you want to delete.
    id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The version number of the traffic policy that you want to delete.
    version: int = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DeleteTrafficPolicyResponse(OutputShapeBase):
    """
    An empty element.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


@dataclasses.dataclass
class DeleteVPCAssociationAuthorizationRequest(ShapeBase):
    """
    A complex type that contains information about the request to remove
    authorization to associate a VPC that was created by one AWS account with a
    hosted zone that was created with a different AWS account.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "hosted_zone_id",
                "HostedZoneId",
                TypeInfo(str),
            ),
            (
                "vpc",
                "VPC",
                TypeInfo(VPC),
            ),
        ]

    # When removing authorization to associate a VPC that was created by one AWS
    # account with a hosted zone that was created with a different AWS account,
    # the ID of the hosted zone.
    hosted_zone_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # When removing authorization to associate a VPC that was created by one AWS
    # account with a hosted zone that was created with a different AWS account, a
    # complex type that includes the ID and region of the VPC.
    vpc: "VPC" = dataclasses.field(default_factory=dict, )


@dataclasses.dataclass
class DeleteVPCAssociationAuthorizationResponse(OutputShapeBase):
    """
    Empty response for the request.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


@dataclasses.dataclass
class Dimension(ShapeBase):
    """
    For the metric that the CloudWatch alarm is associated with, a complex type that
    contains information about one dimension.
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
                "value",
                "Value",
                TypeInfo(str),
            ),
        ]

    # For the metric that the CloudWatch alarm is associated with, the name of
    # one dimension.
    name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # For the metric that the CloudWatch alarm is associated with, the value of
    # one dimension.
    value: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DisassociateVPCFromHostedZoneRequest(ShapeBase):
    """
    A complex type that contains information about the VPC that you want to
    disassociate from a specified private hosted zone.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "hosted_zone_id",
                "HostedZoneId",
                TypeInfo(str),
            ),
            (
                "vpc",
                "VPC",
                TypeInfo(VPC),
            ),
            (
                "comment",
                "Comment",
                TypeInfo(str),
            ),
        ]

    # The ID of the private hosted zone that you want to disassociate a VPC from.
    hosted_zone_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A complex type that contains information about the VPC that you're
    # disassociating from the specified hosted zone.
    vpc: "VPC" = dataclasses.field(default_factory=dict, )

    # _Optional:_ A comment about the disassociation request.
    comment: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class DisassociateVPCFromHostedZoneResponse(OutputShapeBase):
    """
    A complex type that contains the response information for the disassociate
    request.
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
                "change_info",
                "ChangeInfo",
                TypeInfo(ChangeInfo),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that describes the changes made to the specified private
    # hosted zone.
    change_info: "ChangeInfo" = dataclasses.field(default_factory=dict, )


@dataclasses.dataclass
class GeoLocation(ShapeBase):
    """
    A complex type that contains information about a geo location.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "continent_code",
                "ContinentCode",
                TypeInfo(str),
            ),
            (
                "country_code",
                "CountryCode",
                TypeInfo(str),
            ),
            (
                "subdivision_code",
                "SubdivisionCode",
                TypeInfo(str),
            ),
        ]

    # The two-letter code for the continent.

    # Valid values: `AF` | `AN` | `AS` | `EU` | `OC` | `NA` | `SA`

    # Constraint: Specifying `ContinentCode` with either `CountryCode` or
    # `SubdivisionCode` returns an `InvalidInput` error.
    continent_code: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The two-letter code for the country.
    country_code: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The code for the subdivision, for example, a state in the United States or
    # a province in Canada.
    subdivision_code: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class GeoLocationDetails(ShapeBase):
    """
    A complex type that contains the codes and full continent, country, and
    subdivision names for the specified `geolocation` code.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "continent_code",
                "ContinentCode",
                TypeInfo(str),
            ),
            (
                "continent_name",
                "ContinentName",
                TypeInfo(str),
            ),
            (
                "country_code",
                "CountryCode",
                TypeInfo(str),
            ),
            (
                "country_name",
                "CountryName",
                TypeInfo(str),
            ),
            (
                "subdivision_code",
                "SubdivisionCode",
                TypeInfo(str),
            ),
            (
                "subdivision_name",
                "SubdivisionName",
                TypeInfo(str),
            ),
        ]

    # The two-letter code for the continent.
    continent_code: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The full name of the continent.
    continent_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The two-letter code for the country.
    country_code: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the country.
    country_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The code for the subdivision, for example, a state in the United States or
    # a province in Canada.
    subdivision_code: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The full name of the subdivision, for example, a state in the United States
    # or a province in Canada.
    subdivision_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class GetAccountLimitRequest(ShapeBase):
    """
    A complex type that contains information about the request to create a hosted
    zone.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "type",
                "Type",
                TypeInfo(AccountLimitType),
            ),
        ]

    # The limit that you want to get. Valid values include the following:

    #   * **MAX_HEALTH_CHECKS_BY_OWNER** : The maximum number of health checks that you can create using the current account.

    #   * **MAX_HOSTED_ZONES_BY_OWNER** : The maximum number of hosted zones that you can create using the current account.

    #   * **MAX_REUSABLE_DELEGATION_SETS_BY_OWNER** : The maximum number of reusable delegation sets that you can create using the current account.

    #   * **MAX_TRAFFIC_POLICIES_BY_OWNER** : The maximum number of traffic policies that you can create using the current account.

    #   * **MAX_TRAFFIC_POLICY_INSTANCES_BY_OWNER** : The maximum number of traffic policy instances that you can create using the current account. (Traffic policy instances are referred to as traffic flow policy records in the Amazon Route 53 console.)
    type: "AccountLimitType" = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class GetAccountLimitResponse(OutputShapeBase):
    """
    A complex type that contains the requested limit.
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
                "limit",
                "Limit",
                TypeInfo(AccountLimit),
            ),
            (
                "count",
                "Count",
                TypeInfo(int),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The current setting for the specified limit. For example, if you specified
    # `MAX_HEALTH_CHECKS_BY_OWNER` for the value of `Type` in the request, the
    # value of `Limit` is the maximum number of health checks that you can create
    # using the current account.
    limit: "AccountLimit" = dataclasses.field(default_factory=dict, )

    # The current number of entities that you have created of the specified type.
    # For example, if you specified `MAX_HEALTH_CHECKS_BY_OWNER` for the value of
    # `Type` in the request, the value of `Count` is the current number of health
    # checks that you have created using the current account.
    count: int = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class GetChangeRequest(ShapeBase):
    """
    The input for a GetChange request.
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

    # The ID of the change batch request. The value that you specify here is the
    # value that `ChangeResourceRecordSets` returned in the `Id` element when you
    # submitted the request.
    id: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class GetChangeResponse(OutputShapeBase):
    """
    A complex type that contains the `ChangeInfo` element.
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
                "change_info",
                "ChangeInfo",
                TypeInfo(ChangeInfo),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains information about the specified change batch.
    change_info: "ChangeInfo" = dataclasses.field(default_factory=dict, )


@dataclasses.dataclass
class GetCheckerIpRangesRequest(ShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return []


@dataclasses.dataclass
class GetCheckerIpRangesResponse(OutputShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "checker_ip_ranges",
                "CheckerIpRanges",
                TypeInfo(typing.List[str]),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )
    checker_ip_ranges: typing.List[str] = dataclasses.field(
        default_factory=list,
    )


@dataclasses.dataclass
class GetGeoLocationRequest(ShapeBase):
    """
    A request for information about whether a specified geographic location is
    supported for Amazon Route 53 geolocation resource record sets.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "continent_code",
                "ContinentCode",
                TypeInfo(str),
            ),
            (
                "country_code",
                "CountryCode",
                TypeInfo(str),
            ),
            (
                "subdivision_code",
                "SubdivisionCode",
                TypeInfo(str),
            ),
        ]

    # Amazon Route 53 supports the following continent codes:

    #   * **AF** : Africa

    #   * **AN** : Antarctica

    #   * **AS** : Asia

    #   * **EU** : Europe

    #   * **OC** : Oceania

    #   * **NA** : North America

    #   * **SA** : South America
    continent_code: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Amazon Route 53 uses the two-letter country codes that are specified in
    # [ISO standard 3166-1
    # alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).
    country_code: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Amazon Route 53 uses the one- to three-letter subdivision codes that are
    # specified in [ISO standard 3166-1
    # alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2). Amazon Route 53
    # doesn't support subdivision codes for all countries. If you specify
    # `SubdivisionCode`, you must also specify `CountryCode`.
    subdivision_code: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class GetGeoLocationResponse(OutputShapeBase):
    """
    A complex type that contains the response information for the specified
    geolocation code.
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
                "geo_location_details",
                "GeoLocationDetails",
                TypeInfo(GeoLocationDetails),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains the codes and full continent, country, and
    # subdivision names for the specified geolocation code.
    geo_location_details: "GeoLocationDetails" = dataclasses.field(
        default_factory=dict,
    )


@dataclasses.dataclass
class GetHealthCheckCountRequest(ShapeBase):
    """
    A request for the number of health checks that are associated with the current
    AWS account.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return []


@dataclasses.dataclass
class GetHealthCheckCountResponse(OutputShapeBase):
    """
    A complex type that contains the response to a `GetHealthCheckCount` request.
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
                "health_check_count",
                "HealthCheckCount",
                TypeInfo(int),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The number of health checks associated with the current AWS account.
    health_check_count: int = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class GetHealthCheckLastFailureReasonRequest(ShapeBase):
    """
    A request for the reason that a health check failed most recently.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "health_check_id",
                "HealthCheckId",
                TypeInfo(str),
            ),
        ]

    # The ID for the health check for which you want the last failure reason.
    # When you created the health check, `CreateHealthCheck` returned the ID in
    # the response, in the `HealthCheckId` element.

    # If you want to get the last failure reason for a calculated health check,
    # you must use the Amazon Route 53 console or the CloudWatch console. You
    # can't use `GetHealthCheckLastFailureReason` for a calculated health check.
    health_check_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class GetHealthCheckLastFailureReasonResponse(OutputShapeBase):
    """
    A complex type that contains the response to a `GetHealthCheckLastFailureReason`
    request.
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
                "health_check_observations",
                "HealthCheckObservations",
                TypeInfo(typing.List[HealthCheckObservation]),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A list that contains one `Observation` element for each Amazon Route 53
    # health checker that is reporting a last failure reason.
    health_check_observations: typing.List["HealthCheckObservation"
                                          ] = dataclasses.field(
                                              default_factory=list,
                                          )


@dataclasses.dataclass
class GetHealthCheckRequest(ShapeBase):
    """
    A request to get information about a specified health check.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "health_check_id",
                "HealthCheckId",
                TypeInfo(str),
            ),
        ]

    # The identifier that Amazon Route 53 assigned to the health check when you
    # created it. When you add or update a resource record set, you use this
    # value to specify which health check to use. The value can be up to 64
    # characters long.
    health_check_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class GetHealthCheckResponse(OutputShapeBase):
    """
    A complex type that contains the response to a `GetHealthCheck` request.
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
                "health_check",
                "HealthCheck",
                TypeInfo(HealthCheck),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains information about one health check that is
    # associated with the current AWS account.
    health_check: "HealthCheck" = dataclasses.field(default_factory=dict, )


@dataclasses.dataclass
class GetHealthCheckStatusRequest(ShapeBase):
    """
    A request to get the status for a health check.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "health_check_id",
                "HealthCheckId",
                TypeInfo(str),
            ),
        ]

    # The ID for the health check that you want the current status for. When you
    # created the health check, `CreateHealthCheck` returned the ID in the
    # response, in the `HealthCheckId` element.

    # If you want to check the status of a calculated health check, you must use
    # the Amazon Route 53 console or the CloudWatch console. You can't use
    # `GetHealthCheckStatus` to get the status of a calculated health check.
    health_check_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class GetHealthCheckStatusResponse(OutputShapeBase):
    """
    A complex type that contains the response to a `GetHealthCheck` request.
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
                "health_check_observations",
                "HealthCheckObservations",
                TypeInfo(typing.List[HealthCheckObservation]),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A list that contains one `HealthCheckObservation` element for each Amazon
    # Route 53 health checker that is reporting a status about the health check
    # endpoint.
    health_check_observations: typing.List["HealthCheckObservation"
                                          ] = dataclasses.field(
                                              default_factory=list,
                                          )


@dataclasses.dataclass
class GetHostedZoneCountRequest(ShapeBase):
    """
    A request to retrieve a count of all the hosted zones that are associated with
    the current AWS account.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return []


@dataclasses.dataclass
class GetHostedZoneCountResponse(OutputShapeBase):
    """
    A complex type that contains the response to a `GetHostedZoneCount` request.
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
                "hosted_zone_count",
                "HostedZoneCount",
                TypeInfo(int),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The total number of public and private hosted zones that are associated
    # with the current AWS account.
    hosted_zone_count: int = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class GetHostedZoneLimitRequest(ShapeBase):
    """
    A complex type that contains information about the request to create a hosted
    zone.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "type",
                "Type",
                TypeInfo(HostedZoneLimitType),
            ),
            (
                "hosted_zone_id",
                "HostedZoneId",
                TypeInfo(str),
            ),
        ]

    # The limit that you want to get. Valid values include the following:

    #   * **MAX_RRSETS_BY_ZONE** : The maximum number of records that you can create in the specified hosted zone.

    #   * **MAX_VPCS_ASSOCIATED_BY_ZONE** : The maximum number of Amazon VPCs that you can associate with the specified private hosted zone.
    type: "HostedZoneLimitType" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The ID of the hosted zone that you want to get a limit for.
    hosted_zone_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class GetHostedZoneLimitResponse(OutputShapeBase):
    """
    A complex type that contains the requested limit.
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
                "limit",
                "Limit",
                TypeInfo(HostedZoneLimit),
            ),
            (
                "count",
                "Count",
                TypeInfo(int),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The current setting for the specified limit. For example, if you specified
    # `MAX_RRSETS_BY_ZONE` for the value of `Type` in the request, the value of
    # `Limit` is the maximum number of records that you can create in the
    # specified hosted zone.
    limit: "HostedZoneLimit" = dataclasses.field(default_factory=dict, )

    # The current number of entities that you have created of the specified type.
    # For example, if you specified `MAX_RRSETS_BY_ZONE` for the value of `Type`
    # in the request, the value of `Count` is the current number of records that
    # you have created in the specified hosted zone.
    count: int = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class GetHostedZoneRequest(ShapeBase):
    """
    A request to get information about a specified hosted zone.
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

    # The ID of the hosted zone that you want to get information about.
    id: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class GetHostedZoneResponse(OutputShapeBase):
    """
    A complex type that contain the response to a `GetHostedZone` request.
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
                "hosted_zone",
                "HostedZone",
                TypeInfo(HostedZone),
            ),
            (
                "delegation_set",
                "DelegationSet",
                TypeInfo(DelegationSet),
            ),
            (
                "_vpcs",
                "VPCs",
                TypeInfo(typing.List[VPC]),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains general information about the specified hosted
    # zone.
    hosted_zone: "HostedZone" = dataclasses.field(default_factory=dict, )

    # A complex type that lists the Amazon Route 53 name servers for the
    # specified hosted zone.
    delegation_set: "DelegationSet" = dataclasses.field(default_factory=dict, )

    # A complex type that contains information about the VPCs that are associated
    # with the specified hosted zone.
    _vpcs: typing.List["VPC"] = dataclasses.field(default_factory=list, )


@dataclasses.dataclass
class GetQueryLoggingConfigRequest(ShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "id",
                "Id",
                TypeInfo(str),
            ),
        ]

    # The ID of the configuration for DNS query logging that you want to get
    # information about.
    id: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class GetQueryLoggingConfigResponse(OutputShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "query_logging_config",
                "QueryLoggingConfig",
                TypeInfo(QueryLoggingConfig),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains information about the query logging
    # configuration that you specified in a GetQueryLoggingConfig request.
    query_logging_config: "QueryLoggingConfig" = dataclasses.field(
        default_factory=dict,
    )


@dataclasses.dataclass
class GetReusableDelegationSetLimitRequest(ShapeBase):
    """
    A complex type that contains information about the request to create a hosted
    zone.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "type",
                "Type",
                TypeInfo(ReusableDelegationSetLimitType),
            ),
            (
                "delegation_set_id",
                "DelegationSetId",
                TypeInfo(str),
            ),
        ]

    # Specify `MAX_ZONES_BY_REUSABLE_DELEGATION_SET` to get the maximum number of
    # hosted zones that you can associate with the specified reusable delegation
    # set.
    type: "ReusableDelegationSetLimitType" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The ID of the delegation set that you want to get the limit for.
    delegation_set_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class GetReusableDelegationSetLimitResponse(OutputShapeBase):
    """
    A complex type that contains the requested limit.
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
                "limit",
                "Limit",
                TypeInfo(ReusableDelegationSetLimit),
            ),
            (
                "count",
                "Count",
                TypeInfo(int),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The current setting for the limit on hosted zones that you can associate
    # with the specified reusable delegation set.
    limit: "ReusableDelegationSetLimit" = dataclasses.field(
        default_factory=dict,
    )

    # The current number of hosted zones that you can associate with the
    # specified reusable delegation set.
    count: int = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class GetReusableDelegationSetRequest(ShapeBase):
    """
    A request to get information about a specified reusable delegation set.
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

    # The ID of the reusable delegation set that you want to get a list of name
    # servers for.
    id: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class GetReusableDelegationSetResponse(OutputShapeBase):
    """
    A complex type that contains the response to the `GetReusableDelegationSet`
    request.
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
                "delegation_set",
                "DelegationSet",
                TypeInfo(DelegationSet),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains information about the reusable delegation set.
    delegation_set: "DelegationSet" = dataclasses.field(default_factory=dict, )


@dataclasses.dataclass
class GetTrafficPolicyInstanceCountRequest(ShapeBase):
    """
    Request to get the number of traffic policy instances that are associated with
    the current AWS account.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return []


@dataclasses.dataclass
class GetTrafficPolicyInstanceCountResponse(OutputShapeBase):
    """
    A complex type that contains information about the resource record sets that
    Amazon Route 53 created based on a specified traffic policy.
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
                "traffic_policy_instance_count",
                "TrafficPolicyInstanceCount",
                TypeInfo(int),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The number of traffic policy instances that are associated with the current
    # AWS account.
    traffic_policy_instance_count: int = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


@dataclasses.dataclass
class GetTrafficPolicyInstanceRequest(ShapeBase):
    """
    Gets information about a specified traffic policy instance.
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

    # The ID of the traffic policy instance that you want to get information
    # about.
    id: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class GetTrafficPolicyInstanceResponse(OutputShapeBase):
    """
    A complex type that contains information about the resource record sets that
    Amazon Route 53 created based on a specified traffic policy.
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
                "traffic_policy_instance",
                "TrafficPolicyInstance",
                TypeInfo(TrafficPolicyInstance),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains settings for the traffic policy instance.
    traffic_policy_instance: "TrafficPolicyInstance" = dataclasses.field(
        default_factory=dict,
    )


@dataclasses.dataclass
class GetTrafficPolicyRequest(ShapeBase):
    """
    Gets information about a specific traffic policy version.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "id",
                "Id",
                TypeInfo(str),
            ),
            (
                "version",
                "Version",
                TypeInfo(int),
            ),
        ]

    # The ID of the traffic policy that you want to get information about.
    id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The version number of the traffic policy that you want to get information
    # about.
    version: int = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class GetTrafficPolicyResponse(OutputShapeBase):
    """
    A complex type that contains the response information for the request.
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
                "traffic_policy",
                "TrafficPolicy",
                TypeInfo(TrafficPolicy),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains settings for the specified traffic policy.
    traffic_policy: "TrafficPolicy" = dataclasses.field(default_factory=dict, )


@dataclasses.dataclass
class HealthCheck(ShapeBase):
    """
    A complex type that contains information about one health check that is
    associated with the current AWS account.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "id",
                "Id",
                TypeInfo(str),
            ),
            (
                "caller_reference",
                "CallerReference",
                TypeInfo(str),
            ),
            (
                "health_check_config",
                "HealthCheckConfig",
                TypeInfo(HealthCheckConfig),
            ),
            (
                "health_check_version",
                "HealthCheckVersion",
                TypeInfo(int),
            ),
            (
                "linked_service",
                "LinkedService",
                TypeInfo(LinkedService),
            ),
            (
                "cloud_watch_alarm_configuration",
                "CloudWatchAlarmConfiguration",
                TypeInfo(CloudWatchAlarmConfiguration),
            ),
        ]

    # The identifier that Amazon Route 53assigned to the health check when you
    # created it. When you add or update a resource record set, you use this
    # value to specify which health check to use. The value can be up to 64
    # characters long.
    id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A unique string that you specified when you created the health check.
    caller_reference: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A complex type that contains detailed information about one health check.
    health_check_config: "HealthCheckConfig" = dataclasses.field(
        default_factory=dict,
    )

    # The version of the health check. You can optionally pass this value in a
    # call to `UpdateHealthCheck` to prevent overwriting another change to the
    # health check.
    health_check_version: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If the health check was created by another service, the service that
    # created the health check. When a health check is created by another
    # service, you can't edit or delete it using Amazon Route 53.
    linked_service: "LinkedService" = dataclasses.field(default_factory=dict, )

    # A complex type that contains information about the CloudWatch alarm that
    # Amazon Route 53 is monitoring for this health check.
    cloud_watch_alarm_configuration: "CloudWatchAlarmConfiguration" = dataclasses.field(
        default_factory=dict,
    )


@dataclasses.dataclass
class HealthCheckAlreadyExists(ShapeBase):
    """
    The health check you're attempting to create already exists. Amazon Route 53
    returns this error when you submit a request that has the following values:

      * The same value for `CallerReference` as an existing health check, and one or more values that differ from the existing health check that has the same caller reference.

      * The same value for `CallerReference` as a health check that you created and later deleted, regardless of the other settings in the request.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class HealthCheckConfig(ShapeBase):
    """
    A complex type that contains information about the health check.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "type",
                "Type",
                TypeInfo(HealthCheckType),
            ),
            (
                "ip_address",
                "IPAddress",
                TypeInfo(str),
            ),
            (
                "port",
                "Port",
                TypeInfo(int),
            ),
            (
                "resource_path",
                "ResourcePath",
                TypeInfo(str),
            ),
            (
                "fully_qualified_domain_name",
                "FullyQualifiedDomainName",
                TypeInfo(str),
            ),
            (
                "search_string",
                "SearchString",
                TypeInfo(str),
            ),
            (
                "request_interval",
                "RequestInterval",
                TypeInfo(int),
            ),
            (
                "failure_threshold",
                "FailureThreshold",
                TypeInfo(int),
            ),
            (
                "measure_latency",
                "MeasureLatency",
                TypeInfo(bool),
            ),
            (
                "inverted",
                "Inverted",
                TypeInfo(bool),
            ),
            (
                "health_threshold",
                "HealthThreshold",
                TypeInfo(int),
            ),
            (
                "child_health_checks",
                "ChildHealthChecks",
                TypeInfo(typing.List[str]),
            ),
            (
                "enable_sni",
                "EnableSNI",
                TypeInfo(bool),
            ),
            (
                "regions",
                "Regions",
                TypeInfo(typing.List[HealthCheckRegion]),
            ),
            (
                "alarm_identifier",
                "AlarmIdentifier",
                TypeInfo(AlarmIdentifier),
            ),
            (
                "insufficient_data_health_status",
                "InsufficientDataHealthStatus",
                TypeInfo(InsufficientDataHealthStatus),
            ),
        ]

    # The type of health check that you want to create, which indicates how
    # Amazon Route 53 determines whether an endpoint is healthy.

    # You can't change the value of `Type` after you create a health check.

    # You can create the following types of health checks:

    #   * **HTTP** : Amazon Route 53 tries to establish a TCP connection. If successful, Amazon Route 53 submits an HTTP request and waits for an HTTP status code of 200 or greater and less than 400.

    #   * **HTTPS** : Amazon Route 53 tries to establish a TCP connection. If successful, Amazon Route 53 submits an HTTPS request and waits for an HTTP status code of 200 or greater and less than 400.

    # If you specify `HTTPS` for the value of `Type`, the endpoint must support
    # TLS v1.0 or later.

    #   * **HTTP_STR_MATCH** : Amazon Route 53 tries to establish a TCP connection. If successful, Amazon Route 53 submits an HTTP request and searches the first 5,120 bytes of the response body for the string that you specify in `SearchString`.

    #   * **HTTPS_STR_MATCH** : Amazon Route 53 tries to establish a TCP connection. If successful, Amazon Route 53 submits an `HTTPS` request and searches the first 5,120 bytes of the response body for the string that you specify in `SearchString`.

    #   * **TCP** : Amazon Route 53 tries to establish a TCP connection.

    #   * **CLOUDWATCH_METRIC** : The health check is associated with a CloudWatch alarm. If the state of the alarm is `OK`, the health check is considered healthy. If the state is `ALARM`, the health check is considered unhealthy. If CloudWatch doesn't have sufficient data to determine whether the state is `OK` or `ALARM`, the health check status depends on the setting for `InsufficientDataHealthStatus`: `Healthy`, `Unhealthy`, or `LastKnownStatus`.

    #   * **CALCULATED** : For health checks that monitor the status of other health checks, Amazon Route 53 adds up the number of health checks that Amazon Route 53 health checkers consider to be healthy and compares that number with the value of `HealthThreshold`.

    # For more information, see [How Amazon Route 53 Determines Whether an
    # Endpoint Is
    # Healthy](http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-
    # failover-determining-health-of-endpoints.html) in the _Amazon Route 53
    # Developer Guide_.
    type: "HealthCheckType" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The IPv4 or IPv6 IP address of the endpoint that you want Amazon Route 53
    # to perform health checks on. If you don't specify a value for `IPAddress`,
    # Amazon Route 53 sends a DNS request to resolve the domain name that you
    # specify in `FullyQualifiedDomainName` at the interval that you specify in
    # `RequestInterval`. Using an IP address returned by DNS, Amazon Route 53
    # then checks the health of the endpoint.

    # Use one of the following formats for the value of `IPAddress`:

    #   * **IPv4 address** : four values between 0 and 255, separated by periods (.), for example, `192.0.2.44`.

    #   * **IPv6 address** : eight groups of four hexadecimal values, separated by colons (:), for example, `2001:0db8:85a3:0000:0000:abcd:0001:2345`. You can also shorten IPv6 addresses as described in RFC 5952, for example, `2001:db8:85a3::abcd:1:2345`.

    # If the endpoint is an EC2 instance, we recommend that you create an Elastic
    # IP address, associate it with your EC2 instance, and specify the Elastic IP
    # address for `IPAddress`. This ensures that the IP address of your instance
    # will never change.

    # For more information, see HealthCheckConfig$FullyQualifiedDomainName.

    # Constraints: Amazon Route 53 can't check the health of endpoints for which
    # the IP address is in local, private, non-routable, or multicast ranges. For
    # more information about IP addresses for which you can't create health
    # checks, see the following documents:

    #   * [RFC 5735, Special Use IPv4 Addresses](https://tools.ietf.org/html/rfc5735)

    #   * [RFC 6598, IANA-Reserved IPv4 Prefix for Shared Address Space](https://tools.ietf.org/html/rfc6598)

    #   * [RFC 5156, Special-Use IPv6 Addresses](https://tools.ietf.org/html/rfc5156)

    # When the value of `Type` is `CALCULATED` or `CLOUDWATCH_METRIC`, omit
    # `IPAddress`.
    ip_address: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The port on the endpoint on which you want Amazon Route 53 to perform
    # health checks. Specify a value for `Port` only when you specify a value for
    # `IPAddress`.
    port: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The path, if any, that you want Amazon Route 53 to request when performing
    # health checks. The path can be any value for which your endpoint will
    # return an HTTP status code of 2xx or 3xx when the endpoint is healthy, for
    # example, the file /docs/route53-health-check.html.
    resource_path: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Amazon Route 53 behavior depends on whether you specify a value for
    # `IPAddress`.

    # **If you specify a value for** `IPAddress`:

    # Amazon Route 53 sends health check requests to the specified IPv4 or IPv6
    # address and passes the value of `FullyQualifiedDomainName` in the `Host`
    # header for all health checks except TCP health checks. This is typically
    # the fully qualified DNS name of the endpoint on which you want Amazon Route
    # 53 to perform health checks.

    # When Amazon Route 53 checks the health of an endpoint, here is how it
    # constructs the `Host` header:

    #   * If you specify a value of `80` for `Port` and `HTTP` or `HTTP_STR_MATCH` for `Type`, Amazon Route 53 passes the value of `FullyQualifiedDomainName` to the endpoint in the Host header.

    #   * If you specify a value of `443` for `Port` and `HTTPS` or `HTTPS_STR_MATCH` for `Type`, Amazon Route 53 passes the value of `FullyQualifiedDomainName` to the endpoint in the `Host` header.

    #   * If you specify another value for `Port` and any value except `TCP` for `Type`, Amazon Route 53 passes `FullyQualifiedDomainName:Port` to the endpoint in the `Host` header.

    # If you don't specify a value for `FullyQualifiedDomainName`, Amazon Route
    # 53 substitutes the value of `IPAddress` in the `Host` header in each of the
    # preceding cases.

    # **If you don't specify a value for`IPAddress` ** :

    # Amazon Route 53 sends a DNS request to the domain that you specify for
    # `FullyQualifiedDomainName` at the interval that you specify for
    # `RequestInterval`. Using an IPv4 address that DNS returns, Amazon Route 53
    # then checks the health of the endpoint.

    # If you don't specify a value for `IPAddress`, Amazon Route 53 uses only
    # IPv4 to send health checks to the endpoint. If there's no resource record
    # set with a type of A for the name that you specify for
    # `FullyQualifiedDomainName`, the health check fails with a "DNS resolution
    # failed" error.

    # If you want to check the health of weighted, latency, or failover resource
    # record sets and you choose to specify the endpoint only by
    # `FullyQualifiedDomainName`, we recommend that you create a separate health
    # check for each endpoint. For example, create a health check for each HTTP
    # server that is serving content for www.example.com. For the value of
    # `FullyQualifiedDomainName`, specify the domain name of the server (such as
    # us-east-2-www.example.com), not the name of the resource record sets
    # (www.example.com).

    # In this configuration, if you create a health check for which the value of
    # `FullyQualifiedDomainName` matches the name of the resource record sets and
    # you then associate the health check with those resource record sets, health
    # check results will be unpredictable.

    # In addition, if the value that you specify for `Type` is `HTTP`, `HTTPS`,
    # `HTTP_STR_MATCH`, or `HTTPS_STR_MATCH`, Amazon Route 53 passes the value of
    # `FullyQualifiedDomainName` in the `Host` header, as it does when you
    # specify a value for `IPAddress`. If the value of `Type` is `TCP`, Amazon
    # Route 53 doesn't pass a `Host` header.
    fully_qualified_domain_name: str = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # If the value of Type is `HTTP_STR_MATCH` or `HTTP_STR_MATCH`, the string
    # that you want Amazon Route 53 to search for in the response body from the
    # specified resource. If the string appears in the response body, Amazon
    # Route 53 considers the resource healthy.

    # Amazon Route 53 considers case when searching for `SearchString` in the
    # response body.
    search_string: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The number of seconds between the time that Amazon Route 53 gets a response
    # from your endpoint and the time that it sends the next health check
    # request. Each Amazon Route 53 health checker makes requests at this
    # interval.

    # You can't change the value of `RequestInterval` after you create a health
    # check.

    # If you don't specify a value for `RequestInterval`, the default value is
    # `30` seconds.
    request_interval: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The number of consecutive health checks that an endpoint must pass or fail
    # for Amazon Route 53 to change the current status of the endpoint from
    # unhealthy to healthy or vice versa. For more information, see [How Amazon
    # Route 53 Determines Whether an Endpoint Is
    # Healthy](http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-
    # failover-determining-health-of-endpoints.html) in the _Amazon Route 53
    # Developer Guide_.

    # If you don't specify a value for `FailureThreshold`, the default value is
    # three health checks.
    failure_threshold: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Specify whether you want Amazon Route 53 to measure the latency between
    # health checkers in multiple AWS regions and your endpoint, and to display
    # CloudWatch latency graphs on the **Health Checks** page in the Amazon Route
    # 53 console.

    # You can't change the value of `MeasureLatency` after you create a health
    # check.
    measure_latency: bool = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Specify whether you want Amazon Route 53 to invert the status of a health
    # check, for example, to consider a health check unhealthy when it otherwise
    # would be considered healthy.
    inverted: bool = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The number of child health checks that are associated with a `CALCULATED`
    # health that Amazon Route 53 must consider healthy for the `CALCULATED`
    # health check to be considered healthy. To specify the child health checks
    # that you want to associate with a `CALCULATED` health check, use the
    # HealthCheckConfig$ChildHealthChecks and HealthCheckConfig$ChildHealthChecks
    # elements.

    # Note the following:

    #   * If you specify a number greater than the number of child health checks, Amazon Route 53 always considers this health check to be unhealthy.

    #   * If you specify `0`, Amazon Route 53 always considers this health check to be healthy.
    health_threshold: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # (CALCULATED Health Checks Only) A complex type that contains one
    # `ChildHealthCheck` element for each health check that you want to associate
    # with a `CALCULATED` health check.
    child_health_checks: typing.List[str] = dataclasses.field(
        default_factory=list,
    )

    # Specify whether you want Amazon Route 53 to send the value of
    # `FullyQualifiedDomainName` to the endpoint in the `client_hello` message
    # during TLS negotiation. This allows the endpoint to respond to `HTTPS`
    # health check requests with the applicable SSL/TLS certificate.

    # Some endpoints require that `HTTPS` requests include the host name in the
    # `client_hello` message. If you don't enable SNI, the status of the health
    # check will be `SSL alert handshake_failure`. A health check can also have
    # that status for other reasons. If SNI is enabled and you're still getting
    # the error, check the SSL/TLS configuration on your endpoint and confirm
    # that your certificate is valid.

    # The SSL/TLS certificate on your endpoint includes a domain name in the
    # `Common Name` field and possibly several more in the `Subject Alternative
    # Names` field. One of the domain names in the certificate should match the
    # value that you specify for `FullyQualifiedDomainName`. If the endpoint
    # responds to the `client_hello` message with a certificate that does not
    # include the domain name that you specified in `FullyQualifiedDomainName`, a
    # health checker will retry the handshake. In the second attempt, the health
    # checker will omit `FullyQualifiedDomainName` from the `client_hello`
    # message.
    enable_sni: bool = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A complex type that contains one `Region` element for each region from
    # which you want Amazon Route 53 health checkers to check the specified
    # endpoint.

    # If you don't specify any regions, Amazon Route 53 health checkers
    # automatically performs checks from all of the regions that are listed under
    # **Valid Values**.

    # If you update a health check to remove a region that has been performing
    # health checks, Amazon Route 53 will briefly continue to perform checks from
    # that region to ensure that some health checkers are always checking the
    # endpoint (for example, if you replace three regions with four different
    # regions).
    regions: typing.List["HealthCheckRegion"] = dataclasses.field(
        default_factory=list,
    )

    # A complex type that identifies the CloudWatch alarm that you want Amazon
    # Route 53 health checkers to use to determine whether this health check is
    # healthy.
    alarm_identifier: "AlarmIdentifier" = dataclasses.field(
        default_factory=dict,
    )

    # When CloudWatch has insufficient data about the metric to determine the
    # alarm state, the status that you want Amazon Route 53 to assign to the
    # health check:

    #   * `Healthy`: Amazon Route 53 considers the health check to be healthy.

    #   * `Unhealthy`: Amazon Route 53 considers the health check to be unhealthy.

    #   * `LastKnownStatus`: Amazon Route 53 uses the status of the health check from the last time that CloudWatch had sufficient data to determine the alarm state. For new health checks that have no last known status, the default status for the health check is healthy.
    insufficient_data_health_status: "InsufficientDataHealthStatus" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


@dataclasses.dataclass
class HealthCheckInUse(ShapeBase):
    """
    This error code is not in use.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class HealthCheckObservation(ShapeBase):
    """
    A complex type that contains the last failure reason as reported by one Amazon
    Route 53 health checker.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "region",
                "Region",
                TypeInfo(HealthCheckRegion),
            ),
            (
                "ip_address",
                "IPAddress",
                TypeInfo(str),
            ),
            (
                "status_report",
                "StatusReport",
                TypeInfo(StatusReport),
            ),
        ]

    # The region of the Amazon Route 53 health checker that provided the status
    # in `StatusReport`.
    region: "HealthCheckRegion" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The IP address of the Amazon Route 53 health checker that provided the
    # failure reason in `StatusReport`.
    ip_address: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A complex type that contains the last failure reason as reported by one
    # Amazon Route 53 health checker and the time of the failed health check.
    status_report: "StatusReport" = dataclasses.field(default_factory=dict, )


class HealthCheckRegion(Enum):
    us_east_1 = "us-east-1"
    us_west_1 = "us-west-1"
    us_west_2 = "us-west-2"
    eu_west_1 = "eu-west-1"
    ap_southeast_1 = "ap-southeast-1"
    ap_southeast_2 = "ap-southeast-2"
    ap_northeast_1 = "ap-northeast-1"
    sa_east_1 = "sa-east-1"


class HealthCheckType(Enum):
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    HTTP_STR_MATCH = "HTTP_STR_MATCH"
    HTTPS_STR_MATCH = "HTTPS_STR_MATCH"
    TCP = "TCP"
    CALCULATED = "CALCULATED"
    CLOUDWATCH_METRIC = "CLOUDWATCH_METRIC"


@dataclasses.dataclass
class HealthCheckVersionMismatch(ShapeBase):
    """
    The value of `HealthCheckVersion` in the request doesn't match the value of
    `HealthCheckVersion` in the health check.
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

    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class HostedZone(ShapeBase):
    """
    A complex type that contains general information about the hosted zone.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "id",
                "Id",
                TypeInfo(str),
            ),
            (
                "name",
                "Name",
                TypeInfo(str),
            ),
            (
                "caller_reference",
                "CallerReference",
                TypeInfo(str),
            ),
            (
                "config",
                "Config",
                TypeInfo(HostedZoneConfig),
            ),
            (
                "resource_record_set_count",
                "ResourceRecordSetCount",
                TypeInfo(int),
            ),
            (
                "linked_service",
                "LinkedService",
                TypeInfo(LinkedService),
            ),
        ]

    # The ID that Amazon Route 53 assigned to the hosted zone when you created
    # it.
    id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the domain. For public hosted zones, this is the name that you
    # have registered with your DNS registrar.

    # For information about how to specify characters other than `a-z`, `0-9`,
    # and `-` (hyphen) and how to specify internationalized domain names, see
    # CreateHostedZone.
    name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The value that you specified for `CallerReference` when you created the
    # hosted zone.
    caller_reference: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A complex type that includes the `Comment` and `PrivateZone` elements. If
    # you omitted the `HostedZoneConfig` and `Comment` elements from the request,
    # the `Config` and `Comment` elements don't appear in the response.
    config: "HostedZoneConfig" = dataclasses.field(default_factory=dict, )

    # The number of resource record sets in the hosted zone.
    resource_record_set_count: int = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # If the hosted zone was created by another service, the service that created
    # the hosted zone. When a hosted zone is created by another service, you
    # can't edit or delete it using Amazon Route 53.
    linked_service: "LinkedService" = dataclasses.field(default_factory=dict, )


@dataclasses.dataclass
class HostedZoneAlreadyExists(ShapeBase):
    """
    The hosted zone you're trying to create already exists. Amazon Route 53 returns
    this error when a hosted zone has already been created with the specified
    `CallerReference`.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class HostedZoneConfig(ShapeBase):
    """
    A complex type that contains an optional comment about your hosted zone. If you
    don't want to specify a comment, omit both the `HostedZoneConfig` and `Comment`
    elements.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "comment",
                "Comment",
                TypeInfo(str),
            ),
            (
                "private_zone",
                "PrivateZone",
                TypeInfo(bool),
            ),
        ]

    # Any comments that you want to include about the hosted zone.
    comment: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A value that indicates whether this is a private hosted zone.
    private_zone: bool = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class HostedZoneLimit(ShapeBase):
    """
    A complex type that contains the type of limit that you specified in the request
    and the current value for that limit.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "type",
                "Type",
                TypeInfo(HostedZoneLimitType),
            ),
            (
                "value",
                "Value",
                TypeInfo(int),
            ),
        ]

    # The limit that you requested. Valid values include the following:

    #   * **MAX_RRSETS_BY_ZONE** : The maximum number of records that you can create in the specified hosted zone.

    #   * **MAX_VPCS_ASSOCIATED_BY_ZONE** : The maximum number of Amazon VPCs that you can associate with the specified private hosted zone.
    type: "HostedZoneLimitType" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The current value for the limit that is specified by `Type`.
    value: int = dataclasses.field(default=ShapeBase.NOT_SET, )


class HostedZoneLimitType(Enum):
    MAX_RRSETS_BY_ZONE = "MAX_RRSETS_BY_ZONE"
    MAX_VPCS_ASSOCIATED_BY_ZONE = "MAX_VPCS_ASSOCIATED_BY_ZONE"


@dataclasses.dataclass
class HostedZoneNotEmpty(ShapeBase):
    """
    The hosted zone contains resource records that are not SOA or NS records.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class HostedZoneNotFound(ShapeBase):
    """
    The specified HostedZone can't be found.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class HostedZoneNotPrivate(ShapeBase):
    """
    The specified hosted zone is a public hosted zone, not a private hosted zone.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class IncompatibleVersion(ShapeBase):
    """
    The resource you're trying to access is unsupported on this Amazon Route 53
    endpoint.
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

    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class InsufficientCloudWatchLogsResourcePolicy(ShapeBase):
    """
    Amazon Route 53 doesn't have the permissions required to create log streams and
    send query logs to log streams. Possible causes include the following:

      * There is no resource policy that specifies the log group ARN in the value for `Resource`.

      * The resource policy that includes the log group ARN in the value for `Resource` doesn't have the necessary permissions.

      * The resource policy hasn't finished propagating yet.
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

    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


class InsufficientDataHealthStatus(Enum):
    Healthy = "Healthy"
    Unhealthy = "Unhealthy"
    LastKnownStatus = "LastKnownStatus"


@dataclasses.dataclass
class InvalidArgument(ShapeBase):
    """
    Parameter name is invalid.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class InvalidChangeBatch(ShapeBase):
    """
    This exception contains a list of messages that might contain one or more error
    messages. Each error message indicates one error in the change batch.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "messages",
                "messages",
                TypeInfo(typing.List[str]),
            ),
            (
                "message",
                "message",
                TypeInfo(str),
            ),
        ]

    # Descriptive message for the error response.
    messages: typing.List[str] = dataclasses.field(default_factory=list, )
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class InvalidDomainName(ShapeBase):
    """
    The specified domain name is not valid.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class InvalidInput(ShapeBase):
    """
    The input is not valid.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class InvalidPaginationToken(ShapeBase):
    """
    The value that you specified to get the second or subsequent page of results is
    invalid.
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

    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class InvalidTrafficPolicyDocument(ShapeBase):
    """
    The format of the traffic policy document that you specified in the `Document`
    element is invalid.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class InvalidVPCId(ShapeBase):
    """
    The VPC ID that you specified either isn't a valid ID or the current account is
    not authorized to access this VPC.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class LastVPCAssociation(ShapeBase):
    """
    The VPC that you're trying to disassociate from the private hosted zone is the
    last VPC that is associated with the hosted zone. Amazon Route 53 doesn't
    support disassociating the last VPC from a hosted zone.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class LimitsExceeded(ShapeBase):
    """
    This operation can't be completed either because the current account has reached
    the limit on reusable delegation sets that it can create or because you've
    reached the limit on the number of Amazon VPCs that you can associate with a
    private hosted zone. To get the current limit on the number of reusable
    delegation sets, see GetAccountLimit. To get the current limit on the number of
    Amazon VPCs that you can associate with a private hosted zone, see
    GetHostedZoneLimit. To request a higher limit, [create a
    case](http://aws.amazon.com/route53-request) with the AWS Support Center.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class LinkedService(ShapeBase):
    """
    If a health check or hosted zone was created by another service, `LinkedService`
    is a complex type that describes the service that created the resource. When a
    resource is created by another service, you can't edit or delete it using Amazon
    Route 53.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "service_principal",
                "ServicePrincipal",
                TypeInfo(str),
            ),
            (
                "description",
                "Description",
                TypeInfo(str),
            ),
        ]

    # If the health check or hosted zone was created by another service, the
    # service that created the resource. When a resource is created by another
    # service, you can't edit or delete it using Amazon Route 53.
    service_principal: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If the health check or hosted zone was created by another service, an
    # optional description that can be provided by the other service. When a
    # resource is created by another service, you can't edit or delete it using
    # Amazon Route 53.
    description: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListGeoLocationsRequest(ShapeBase):
    """
    A request to get a list of geographic locations that Amazon Route 53 supports
    for geolocation resource record sets.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "start_continent_code",
                "StartContinentCode",
                TypeInfo(str),
            ),
            (
                "start_country_code",
                "StartCountryCode",
                TypeInfo(str),
            ),
            (
                "start_subdivision_code",
                "StartSubdivisionCode",
                TypeInfo(str),
            ),
            (
                "max_items",
                "MaxItems",
                TypeInfo(str),
            ),
        ]

    # The code for the continent with which you want to start listing locations
    # that Amazon Route 53 supports for geolocation. If Amazon Route 53 has
    # already returned a page or more of results, if `IsTruncated` is true, and
    # if `NextContinentCode` from the previous response has a value, enter that
    # value in `StartContinentCode` to return the next page of results.

    # Include `StartContinentCode` only if you want to list continents. Don't
    # include `StartContinentCode` when you're listing countries or countries
    # with their subdivisions.
    start_continent_code: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The code for the country with which you want to start listing locations
    # that Amazon Route 53 supports for geolocation. If Amazon Route 53 has
    # already returned a page or more of results, if `IsTruncated` is `true`, and
    # if `NextCountryCode` from the previous response has a value, enter that
    # value in `StartCountryCode` to return the next page of results.

    # Amazon Route 53 uses the two-letter country codes that are specified in
    # [ISO standard 3166-1
    # alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).
    start_country_code: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The code for the subdivision (for example, state or province) with which
    # you want to start listing locations that Amazon Route 53 supports for
    # geolocation. If Amazon Route 53 has already returned a page or more of
    # results, if `IsTruncated` is `true`, and if `NextSubdivisionCode` from the
    # previous response has a value, enter that value in `StartSubdivisionCode`
    # to return the next page of results.

    # To list subdivisions of a country, you must include both `StartCountryCode`
    # and `StartSubdivisionCode`.
    start_subdivision_code: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # (Optional) The maximum number of geolocations to be included in the
    # response body for this request. If more than `MaxItems` geolocations remain
    # to be listed, then the value of the `IsTruncated` element in the response
    # is `true`.
    max_items: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListGeoLocationsResponse(OutputShapeBase):
    """
    A complex type containing the response information for the request.
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
                "geo_location_details_list",
                "GeoLocationDetailsList",
                TypeInfo(typing.List[GeoLocationDetails]),
            ),
            (
                "is_truncated",
                "IsTruncated",
                TypeInfo(bool),
            ),
            (
                "max_items",
                "MaxItems",
                TypeInfo(str),
            ),
            (
                "next_continent_code",
                "NextContinentCode",
                TypeInfo(str),
            ),
            (
                "next_country_code",
                "NextCountryCode",
                TypeInfo(str),
            ),
            (
                "next_subdivision_code",
                "NextSubdivisionCode",
                TypeInfo(str),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains one `GeoLocationDetails` element for each
    # location that Amazon Route 53 supports for geolocation.
    geo_location_details_list: typing.List["GeoLocationDetails"
                                          ] = dataclasses.field(
                                              default_factory=list,
                                          )

    # A value that indicates whether more locations remain to be listed after the
    # last location in this response. If so, the value of `IsTruncated` is
    # `true`. To get more values, submit another request and include the values
    # of `NextContinentCode`, `NextCountryCode`, and `NextSubdivisionCode` in the
    # `StartContinentCode`, `StartCountryCode`, and `StartSubdivisionCode`, as
    # applicable.
    is_truncated: bool = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The value that you specified for `MaxItems` in the request.
    max_items: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If `IsTruncated` is `true`, you can make a follow-up request to display
    # more locations. Enter the value of `NextContinentCode` in the
    # `StartContinentCode` parameter in another `ListGeoLocations` request.
    next_continent_code: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If `IsTruncated` is `true`, you can make a follow-up request to display
    # more locations. Enter the value of `NextCountryCode` in the
    # `StartCountryCode` parameter in another `ListGeoLocations` request.
    next_country_code: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If `IsTruncated` is `true`, you can make a follow-up request to display
    # more locations. Enter the value of `NextSubdivisionCode` in the
    # `StartSubdivisionCode` parameter in another `ListGeoLocations` request.
    next_subdivision_code: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListHealthChecksRequest(ShapeBase):
    """
    A request to retrieve a list of the health checks that are associated with the
    current AWS account.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "marker",
                "Marker",
                TypeInfo(str),
            ),
            (
                "max_items",
                "MaxItems",
                TypeInfo(str),
            ),
        ]

    # If the value of `IsTruncated` in the previous response was `true`, you have
    # more health checks. To get another group, submit another `ListHealthChecks`
    # request.

    # For the value of `marker`, specify the value of `NextMarker` from the
    # previous response, which is the ID of the first health check that Amazon
    # Route 53 will return if you submit another request.

    # If the value of `IsTruncated` in the previous response was `false`, there
    # are no more health checks to get.
    marker: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The maximum number of health checks that you want `ListHealthChecks` to
    # return in response to the current request. Amazon Route 53 returns a
    # maximum of 100 items. If you set `MaxItems` to a value greater than 100,
    # Amazon Route 53 returns only the first 100 health checks.
    max_items: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListHealthChecksResponse(OutputShapeBase):
    """
    A complex type that contains the response to a `ListHealthChecks` request.
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
                "health_checks",
                "HealthChecks",
                TypeInfo(typing.List[HealthCheck]),
            ),
            (
                "marker",
                "Marker",
                TypeInfo(str),
            ),
            (
                "is_truncated",
                "IsTruncated",
                TypeInfo(bool),
            ),
            (
                "max_items",
                "MaxItems",
                TypeInfo(str),
            ),
            (
                "next_marker",
                "NextMarker",
                TypeInfo(str),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains one `HealthCheck` element for each health
    # check that is associated with the current AWS account.
    health_checks: typing.List["HealthCheck"] = dataclasses.field(
        default_factory=list,
    )

    # For the second and subsequent calls to `ListHealthChecks`, `Marker` is the
    # value that you specified for the `marker` parameter in the previous
    # request.
    marker: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A flag that indicates whether there are more health checks to be listed. If
    # the response was truncated, you can get the next group of health checks by
    # submitting another `ListHealthChecks` request and specifying the value of
    # `NextMarker` in the `marker` parameter.
    is_truncated: bool = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The value that you specified for the `maxitems` parameter in the call to
    # `ListHealthChecks` that produced the current response.
    max_items: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If `IsTruncated` is `true`, the value of `NextMarker` identifies the first
    # health check that Amazon Route 53 returns if you submit another
    # `ListHealthChecks` request and specify the value of `NextMarker` in the
    # `marker` parameter.
    next_marker: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListHostedZonesByNameRequest(ShapeBase):
    """
    Retrieves a list of the public and private hosted zones that are associated with
    the current AWS account in ASCII order by domain name.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "dns_name",
                "DNSName",
                TypeInfo(str),
            ),
            (
                "hosted_zone_id",
                "HostedZoneId",
                TypeInfo(str),
            ),
            (
                "max_items",
                "MaxItems",
                TypeInfo(str),
            ),
        ]

    # (Optional) For your first request to `ListHostedZonesByName`, include the
    # `dnsname` parameter only if you want to specify the name of the first
    # hosted zone in the response. If you don't include the `dnsname` parameter,
    # Amazon Route 53 returns all of the hosted zones that were created by the
    # current AWS account, in ASCII order. For subsequent requests, include both
    # `dnsname` and `hostedzoneid` parameters. For `dnsname`, specify the value
    # of `NextDNSName` from the previous response.
    dns_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # (Optional) For your first request to `ListHostedZonesByName`, do not
    # include the `hostedzoneid` parameter.

    # If you have more hosted zones than the value of `maxitems`,
    # `ListHostedZonesByName` returns only the first `maxitems` hosted zones. To
    # get the next group of `maxitems` hosted zones, submit another request to
    # `ListHostedZonesByName` and include both `dnsname` and `hostedzoneid`
    # parameters. For the value of `hostedzoneid`, specify the value of the
    # `NextHostedZoneId` element from the previous response.
    hosted_zone_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The maximum number of hosted zones to be included in the response body for
    # this request. If you have more than `maxitems` hosted zones, then the value
    # of the `IsTruncated` element in the response is true, and the values of
    # `NextDNSName` and `NextHostedZoneId` specify the first hosted zone in the
    # next group of `maxitems` hosted zones.
    max_items: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListHostedZonesByNameResponse(OutputShapeBase):
    """
    A complex type that contains the response information for the request.
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
                "hosted_zones",
                "HostedZones",
                TypeInfo(typing.List[HostedZone]),
            ),
            (
                "is_truncated",
                "IsTruncated",
                TypeInfo(bool),
            ),
            (
                "max_items",
                "MaxItems",
                TypeInfo(str),
            ),
            (
                "dns_name",
                "DNSName",
                TypeInfo(str),
            ),
            (
                "hosted_zone_id",
                "HostedZoneId",
                TypeInfo(str),
            ),
            (
                "next_dns_name",
                "NextDNSName",
                TypeInfo(str),
            ),
            (
                "next_hosted_zone_id",
                "NextHostedZoneId",
                TypeInfo(str),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains general information about the hosted zone.
    hosted_zones: typing.List["HostedZone"] = dataclasses.field(
        default_factory=list,
    )

    # A flag that indicates whether there are more hosted zones to be listed. If
    # the response was truncated, you can get the next group of `maxitems` hosted
    # zones by calling `ListHostedZonesByName` again and specifying the values of
    # `NextDNSName` and `NextHostedZoneId` elements in the `dnsname` and
    # `hostedzoneid` parameters.
    is_truncated: bool = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The value that you specified for the `maxitems` parameter in the call to
    # `ListHostedZonesByName` that produced the current response.
    max_items: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # For the second and subsequent calls to `ListHostedZonesByName`, `DNSName`
    # is the value that you specified for the `dnsname` parameter in the request
    # that produced the current response.
    dns_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The ID that Amazon Route 53 assigned to the hosted zone when you created
    # it.
    hosted_zone_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If `IsTruncated` is true, the value of `NextDNSName` is the name of the
    # first hosted zone in the next group of `maxitems` hosted zones. Call
    # `ListHostedZonesByName` again and specify the value of `NextDNSName` and
    # `NextHostedZoneId` in the `dnsname` and `hostedzoneid` parameters,
    # respectively.

    # This element is present only if `IsTruncated` is `true`.
    next_dns_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If `IsTruncated` is `true`, the value of `NextHostedZoneId` identifies the
    # first hosted zone in the next group of `maxitems` hosted zones. Call
    # `ListHostedZonesByName` again and specify the value of `NextDNSName` and
    # `NextHostedZoneId` in the `dnsname` and `hostedzoneid` parameters,
    # respectively.

    # This element is present only if `IsTruncated` is `true`.
    next_hosted_zone_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListHostedZonesRequest(ShapeBase):
    """
    A request to retrieve a list of the public and private hosted zones that are
    associated with the current AWS account.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "marker",
                "Marker",
                TypeInfo(str),
            ),
            (
                "max_items",
                "MaxItems",
                TypeInfo(str),
            ),
            (
                "delegation_set_id",
                "DelegationSetId",
                TypeInfo(str),
            ),
        ]

    # If the value of `IsTruncated` in the previous response was `true`, you have
    # more hosted zones. To get more hosted zones, submit another
    # `ListHostedZones` request.

    # For the value of `marker`, specify the value of `NextMarker` from the
    # previous response, which is the ID of the first hosted zone that Amazon
    # Route 53 will return if you submit another request.

    # If the value of `IsTruncated` in the previous response was `false`, there
    # are no more hosted zones to get.
    marker: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # (Optional) The maximum number of hosted zones that you want Amazon Route 53
    # to return. If you have more than `maxitems` hosted zones, the value of
    # `IsTruncated` in the response is `true`, and the value of `NextMarker` is
    # the hosted zone ID of the first hosted zone that Amazon Route 53 will
    # return if you submit another request.
    max_items: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If you're using reusable delegation sets and you want to list all of the
    # hosted zones that are associated with a reusable delegation set, specify
    # the ID of that reusable delegation set.
    delegation_set_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListHostedZonesResponse(OutputShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "hosted_zones",
                "HostedZones",
                TypeInfo(typing.List[HostedZone]),
            ),
            (
                "marker",
                "Marker",
                TypeInfo(str),
            ),
            (
                "is_truncated",
                "IsTruncated",
                TypeInfo(bool),
            ),
            (
                "max_items",
                "MaxItems",
                TypeInfo(str),
            ),
            (
                "next_marker",
                "NextMarker",
                TypeInfo(str),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains general information about the hosted zone.
    hosted_zones: typing.List["HostedZone"] = dataclasses.field(
        default_factory=list,
    )

    # For the second and subsequent calls to `ListHostedZones`, `Marker` is the
    # value that you specified for the `marker` parameter in the request that
    # produced the current response.
    marker: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A flag indicating whether there are more hosted zones to be listed. If the
    # response was truncated, you can get more hosted zones by submitting another
    # `ListHostedZones` request and specifying the value of `NextMarker` in the
    # `marker` parameter.
    is_truncated: bool = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The value that you specified for the `maxitems` parameter in the call to
    # `ListHostedZones` that produced the current response.
    max_items: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If `IsTruncated` is `true`, the value of `NextMarker` identifies the first
    # hosted zone in the next group of hosted zones. Submit another
    # `ListHostedZones` request, and specify the value of `NextMarker` from the
    # response in the `marker` parameter.

    # This element is present only if `IsTruncated` is `true`.
    next_marker: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListQueryLoggingConfigsRequest(ShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "hosted_zone_id",
                "HostedZoneId",
                TypeInfo(str),
            ),
            (
                "next_token",
                "NextToken",
                TypeInfo(str),
            ),
            (
                "max_results",
                "MaxResults",
                TypeInfo(str),
            ),
        ]

    # (Optional) If you want to list the query logging configuration that is
    # associated with a hosted zone, specify the ID in `HostedZoneId`.

    # If you don't specify a hosted zone ID, `ListQueryLoggingConfigs` returns
    # all of the configurations that are associated with the current AWS account.
    hosted_zone_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # (Optional) If the current AWS account has more than `MaxResults` query
    # logging configurations, use `NextToken` to get the second and subsequent
    # pages of results.

    # For the first `ListQueryLoggingConfigs` request, omit this value.

    # For the second and subsequent requests, get the value of `NextToken` from
    # the previous response and specify that value for `NextToken` in the
    # request.
    next_token: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # (Optional) The maximum number of query logging configurations that you want
    # Amazon Route 53 to return in response to the current request. If the
    # current AWS account has more than `MaxResults` configurations, use the
    # value of ListQueryLoggingConfigsResponse$NextToken in the response to get
    # the next page of results.

    # If you don't specify a value for `MaxResults`, Amazon Route 53 returns up
    # to 100 configurations.
    max_results: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListQueryLoggingConfigsResponse(OutputShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "query_logging_configs",
                "QueryLoggingConfigs",
                TypeInfo(typing.List[QueryLoggingConfig]),
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

    # An array that contains one QueryLoggingConfig element for each
    # configuration for DNS query logging that is associated with the current AWS
    # account.
    query_logging_configs: typing.List["QueryLoggingConfig"
                                      ] = dataclasses.field(
                                          default_factory=list,
                                      )

    # If a response includes the last of the query logging configurations that
    # are associated with the current AWS account, `NextToken` doesn't appear in
    # the response.

    # If a response doesn't include the last of the configurations, you can get
    # more configurations by submitting another ListQueryLoggingConfigs request.
    # Get the value of `NextToken` that Amazon Route 53 returned in the previous
    # response and include it in `NextToken` in the next request.
    next_token: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListResourceRecordSetsRequest(ShapeBase):
    """
    A request for the resource record sets that are associated with a specified
    hosted zone.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "hosted_zone_id",
                "HostedZoneId",
                TypeInfo(str),
            ),
            (
                "start_record_name",
                "StartRecordName",
                TypeInfo(str),
            ),
            (
                "start_record_type",
                "StartRecordType",
                TypeInfo(RRType),
            ),
            (
                "start_record_identifier",
                "StartRecordIdentifier",
                TypeInfo(str),
            ),
            (
                "max_items",
                "MaxItems",
                TypeInfo(str),
            ),
        ]

    # The ID of the hosted zone that contains the resource record sets that you
    # want to list.
    hosted_zone_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The first name in the lexicographic ordering of resource record sets that
    # you want to list.
    start_record_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The type of resource record set to begin the record listing from.

    # Valid values for basic resource record sets: `A` | `AAAA` | `CAA` | `CNAME`
    # | `MX` | `NAPTR` | `NS` | `PTR` | `SOA` | `SPF` | `SRV` | `TXT`

    # Values for weighted, latency, geo, and failover resource record sets: `A` |
    # `AAAA` | `CAA` | `CNAME` | `MX` | `NAPTR` | `PTR` | `SPF` | `SRV` | `TXT`

    # Values for alias resource record sets:

    #   * **CloudFront distribution** : A or AAAA

    #   * **Elastic Beanstalk environment that has a regionalized subdomain** : A

    #   * **ELB load balancer** : A | AAAA

    #   * **Amazon S3 bucket** : A

    #   * **Another resource record set in this hosted zone:** The type of the resource record set that the alias references.

    # Constraint: Specifying `type` without specifying `name` returns an
    # `InvalidInput` error.
    start_record_type: "RRType" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # _Weighted resource record sets only:_ If results were truncated for a given
    # DNS name and type, specify the value of `NextRecordIdentifier` from the
    # previous response to get the next resource record set that has the current
    # DNS name and type.
    start_record_identifier: str = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # (Optional) The maximum number of resource records sets to include in the
    # response body for this request. If the response includes more than
    # `maxitems` resource record sets, the value of the `IsTruncated` element in
    # the response is `true`, and the values of the `NextRecordName` and
    # `NextRecordType` elements in the response identify the first resource
    # record set in the next group of `maxitems` resource record sets.
    max_items: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListResourceRecordSetsResponse(OutputShapeBase):
    """
    A complex type that contains list information for the resource record set.
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
                "resource_record_sets",
                "ResourceRecordSets",
                TypeInfo(typing.List[ResourceRecordSet]),
            ),
            (
                "is_truncated",
                "IsTruncated",
                TypeInfo(bool),
            ),
            (
                "max_items",
                "MaxItems",
                TypeInfo(str),
            ),
            (
                "next_record_name",
                "NextRecordName",
                TypeInfo(str),
            ),
            (
                "next_record_type",
                "NextRecordType",
                TypeInfo(RRType),
            ),
            (
                "next_record_identifier",
                "NextRecordIdentifier",
                TypeInfo(str),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # Information about multiple resource record sets.
    resource_record_sets: typing.List["ResourceRecordSet"] = dataclasses.field(
        default_factory=list,
    )

    # A flag that indicates whether more resource record sets remain to be
    # listed. If your results were truncated, you can make a follow-up pagination
    # request by using the `NextRecordName` element.
    is_truncated: bool = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The maximum number of records you requested.
    max_items: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If the results were truncated, the name of the next record in the list.

    # This element is present only if `IsTruncated` is true.
    next_record_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If the results were truncated, the type of the next record in the list.

    # This element is present only if `IsTruncated` is true.
    next_record_type: "RRType" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # _Weighted, latency, geolocation, and failover resource record sets only_ :
    # If results were truncated for a given DNS name and type, the value of
    # `SetIdentifier` for the next resource record set that has the current DNS
    # name and type.
    next_record_identifier: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListReusableDelegationSetsRequest(ShapeBase):
    """
    A request to get a list of the reusable delegation sets that are associated with
    the current AWS account.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "marker",
                "Marker",
                TypeInfo(str),
            ),
            (
                "max_items",
                "MaxItems",
                TypeInfo(str),
            ),
        ]

    # If the value of `IsTruncated` in the previous response was `true`, you have
    # more reusable delegation sets. To get another group, submit another
    # `ListReusableDelegationSets` request.

    # For the value of `marker`, specify the value of `NextMarker` from the
    # previous response, which is the ID of the first reusable delegation set
    # that Amazon Route 53 will return if you submit another request.

    # If the value of `IsTruncated` in the previous response was `false`, there
    # are no more reusable delegation sets to get.
    marker: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The number of reusable delegation sets that you want Amazon Route 53 to
    # return in the response to this request. If you specify a value greater than
    # 100, Amazon Route 53 returns only the first 100 reusable delegation sets.
    max_items: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListReusableDelegationSetsResponse(OutputShapeBase):
    """
    A complex type that contains information about the reusable delegation sets that
    are associated with the current AWS account.
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
                "delegation_sets",
                "DelegationSets",
                TypeInfo(typing.List[DelegationSet]),
            ),
            (
                "marker",
                "Marker",
                TypeInfo(str),
            ),
            (
                "is_truncated",
                "IsTruncated",
                TypeInfo(bool),
            ),
            (
                "max_items",
                "MaxItems",
                TypeInfo(str),
            ),
            (
                "next_marker",
                "NextMarker",
                TypeInfo(str),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains one `DelegationSet` element for each reusable
    # delegation set that was created by the current AWS account.
    delegation_sets: typing.List["DelegationSet"] = dataclasses.field(
        default_factory=list,
    )

    # For the second and subsequent calls to `ListReusableDelegationSets`,
    # `Marker` is the value that you specified for the `marker` parameter in the
    # request that produced the current response.
    marker: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A flag that indicates whether there are more reusable delegation sets to be
    # listed.
    is_truncated: bool = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The value that you specified for the `maxitems` parameter in the call to
    # `ListReusableDelegationSets` that produced the current response.
    max_items: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If `IsTruncated` is `true`, the value of `NextMarker` identifies the next
    # reusable delegation set that Amazon Route 53 will return if you submit
    # another `ListReusableDelegationSets` request and specify the value of
    # `NextMarker` in the `marker` parameter.
    next_marker: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListTagsForResourceRequest(ShapeBase):
    """
    A complex type containing information about a request for a list of the tags
    that are associated with an individual resource.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "resource_type",
                "ResourceType",
                TypeInfo(TagResourceType),
            ),
            (
                "resource_id",
                "ResourceId",
                TypeInfo(str),
            ),
        ]

    # The type of the resource.

    #   * The resource type for health checks is `healthcheck`.

    #   * The resource type for hosted zones is `hostedzone`.
    resource_type: "TagResourceType" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The ID of the resource for which you want to retrieve tags.
    resource_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListTagsForResourceResponse(OutputShapeBase):
    """
    A complex type that contains information about the health checks or hosted zones
    for which you want to list tags.
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
                "resource_tag_set",
                "ResourceTagSet",
                TypeInfo(ResourceTagSet),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A `ResourceTagSet` containing tags associated with the specified resource.
    resource_tag_set: "ResourceTagSet" = dataclasses.field(
        default_factory=dict,
    )


@dataclasses.dataclass
class ListTagsForResourcesRequest(ShapeBase):
    """
    A complex type that contains information about the health checks or hosted zones
    for which you want to list tags.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "resource_type",
                "ResourceType",
                TypeInfo(TagResourceType),
            ),
            (
                "resource_ids",
                "ResourceIds",
                TypeInfo(typing.List[str]),
            ),
        ]

    # The type of the resources.

    #   * The resource type for health checks is `healthcheck`.

    #   * The resource type for hosted zones is `hostedzone`.
    resource_type: "TagResourceType" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains the ResourceId element for each resource for
    # which you want to get a list of tags.
    resource_ids: typing.List[str] = dataclasses.field(default_factory=list, )


@dataclasses.dataclass
class ListTagsForResourcesResponse(OutputShapeBase):
    """
    A complex type containing tags for the specified resources.
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
                "resource_tag_sets",
                "ResourceTagSets",
                TypeInfo(typing.List[ResourceTagSet]),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A list of `ResourceTagSet`s containing tags associated with the specified
    # resources.
    resource_tag_sets: typing.List["ResourceTagSet"] = dataclasses.field(
        default_factory=list,
    )


@dataclasses.dataclass
class ListTrafficPoliciesRequest(ShapeBase):
    """
    A complex type that contains the information about the request to list the
    traffic policies that are associated with the current AWS account.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "traffic_policy_id_marker",
                "TrafficPolicyIdMarker",
                TypeInfo(str),
            ),
            (
                "max_items",
                "MaxItems",
                TypeInfo(str),
            ),
        ]

    # (Conditional) For your first request to `ListTrafficPolicies`, don't
    # include the `TrafficPolicyIdMarker` parameter.

    # If you have more traffic policies than the value of `MaxItems`,
    # `ListTrafficPolicies` returns only the first `MaxItems` traffic policies.
    # To get the next group of policies, submit another request to
    # `ListTrafficPolicies`. For the value of `TrafficPolicyIdMarker`, specify
    # the value of `TrafficPolicyIdMarker` that was returned in the previous
    # response.
    traffic_policy_id_marker: str = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # (Optional) The maximum number of traffic policies that you want Amazon
    # Route 53 to return in response to this request. If you have more than
    # `MaxItems` traffic policies, the value of `IsTruncated` in the response is
    # `true`, and the value of `TrafficPolicyIdMarker` is the ID of the first
    # traffic policy that Amazon Route 53 will return if you submit another
    # request.
    max_items: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListTrafficPoliciesResponse(OutputShapeBase):
    """
    A complex type that contains the response information for the request.
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
                "traffic_policy_summaries",
                "TrafficPolicySummaries",
                TypeInfo(typing.List[TrafficPolicySummary]),
            ),
            (
                "is_truncated",
                "IsTruncated",
                TypeInfo(bool),
            ),
            (
                "traffic_policy_id_marker",
                "TrafficPolicyIdMarker",
                TypeInfo(str),
            ),
            (
                "max_items",
                "MaxItems",
                TypeInfo(str),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A list that contains one `TrafficPolicySummary` element for each traffic
    # policy that was created by the current AWS account.
    traffic_policy_summaries: typing.List["TrafficPolicySummary"
                                         ] = dataclasses.field(
                                             default_factory=list,
                                         )

    # A flag that indicates whether there are more traffic policies to be listed.
    # If the response was truncated, you can get the next group of traffic
    # policies by submitting another `ListTrafficPolicies` request and specifying
    # the value of `TrafficPolicyIdMarker` in the `TrafficPolicyIdMarker` request
    # parameter.
    is_truncated: bool = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If the value of `IsTruncated` is `true`, `TrafficPolicyIdMarker` is the ID
    # of the first traffic policy in the next group of `MaxItems` traffic
    # policies.
    traffic_policy_id_marker: str = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The value that you specified for the `MaxItems` parameter in the
    # `ListTrafficPolicies` request that produced the current response.
    max_items: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListTrafficPolicyInstancesByHostedZoneRequest(ShapeBase):
    """
    A request for the traffic policy instances that you created in a specified
    hosted zone.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "hosted_zone_id",
                "HostedZoneId",
                TypeInfo(str),
            ),
            (
                "traffic_policy_instance_name_marker",
                "TrafficPolicyInstanceNameMarker",
                TypeInfo(str),
            ),
            (
                "traffic_policy_instance_type_marker",
                "TrafficPolicyInstanceTypeMarker",
                TypeInfo(RRType),
            ),
            (
                "max_items",
                "MaxItems",
                TypeInfo(str),
            ),
        ]

    # The ID of the hosted zone that you want to list traffic policy instances
    # for.
    hosted_zone_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If the value of `IsTruncated` in the previous response is true, you have
    # more traffic policy instances. To get more traffic policy instances, submit
    # another `ListTrafficPolicyInstances` request. For the value of
    # `trafficpolicyinstancename`, specify the value of
    # `TrafficPolicyInstanceNameMarker` from the previous response, which is the
    # name of the first traffic policy instance in the next group of traffic
    # policy instances.

    # If the value of `IsTruncated` in the previous response was `false`, there
    # are no more traffic policy instances to get.
    traffic_policy_instance_name_marker: str = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # If the value of `IsTruncated` in the previous response is true, you have
    # more traffic policy instances. To get more traffic policy instances, submit
    # another `ListTrafficPolicyInstances` request. For the value of
    # `trafficpolicyinstancetype`, specify the value of
    # `TrafficPolicyInstanceTypeMarker` from the previous response, which is the
    # type of the first traffic policy instance in the next group of traffic
    # policy instances.

    # If the value of `IsTruncated` in the previous response was `false`, there
    # are no more traffic policy instances to get.
    traffic_policy_instance_type_marker: "RRType" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The maximum number of traffic policy instances to be included in the
    # response body for this request. If you have more than `MaxItems` traffic
    # policy instances, the value of the `IsTruncated` element in the response is
    # `true`, and the values of `HostedZoneIdMarker`,
    # `TrafficPolicyInstanceNameMarker`, and `TrafficPolicyInstanceTypeMarker`
    # represent the first traffic policy instance that Amazon Route 53 will
    # return if you submit another request.
    max_items: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListTrafficPolicyInstancesByHostedZoneResponse(OutputShapeBase):
    """
    A complex type that contains the response information for the request.
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
                "traffic_policy_instances",
                "TrafficPolicyInstances",
                TypeInfo(typing.List[TrafficPolicyInstance]),
            ),
            (
                "is_truncated",
                "IsTruncated",
                TypeInfo(bool),
            ),
            (
                "max_items",
                "MaxItems",
                TypeInfo(str),
            ),
            (
                "traffic_policy_instance_name_marker",
                "TrafficPolicyInstanceNameMarker",
                TypeInfo(str),
            ),
            (
                "traffic_policy_instance_type_marker",
                "TrafficPolicyInstanceTypeMarker",
                TypeInfo(RRType),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A list that contains one `TrafficPolicyInstance` element for each traffic
    # policy instance that matches the elements in the request.
    traffic_policy_instances: typing.List["TrafficPolicyInstance"
                                         ] = dataclasses.field(
                                             default_factory=list,
                                         )

    # A flag that indicates whether there are more traffic policy instances to be
    # listed. If the response was truncated, you can get the next group of
    # traffic policy instances by submitting another
    # `ListTrafficPolicyInstancesByHostedZone` request and specifying the values
    # of `HostedZoneIdMarker`, `TrafficPolicyInstanceNameMarker`, and
    # `TrafficPolicyInstanceTypeMarker` in the corresponding request parameters.
    is_truncated: bool = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The value that you specified for the `MaxItems` parameter in the
    # `ListTrafficPolicyInstancesByHostedZone` request that produced the current
    # response.
    max_items: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If `IsTruncated` is `true`, `TrafficPolicyInstanceNameMarker` is the name
    # of the first traffic policy instance in the next group of traffic policy
    # instances.
    traffic_policy_instance_name_marker: str = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # If `IsTruncated` is true, `TrafficPolicyInstanceTypeMarker` is the DNS type
    # of the resource record sets that are associated with the first traffic
    # policy instance in the next group of traffic policy instances.
    traffic_policy_instance_type_marker: "RRType" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


@dataclasses.dataclass
class ListTrafficPolicyInstancesByPolicyRequest(ShapeBase):
    """
    A complex type that contains the information about the request to list your
    traffic policy instances.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "traffic_policy_id",
                "TrafficPolicyId",
                TypeInfo(str),
            ),
            (
                "traffic_policy_version",
                "TrafficPolicyVersion",
                TypeInfo(int),
            ),
            (
                "hosted_zone_id_marker",
                "HostedZoneIdMarker",
                TypeInfo(str),
            ),
            (
                "traffic_policy_instance_name_marker",
                "TrafficPolicyInstanceNameMarker",
                TypeInfo(str),
            ),
            (
                "traffic_policy_instance_type_marker",
                "TrafficPolicyInstanceTypeMarker",
                TypeInfo(RRType),
            ),
            (
                "max_items",
                "MaxItems",
                TypeInfo(str),
            ),
        ]

    # The ID of the traffic policy for which you want to list traffic policy
    # instances.
    traffic_policy_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The version of the traffic policy for which you want to list traffic policy
    # instances. The version must be associated with the traffic policy that is
    # specified by `TrafficPolicyId`.
    traffic_policy_version: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If the value of `IsTruncated` in the previous response was `true`, you have
    # more traffic policy instances. To get more traffic policy instances, submit
    # another `ListTrafficPolicyInstancesByPolicy` request.

    # For the value of `hostedzoneid`, specify the value of `HostedZoneIdMarker`
    # from the previous response, which is the hosted zone ID of the first
    # traffic policy instance that Amazon Route 53 will return if you submit
    # another request.

    # If the value of `IsTruncated` in the previous response was `false`, there
    # are no more traffic policy instances to get.
    hosted_zone_id_marker: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If the value of `IsTruncated` in the previous response was `true`, you have
    # more traffic policy instances. To get more traffic policy instances, submit
    # another `ListTrafficPolicyInstancesByPolicy` request.

    # For the value of `trafficpolicyinstancename`, specify the value of
    # `TrafficPolicyInstanceNameMarker` from the previous response, which is the
    # name of the first traffic policy instance that Amazon Route 53 will return
    # if you submit another request.

    # If the value of `IsTruncated` in the previous response was `false`, there
    # are no more traffic policy instances to get.
    traffic_policy_instance_name_marker: str = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # If the value of `IsTruncated` in the previous response was `true`, you have
    # more traffic policy instances. To get more traffic policy instances, submit
    # another `ListTrafficPolicyInstancesByPolicy` request.

    # For the value of `trafficpolicyinstancetype`, specify the value of
    # `TrafficPolicyInstanceTypeMarker` from the previous response, which is the
    # name of the first traffic policy instance that Amazon Route 53 will return
    # if you submit another request.

    # If the value of `IsTruncated` in the previous response was `false`, there
    # are no more traffic policy instances to get.
    traffic_policy_instance_type_marker: "RRType" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The maximum number of traffic policy instances to be included in the
    # response body for this request. If you have more than `MaxItems` traffic
    # policy instances, the value of the `IsTruncated` element in the response is
    # `true`, and the values of `HostedZoneIdMarker`,
    # `TrafficPolicyInstanceNameMarker`, and `TrafficPolicyInstanceTypeMarker`
    # represent the first traffic policy instance that Amazon Route 53 will
    # return if you submit another request.
    max_items: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListTrafficPolicyInstancesByPolicyResponse(OutputShapeBase):
    """
    A complex type that contains the response information for the request.
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
                "traffic_policy_instances",
                "TrafficPolicyInstances",
                TypeInfo(typing.List[TrafficPolicyInstance]),
            ),
            (
                "is_truncated",
                "IsTruncated",
                TypeInfo(bool),
            ),
            (
                "max_items",
                "MaxItems",
                TypeInfo(str),
            ),
            (
                "hosted_zone_id_marker",
                "HostedZoneIdMarker",
                TypeInfo(str),
            ),
            (
                "traffic_policy_instance_name_marker",
                "TrafficPolicyInstanceNameMarker",
                TypeInfo(str),
            ),
            (
                "traffic_policy_instance_type_marker",
                "TrafficPolicyInstanceTypeMarker",
                TypeInfo(RRType),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A list that contains one `TrafficPolicyInstance` element for each traffic
    # policy instance that matches the elements in the request.
    traffic_policy_instances: typing.List["TrafficPolicyInstance"
                                         ] = dataclasses.field(
                                             default_factory=list,
                                         )

    # A flag that indicates whether there are more traffic policy instances to be
    # listed. If the response was truncated, you can get the next group of
    # traffic policy instances by calling `ListTrafficPolicyInstancesByPolicy`
    # again and specifying the values of the `HostedZoneIdMarker`,
    # `TrafficPolicyInstanceNameMarker`, and `TrafficPolicyInstanceTypeMarker`
    # elements in the corresponding request parameters.
    is_truncated: bool = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The value that you specified for the `MaxItems` parameter in the call to
    # `ListTrafficPolicyInstancesByPolicy` that produced the current response.
    max_items: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If `IsTruncated` is `true`, `HostedZoneIdMarker` is the ID of the hosted
    # zone of the first traffic policy instance in the next group of traffic
    # policy instances.
    hosted_zone_id_marker: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If `IsTruncated` is `true`, `TrafficPolicyInstanceNameMarker` is the name
    # of the first traffic policy instance in the next group of `MaxItems`
    # traffic policy instances.
    traffic_policy_instance_name_marker: str = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # If `IsTruncated` is `true`, `TrafficPolicyInstanceTypeMarker` is the DNS
    # type of the resource record sets that are associated with the first traffic
    # policy instance in the next group of `MaxItems` traffic policy instances.
    traffic_policy_instance_type_marker: "RRType" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


@dataclasses.dataclass
class ListTrafficPolicyInstancesRequest(ShapeBase):
    """
    A request to get information about the traffic policy instances that you created
    by using the current AWS account.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "hosted_zone_id_marker",
                "HostedZoneIdMarker",
                TypeInfo(str),
            ),
            (
                "traffic_policy_instance_name_marker",
                "TrafficPolicyInstanceNameMarker",
                TypeInfo(str),
            ),
            (
                "traffic_policy_instance_type_marker",
                "TrafficPolicyInstanceTypeMarker",
                TypeInfo(RRType),
            ),
            (
                "max_items",
                "MaxItems",
                TypeInfo(str),
            ),
        ]

    # If the value of `IsTruncated` in the previous response was `true`, you have
    # more traffic policy instances. To get more traffic policy instances, submit
    # another `ListTrafficPolicyInstances` request. For the value of
    # `HostedZoneId`, specify the value of `HostedZoneIdMarker` from the previous
    # response, which is the hosted zone ID of the first traffic policy instance
    # in the next group of traffic policy instances.

    # If the value of `IsTruncated` in the previous response was `false`, there
    # are no more traffic policy instances to get.
    hosted_zone_id_marker: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If the value of `IsTruncated` in the previous response was `true`, you have
    # more traffic policy instances. To get more traffic policy instances, submit
    # another `ListTrafficPolicyInstances` request. For the value of
    # `trafficpolicyinstancename`, specify the value of
    # `TrafficPolicyInstanceNameMarker` from the previous response, which is the
    # name of the first traffic policy instance in the next group of traffic
    # policy instances.

    # If the value of `IsTruncated` in the previous response was `false`, there
    # are no more traffic policy instances to get.
    traffic_policy_instance_name_marker: str = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # If the value of `IsTruncated` in the previous response was `true`, you have
    # more traffic policy instances. To get more traffic policy instances, submit
    # another `ListTrafficPolicyInstances` request. For the value of
    # `trafficpolicyinstancetype`, specify the value of
    # `TrafficPolicyInstanceTypeMarker` from the previous response, which is the
    # type of the first traffic policy instance in the next group of traffic
    # policy instances.

    # If the value of `IsTruncated` in the previous response was `false`, there
    # are no more traffic policy instances to get.
    traffic_policy_instance_type_marker: "RRType" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The maximum number of traffic policy instances that you want Amazon Route
    # 53 to return in response to a `ListTrafficPolicyInstances` request. If you
    # have more than `MaxItems` traffic policy instances, the value of the
    # `IsTruncated` element in the response is `true`, and the values of
    # `HostedZoneIdMarker`, `TrafficPolicyInstanceNameMarker`, and
    # `TrafficPolicyInstanceTypeMarker` represent the first traffic policy
    # instance in the next group of `MaxItems` traffic policy instances.
    max_items: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListTrafficPolicyInstancesResponse(OutputShapeBase):
    """
    A complex type that contains the response information for the request.
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
                "traffic_policy_instances",
                "TrafficPolicyInstances",
                TypeInfo(typing.List[TrafficPolicyInstance]),
            ),
            (
                "is_truncated",
                "IsTruncated",
                TypeInfo(bool),
            ),
            (
                "max_items",
                "MaxItems",
                TypeInfo(str),
            ),
            (
                "hosted_zone_id_marker",
                "HostedZoneIdMarker",
                TypeInfo(str),
            ),
            (
                "traffic_policy_instance_name_marker",
                "TrafficPolicyInstanceNameMarker",
                TypeInfo(str),
            ),
            (
                "traffic_policy_instance_type_marker",
                "TrafficPolicyInstanceTypeMarker",
                TypeInfo(RRType),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A list that contains one `TrafficPolicyInstance` element for each traffic
    # policy instance that matches the elements in the request.
    traffic_policy_instances: typing.List["TrafficPolicyInstance"
                                         ] = dataclasses.field(
                                             default_factory=list,
                                         )

    # A flag that indicates whether there are more traffic policy instances to be
    # listed. If the response was truncated, you can get more traffic policy
    # instances by calling `ListTrafficPolicyInstances` again and specifying the
    # values of the `HostedZoneIdMarker`, `TrafficPolicyInstanceNameMarker`, and
    # `TrafficPolicyInstanceTypeMarker` in the corresponding request parameters.
    is_truncated: bool = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The value that you specified for the `MaxItems` parameter in the call to
    # `ListTrafficPolicyInstances` that produced the current response.
    max_items: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If `IsTruncated` is `true`, `HostedZoneIdMarker` is the ID of the hosted
    # zone of the first traffic policy instance that Amazon Route 53 will return
    # if you submit another `ListTrafficPolicyInstances` request.
    hosted_zone_id_marker: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If `IsTruncated` is `true`, `TrafficPolicyInstanceNameMarker` is the name
    # of the first traffic policy instance that Amazon Route 53 will return if
    # you submit another `ListTrafficPolicyInstances` request.
    traffic_policy_instance_name_marker: str = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # If `IsTruncated` is `true`, `TrafficPolicyInstanceTypeMarker` is the DNS
    # type of the resource record sets that are associated with the first traffic
    # policy instance that Amazon Route 53 will return if you submit another
    # `ListTrafficPolicyInstances` request.
    traffic_policy_instance_type_marker: "RRType" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


@dataclasses.dataclass
class ListTrafficPolicyVersionsRequest(ShapeBase):
    """
    A complex type that contains the information about the request to list your
    traffic policies.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "id",
                "Id",
                TypeInfo(str),
            ),
            (
                "traffic_policy_version_marker",
                "TrafficPolicyVersionMarker",
                TypeInfo(str),
            ),
            (
                "max_items",
                "MaxItems",
                TypeInfo(str),
            ),
        ]

    # Specify the value of `Id` of the traffic policy for which you want to list
    # all versions.
    id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # For your first request to `ListTrafficPolicyVersions`, don't include the
    # `TrafficPolicyVersionMarker` parameter.

    # If you have more traffic policy versions than the value of `MaxItems`,
    # `ListTrafficPolicyVersions` returns only the first group of `MaxItems`
    # versions. To get more traffic policy versions, submit another
    # `ListTrafficPolicyVersions` request. For the value of
    # `TrafficPolicyVersionMarker`, specify the value of
    # `TrafficPolicyVersionMarker` in the previous response.
    traffic_policy_version_marker: str = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The maximum number of traffic policy versions that you want Amazon Route 53
    # to include in the response body for this request. If the specified traffic
    # policy has more than `MaxItems` versions, the value of `IsTruncated` in the
    # response is `true`, and the value of the `TrafficPolicyVersionMarker`
    # element is the ID of the first version that Amazon Route 53 will return if
    # you submit another request.
    max_items: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListTrafficPolicyVersionsResponse(OutputShapeBase):
    """
    A complex type that contains the response information for the request.
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
                "traffic_policies",
                "TrafficPolicies",
                TypeInfo(typing.List[TrafficPolicy]),
            ),
            (
                "is_truncated",
                "IsTruncated",
                TypeInfo(bool),
            ),
            (
                "traffic_policy_version_marker",
                "TrafficPolicyVersionMarker",
                TypeInfo(str),
            ),
            (
                "max_items",
                "MaxItems",
                TypeInfo(str),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A list that contains one `TrafficPolicy` element for each traffic policy
    # version that is associated with the specified traffic policy.
    traffic_policies: typing.List["TrafficPolicy"] = dataclasses.field(
        default_factory=list,
    )

    # A flag that indicates whether there are more traffic policies to be listed.
    # If the response was truncated, you can get the next group of traffic
    # policies by submitting another `ListTrafficPolicyVersions` request and
    # specifying the value of `NextMarker` in the `marker` parameter.
    is_truncated: bool = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If `IsTruncated` is `true`, the value of `TrafficPolicyVersionMarker`
    # identifies the first traffic policy that Amazon Route 53 will return if you
    # submit another request. Call `ListTrafficPolicyVersions` again and specify
    # the value of `TrafficPolicyVersionMarker` in the
    # `TrafficPolicyVersionMarker` request parameter.

    # This element is present only if `IsTruncated` is `true`.
    traffic_policy_version_marker: str = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The value that you specified for the `maxitems` parameter in the
    # `ListTrafficPolicyVersions` request that produced the current response.
    max_items: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListVPCAssociationAuthorizationsRequest(ShapeBase):
    """
    A complex type that contains information about that can be associated with your
    hosted zone.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "hosted_zone_id",
                "HostedZoneId",
                TypeInfo(str),
            ),
            (
                "next_token",
                "NextToken",
                TypeInfo(str),
            ),
            (
                "max_results",
                "MaxResults",
                TypeInfo(str),
            ),
        ]

    # The ID of the hosted zone for which you want a list of VPCs that can be
    # associated with the hosted zone.
    hosted_zone_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # _Optional_ : If a response includes a `NextToken` element, there are more
    # VPCs that can be associated with the specified hosted zone. To get the next
    # page of results, submit another request, and include the value of
    # `NextToken` from the response in the `nexttoken` parameter in another
    # `ListVPCAssociationAuthorizations` request.
    next_token: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # _Optional_ : An integer that specifies the maximum number of VPCs that you
    # want Amazon Route 53 to return. If you don't specify a value for
    # `MaxResults`, Amazon Route 53 returns up to 50 VPCs per page.
    max_results: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ListVPCAssociationAuthorizationsResponse(OutputShapeBase):
    """
    A complex type that contains the response information for the request.
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
                "hosted_zone_id",
                "HostedZoneId",
                TypeInfo(str),
            ),
            (
                "_vpcs",
                "VPCs",
                TypeInfo(typing.List[VPC]),
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

    # The ID of the hosted zone that you can associate the listed VPCs with.
    hosted_zone_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The list of VPCs that are authorized to be associated with the specified
    # hosted zone.
    _vpcs: typing.List["VPC"] = dataclasses.field(default_factory=list, )

    # When the response includes a `NextToken` element, there are more VPCs that
    # can be associated with the specified hosted zone. To get the next page of
    # VPCs, submit another `ListVPCAssociationAuthorizations` request, and
    # include the value of the `NextToken` element from the response in the
    # `nexttoken` request parameter.
    next_token: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class NoSuchChange(ShapeBase):
    """
    A change with the specified change ID does not exist.
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

    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class NoSuchCloudWatchLogsLogGroup(ShapeBase):
    """
    There is no CloudWatch Logs log group with the specified ARN.
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

    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class NoSuchDelegationSet(ShapeBase):
    """
    A reusable delegation set with the specified ID does not exist.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class NoSuchGeoLocation(ShapeBase):
    """
    Amazon Route 53 doesn't support the specified geolocation.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class NoSuchHealthCheck(ShapeBase):
    """
    No health check exists with the ID that you specified in the `DeleteHealthCheck`
    request.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class NoSuchHostedZone(ShapeBase):
    """
    No hosted zone exists with the ID that you specified.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class NoSuchQueryLoggingConfig(ShapeBase):
    """
    There is no DNS query logging configuration with the specified ID.
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

    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class NoSuchTrafficPolicy(ShapeBase):
    """
    No traffic policy exists with the specified ID.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class NoSuchTrafficPolicyInstance(ShapeBase):
    """
    No traffic policy instance exists with the specified ID.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class NotAuthorizedException(ShapeBase):
    """
    Associating the specified VPC with the specified hosted zone has not been
    authorized.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class PriorRequestNotComplete(ShapeBase):
    """
    If Amazon Route 53 can't process a request before the next request arrives, it
    will reject subsequent requests for the same hosted zone and return an `HTTP 400
    error` (`Bad request`). If Amazon Route 53 returns this error repeatedly for the
    same request, we recommend that you wait, in intervals of increasing duration,
    before you try the request again.
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

    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class PublicZoneVPCAssociation(ShapeBase):
    """
    You're trying to associate a VPC with a public hosted zone. Amazon Route 53
    doesn't support associating a VPC with a public hosted zone.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class QueryLoggingConfig(ShapeBase):
    """
    A complex type that contains information about a configuration for DNS query
    logging.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "id",
                "Id",
                TypeInfo(str),
            ),
            (
                "hosted_zone_id",
                "HostedZoneId",
                TypeInfo(str),
            ),
            (
                "cloud_watch_logs_log_group_arn",
                "CloudWatchLogsLogGroupArn",
                TypeInfo(str),
            ),
        ]

    # The ID for a configuration for DNS query logging.
    id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The ID of the hosted zone that CloudWatch Logs is logging queries for.
    hosted_zone_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The Amazon Resource Name (ARN) of the CloudWatch Logs log group that Amazon
    # Route 53 is publishing logs to.
    cloud_watch_logs_log_group_arn: str = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


@dataclasses.dataclass
class QueryLoggingConfigAlreadyExists(ShapeBase):
    """
    You can create only one query logging configuration for a hosted zone, and a
    query logging configuration already exists for this hosted zone.
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

    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


class RRType(Enum):
    SOA = "SOA"
    A = "A"
    TXT = "TXT"
    NS = "NS"
    CNAME = "CNAME"
    MX = "MX"
    NAPTR = "NAPTR"
    PTR = "PTR"
    SRV = "SRV"
    SPF = "SPF"
    AAAA = "AAAA"
    CAA = "CAA"


class ResettableElementName(Enum):
    FullyQualifiedDomainName = "FullyQualifiedDomainName"
    Regions = "Regions"
    ResourcePath = "ResourcePath"
    ChildHealthChecks = "ChildHealthChecks"


@dataclasses.dataclass
class ResourceRecord(ShapeBase):
    """
    Information specific to the resource record.

    If you're creating an alias resource record set, omit `ResourceRecord`.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "value",
                "Value",
                TypeInfo(str),
            ),
        ]

    # The current or new DNS record value, not to exceed 4,000 characters. In the
    # case of a `DELETE` action, if the current value does not match the actual
    # value, an error is returned. For descriptions about how to format `Value`
    # for different record types, see [Supported DNS Resource Record
    # Types](http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/ResourceRecordTypes.html)
    # in the _Amazon Route 53 Developer Guide_.

    # You can specify more than one value for all record types except `CNAME` and
    # `SOA`.

    # If you're creating an alias resource record set, omit `Value`.
    value: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ResourceRecordSet(ShapeBase):
    """
    Information about the resource record set to create or delete.
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
                TypeInfo(RRType),
            ),
            (
                "set_identifier",
                "SetIdentifier",
                TypeInfo(str),
            ),
            (
                "weight",
                "Weight",
                TypeInfo(int),
            ),
            (
                "region",
                "Region",
                TypeInfo(ResourceRecordSetRegion),
            ),
            (
                "geo_location",
                "GeoLocation",
                TypeInfo(GeoLocation),
            ),
            (
                "failover",
                "Failover",
                TypeInfo(ResourceRecordSetFailover),
            ),
            (
                "multi_value_answer",
                "MultiValueAnswer",
                TypeInfo(bool),
            ),
            (
                "ttl",
                "TTL",
                TypeInfo(int),
            ),
            (
                "resource_records",
                "ResourceRecords",
                TypeInfo(typing.List[ResourceRecord]),
            ),
            (
                "alias_target",
                "AliasTarget",
                TypeInfo(AliasTarget),
            ),
            (
                "health_check_id",
                "HealthCheckId",
                TypeInfo(str),
            ),
            (
                "traffic_policy_instance_id",
                "TrafficPolicyInstanceId",
                TypeInfo(str),
            ),
        ]

    # The name of the domain you want to perform the action on.

    # Enter a fully qualified domain name, for example, `www.example.com`. You
    # can optionally include a trailing dot. If you omit the trailing dot, Amazon
    # Route 53 still assumes that the domain name that you specify is fully
    # qualified. This means that Amazon Route 53 treats `www.example.com`
    # (without a trailing dot) and `www.example.com.` (with a trailing dot) as
    # identical.

    # For information about how to specify characters other than `a-z`, `0-9`,
    # and `-` (hyphen) and how to specify internationalized domain names, see
    # [DNS Domain Name
    # Format](http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/DomainNameFormat.html)
    # in the _Amazon Route 53 Developer Guide_.

    # You can use the asterisk (*) wildcard to replace the leftmost label in a
    # domain name, for example, `*.example.com`. Note the following:

    #   * The * must replace the entire label. For example, you can't specify `*prod.example.com` or `prod*.example.com`.

    #   * The * can't replace any of the middle labels, for example, marketing.*.example.com.

    #   * If you include * in any position other than the leftmost label in a domain name, DNS treats it as an * character (ASCII 42), not as a wildcard.

    # You can't use the * wildcard for resource records sets that have a type of
    # NS.

    # You can use the * wildcard as the leftmost label in a domain name, for
    # example, `*.example.com`. You can't use an * for one of the middle labels,
    # for example, `marketing.*.example.com`. In addition, the * must replace the
    # entire label; for example, you can't specify `prod*.example.com`.
    name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The DNS record type. For information about different record types and how
    # data is encoded for them, see [Supported DNS Resource Record
    # Types](http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/ResourceRecordTypes.html)
    # in the _Amazon Route 53 Developer Guide_.

    # Valid values for basic resource record sets: `A` | `AAAA` | `CAA` | `CNAME`
    # | `MX` | `NAPTR` | `NS` | `PTR` | `SOA` | `SPF` | `SRV` | `TXT`

    # Values for weighted, latency, geolocation, and failover resource record
    # sets: `A` | `AAAA` | `CAA` | `CNAME` | `MX` | `NAPTR` | `PTR` | `SPF` |
    # `SRV` | `TXT`. When creating a group of weighted, latency, geolocation, or
    # failover resource record sets, specify the same value for all of the
    # resource record sets in the group.

    # Valid values for multivalue answer resource record sets: `A` | `AAAA` |
    # `MX` | `NAPTR` | `PTR` | `SPF` | `SRV` | `TXT`

    # SPF records were formerly used to verify the identity of the sender of
    # email messages. However, we no longer recommend that you create resource
    # record sets for which the value of `Type` is `SPF`. RFC 7208, _Sender
    # Policy Framework (SPF) for Authorizing Use of Domains in Email, Version 1_
    # , has been updated to say, "...[I]ts existence and mechanism defined in
    # [RFC4408] have led to some interoperability issues. Accordingly, its use is
    # no longer appropriate for SPF version 1; implementations are not to use
    # it." In RFC 7208, see section 14.1, [The SPF DNS Record
    # Type](http://tools.ietf.org/html/rfc7208#section-14.1).

    # Values for alias resource record sets:

    #   * **CloudFront distributions:** `A`

    # If IPv6 is enabled for the distribution, create two resource record sets to
    # route traffic to your distribution, one with a value of `A` and one with a
    # value of `AAAA`.

    #   * **AWS Elastic Beanstalk environment that has a regionalized subdomain** : `A`

    #   * **ELB load balancers:** `A` | `AAAA`

    #   * **Amazon S3 buckets:** `A`

    #   * **Another resource record set in this hosted zone:** Specify the type of the resource record set that you're creating the alias for. All values are supported except `NS` and `SOA`.
    type: "RRType" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # _Weighted, Latency, Geo, and Failover resource record sets only:_ An
    # identifier that differentiates among multiple resource record sets that
    # have the same combination of DNS name and type. The value of
    # `SetIdentifier` must be unique for each resource record set that has the
    # same combination of DNS name and type. Omit `SetIdentifier` for any other
    # types of record sets.
    set_identifier: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # _Weighted resource record sets only:_ Among resource record sets that have
    # the same combination of DNS name and type, a value that determines the
    # proportion of DNS queries that Amazon Route 53 responds to using the
    # current resource record set. Amazon Route 53 calculates the sum of the
    # weights for the resource record sets that have the same combination of DNS
    # name and type. Amazon Route 53 then responds to queries based on the ratio
    # of a resource's weight to the total. Note the following:

    #   * You must specify a value for the `Weight` element for every weighted resource record set.

    #   * You can only specify one `ResourceRecord` per weighted resource record set.

    #   * You can't create latency, failover, or geolocation resource record sets that have the same values for the `Name` and `Type` elements as weighted resource record sets.

    #   * You can create a maximum of 100 weighted resource record sets that have the same values for the `Name` and `Type` elements.

    #   * For weighted (but not weighted alias) resource record sets, if you set `Weight` to `0` for a resource record set, Amazon Route 53 never responds to queries with the applicable value for that resource record set. However, if you set `Weight` to `0` for all resource record sets that have the same combination of DNS name and type, traffic is routed to all resources with equal probability.

    # The effect of setting `Weight` to `0` is different when you associate
    # health checks with weighted resource record sets. For more information, see
    # [Options for Configuring Amazon Route 53 Active-Active and Active-Passive
    # Failover](http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-
    # failover-configuring-options.html) in the _Amazon Route 53 Developer
    # Guide_.
    weight: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # _Latency-based resource record sets only:_ The Amazon EC2 Region where you
    # created the resource that this resource record set refers to. The resource
    # typically is an AWS resource, such as an EC2 instance or an ELB load
    # balancer, and is referred to by an IP address or a DNS domain name,
    # depending on the record type.

    # Creating latency and latency alias resource record sets in private hosted
    # zones is not supported.

    # When Amazon Route 53 receives a DNS query for a domain name and type for
    # which you have created latency resource record sets, Amazon Route 53
    # selects the latency resource record set that has the lowest latency between
    # the end user and the associated Amazon EC2 Region. Amazon Route 53 then
    # returns the value that is associated with the selected resource record set.

    # Note the following:

    #   * You can only specify one `ResourceRecord` per latency resource record set.

    #   * You can only create one latency resource record set for each Amazon EC2 Region.

    #   * You aren't required to create latency resource record sets for all Amazon EC2 Regions. Amazon Route 53 will choose the region with the best latency from among the regions that you create latency resource record sets for.

    #   * You can't create non-latency resource record sets that have the same values for the `Name` and `Type` elements as latency resource record sets.
    region: "ResourceRecordSetRegion" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # _Geo location resource record sets only:_ A complex type that lets you
    # control how Amazon Route 53 responds to DNS queries based on the geographic
    # origin of the query. For example, if you want all queries from Africa to be
    # routed to a web server with an IP address of `192.0.2.111`, create a
    # resource record set with a `Type` of `A` and a `ContinentCode` of `AF`.

    # Creating geolocation and geolocation alias resource record sets in private
    # hosted zones is not supported.

    # If you create separate resource record sets for overlapping geographic
    # regions (for example, one resource record set for a continent and one for a
    # country on the same continent), priority goes to the smallest geographic
    # region. This allows you to route most queries for a continent to one
    # resource and to route queries for a country on that continent to a
    # different resource.

    # You can't create two geolocation resource record sets that specify the same
    # geographic location.

    # The value `*` in the `CountryCode` element matches all geographic locations
    # that aren't specified in other geolocation resource record sets that have
    # the same values for the `Name` and `Type` elements.

    # Geolocation works by mapping IP addresses to locations. However, some IP
    # addresses aren't mapped to geographic locations, so even if you create
    # geolocation resource record sets that cover all seven continents, Amazon
    # Route 53 will receive some DNS queries from locations that it can't
    # identify. We recommend that you create a resource record set for which the
    # value of `CountryCode` is `*`, which handles both queries that come from
    # locations for which you haven't created geolocation resource record sets
    # and queries from IP addresses that aren't mapped to a location. If you
    # don't create a `*` resource record set, Amazon Route 53 returns a "no
    # answer" response for queries from those locations.

    # You can't create non-geolocation resource record sets that have the same
    # values for the `Name` and `Type` elements as geolocation resource record
    # sets.
    geo_location: "GeoLocation" = dataclasses.field(default_factory=dict, )

    # _Failover resource record sets only:_ To configure failover, you add the
    # `Failover` element to two resource record sets. For one resource record
    # set, you specify `PRIMARY` as the value for `Failover`; for the other
    # resource record set, you specify `SECONDARY`. In addition, you include the
    # `HealthCheckId` element and specify the health check that you want Amazon
    # Route 53 to perform for each resource record set.

    # Except where noted, the following failover behaviors assume that you have
    # included the `HealthCheckId` element in both resource record sets:

    #   * When the primary resource record set is healthy, Amazon Route 53 responds to DNS queries with the applicable value from the primary resource record set regardless of the health of the secondary resource record set.

    #   * When the primary resource record set is unhealthy and the secondary resource record set is healthy, Amazon Route 53 responds to DNS queries with the applicable value from the secondary resource record set.

    #   * When the secondary resource record set is unhealthy, Amazon Route 53 responds to DNS queries with the applicable value from the primary resource record set regardless of the health of the primary resource record set.

    #   * If you omit the `HealthCheckId` element for the secondary resource record set, and if the primary resource record set is unhealthy, Amazon Route 53 always responds to DNS queries with the applicable value from the secondary resource record set. This is true regardless of the health of the associated endpoint.

    # You can't create non-failover resource record sets that have the same
    # values for the `Name` and `Type` elements as failover resource record sets.

    # For failover alias resource record sets, you must also include the
    # `EvaluateTargetHealth` element and set the value to true.

    # For more information about configuring failover for Amazon Route 53, see
    # the following topics in the _Amazon Route 53 Developer Guide_ :

    #   * [Amazon Route 53 Health Checks and DNS Failover](http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html)

    #   * [Configuring Failover in a Private Hosted Zone](http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-private-hosted-zones.html)
    failover: "ResourceRecordSetFailover" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # _Multivalue answer resource record sets only_ : To route traffic
    # approximately randomly to multiple resources, such as web servers, create
    # one multivalue answer record for each resource and specify `true` for
    # `MultiValueAnswer`. Note the following:

    #   * If you associate a health check with a multivalue answer resource record set, Amazon Route 53 responds to DNS queries with the corresponding IP address only when the health check is healthy.

    #   * If you don't associate a health check with a multivalue answer record, Amazon Route 53 always considers the record to be healthy.

    #   * Amazon Route 53 responds to DNS queries with up to eight healthy records; if you have eight or fewer healthy records, Amazon Route 53 responds to all DNS queries with all the healthy records.

    #   * If you have more than eight healthy records, Amazon Route 53 responds to different DNS resolvers with different combinations of healthy records.

    #   * When all records are unhealthy, Amazon Route 53 responds to DNS queries with up to eight unhealthy records.

    #   * If a resource becomes unavailable after a resolver caches a response, client software typically tries another of the IP addresses in the response.

    # You can't create multivalue answer alias records.
    multi_value_answer: bool = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The resource record cache time to live (TTL), in seconds. Note the
    # following:

    #   * If you're creating or updating an alias resource record set, omit `TTL`. Amazon Route 53 uses the value of `TTL` for the alias target.

    #   * If you're associating this resource record set with a health check (if you're adding a `HealthCheckId` element), we recommend that you specify a `TTL` of 60 seconds or less so clients respond quickly to changes in health status.

    #   * All of the resource record sets in a group of weighted resource record sets must have the same value for `TTL`.

    #   * If a group of weighted resource record sets includes one or more weighted alias resource record sets for which the alias target is an ELB load balancer, we recommend that you specify a `TTL` of 60 seconds for all of the non-alias weighted resource record sets that have the same name and type. Values other than 60 seconds (the TTL for load balancers) will change the effect of the values that you specify for `Weight`.
    ttl: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Information about the resource records to act upon.

    # If you're creating an alias resource record set, omit `ResourceRecords`.
    resource_records: typing.List["ResourceRecord"] = dataclasses.field(
        default_factory=list,
    )

    # _Alias resource record sets only:_ Information about the CloudFront
    # distribution, AWS Elastic Beanstalk environment, ELB load balancer, Amazon
    # S3 bucket, or Amazon Route 53 resource record set to which you're
    # redirecting queries. The AWS Elastic Beanstalk environment must have a
    # regionalized subdomain.

    # If you're creating resource records sets for a private hosted zone, note
    # the following:

    #   * You can't create alias resource record sets for CloudFront distributions in a private hosted zone.

    #   * Creating geolocation alias resource record sets or latency alias resource record sets in a private hosted zone is unsupported.

    #   * For information about creating failover resource record sets in a private hosted zone, see [Configuring Failover in a Private Hosted Zone](http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-private-hosted-zones.html) in the _Amazon Route 53 Developer Guide_.
    alias_target: "AliasTarget" = dataclasses.field(default_factory=dict, )

    # If you want Amazon Route 53 to return this resource record set in response
    # to a DNS query only when a health check is passing, include the
    # `HealthCheckId` element and specify the ID of the applicable health check.

    # Amazon Route 53 determines whether a resource record set is healthy based
    # on one of the following:

    #   * By periodically sending a request to the endpoint that is specified in the health check

    #   * By aggregating the status of a specified group of health checks (calculated health checks)

    #   * By determining the current state of a CloudWatch alarm (CloudWatch metric health checks)

    # For more information, see [How Amazon Route 53 Determines Whether an
    # Endpoint Is
    # Healthy](http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-
    # failover-determining-health-of-endpoints.html).

    # The `HealthCheckId` element is only useful when Amazon Route 53 is choosing
    # between two or more resource record sets to respond to a DNS query, and you
    # want Amazon Route 53 to base the choice in part on the status of a health
    # check. Configuring health checks only makes sense in the following
    # configurations:

    #   * You're checking the health of the resource record sets in a group of weighted, latency, geolocation, or failover resource record sets, and you specify health check IDs for all of the resource record sets. If the health check for one resource record set specifies an endpoint that is not healthy, Amazon Route 53 stops responding to queries using the value for that resource record set.

    #   * You set `EvaluateTargetHealth` to true for the resource record sets in a group of alias, weighted alias, latency alias, geolocation alias, or failover alias resource record sets, and you specify health check IDs for all of the resource record sets that are referenced by the alias resource record sets.

    # Amazon Route 53 doesn't check the health of the endpoint specified in the
    # resource record set, for example, the endpoint specified by the IP address
    # in the `Value` element. When you add a `HealthCheckId` element to a
    # resource record set, Amazon Route 53 checks the health of the endpoint that
    # you specified in the health check.

    # For geolocation resource record sets, if an endpoint is unhealthy, Amazon
    # Route 53 looks for a resource record set for the larger, associated
    # geographic region. For example, suppose you have resource record sets for a
    # state in the United States, for the United States, for North America, and
    # for all locations. If the endpoint for the state resource record set is
    # unhealthy, Amazon Route 53 checks the resource record sets for the United
    # States, for North America, and for all locations (a resource record set for
    # which the value of `CountryCode` is `*`), in that order, until it finds a
    # resource record set for which the endpoint is healthy.

    # If your health checks specify the endpoint only by domain name, we
    # recommend that you create a separate health check for each endpoint. For
    # example, create a health check for each `HTTP` server that is serving
    # content for `www.example.com`. For the value of `FullyQualifiedDomainName`,
    # specify the domain name of the server (such as `us-
    # east-2-www.example.com`), not the name of the resource record sets
    # (example.com).

    # n this configuration, if you create a health check for which the value of
    # `FullyQualifiedDomainName` matches the name of the resource record sets and
    # then associate the health check with those resource record sets, health
    # check results will be unpredictable.

    # For more information, see the following topics in the _Amazon Route 53
    # Developer Guide_ :

    #   * [Amazon Route 53 Health Checks and DNS Failover](http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html)

    #   * [Configuring Failover in a Private Hosted Zone](http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-private-hosted-zones.html)
    health_check_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # When you create a traffic policy instance, Amazon Route 53 automatically
    # creates a resource record set. `TrafficPolicyInstanceId` is the ID of the
    # traffic policy instance that Amazon Route 53 created this resource record
    # set for.

    # To delete the resource record set that is associated with a traffic policy
    # instance, use `DeleteTrafficPolicyInstance`. Amazon Route 53 will delete
    # the resource record set automatically. If you delete the resource record
    # set by using `ChangeResourceRecordSets`, Amazon Route 53 doesn't
    # automatically delete the traffic policy instance, and you'll continue to be
    # charged for it even though it's no longer in use.
    traffic_policy_instance_id: str = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


class ResourceRecordSetFailover(Enum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"


class ResourceRecordSetRegion(Enum):
    us_east_1 = "us-east-1"
    us_east_2 = "us-east-2"
    us_west_1 = "us-west-1"
    us_west_2 = "us-west-2"
    ca_central_1 = "ca-central-1"
    eu_west_1 = "eu-west-1"
    eu_west_2 = "eu-west-2"
    eu_west_3 = "eu-west-3"
    eu_central_1 = "eu-central-1"
    ap_southeast_1 = "ap-southeast-1"
    ap_southeast_2 = "ap-southeast-2"
    ap_northeast_1 = "ap-northeast-1"
    ap_northeast_2 = "ap-northeast-2"
    ap_northeast_3 = "ap-northeast-3"
    sa_east_1 = "sa-east-1"
    cn_north_1 = "cn-north-1"
    cn_northwest_1 = "cn-northwest-1"
    ap_south_1 = "ap-south-1"


@dataclasses.dataclass
class ResourceTagSet(ShapeBase):
    """
    A complex type containing a resource and its associated tags.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "resource_type",
                "ResourceType",
                TypeInfo(TagResourceType),
            ),
            (
                "resource_id",
                "ResourceId",
                TypeInfo(str),
            ),
            (
                "tags",
                "Tags",
                TypeInfo(typing.List[Tag]),
            ),
        ]

    # The type of the resource.

    #   * The resource type for health checks is `healthcheck`.

    #   * The resource type for hosted zones is `hostedzone`.
    resource_type: "TagResourceType" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The ID for the specified resource.
    resource_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The tags associated with the specified resource.
    tags: typing.List["Tag"] = dataclasses.field(default_factory=list, )


@dataclasses.dataclass
class ReusableDelegationSetLimit(ShapeBase):
    """
    A complex type that contains the type of limit that you specified in the request
    and the current value for that limit.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "type",
                "Type",
                TypeInfo(ReusableDelegationSetLimitType),
            ),
            (
                "value",
                "Value",
                TypeInfo(int),
            ),
        ]

    # The limit that you requested: `MAX_ZONES_BY_REUSABLE_DELEGATION_SET`, the
    # maximum number of hosted zones that you can associate with the specified
    # reusable delegation set.
    type: "ReusableDelegationSetLimitType" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The current value for the `MAX_ZONES_BY_REUSABLE_DELEGATION_SET` limit.
    value: int = dataclasses.field(default=ShapeBase.NOT_SET, )


class ReusableDelegationSetLimitType(Enum):
    MAX_ZONES_BY_REUSABLE_DELEGATION_SET = "MAX_ZONES_BY_REUSABLE_DELEGATION_SET"


class Statistic(Enum):
    Average = "Average"
    Sum = "Sum"
    SampleCount = "SampleCount"
    Maximum = "Maximum"
    Minimum = "Minimum"


@dataclasses.dataclass
class StatusReport(ShapeBase):
    """
    A complex type that contains the status that one Amazon Route 53 health checker
    reports and the time of the health check.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "status",
                "Status",
                TypeInfo(str),
            ),
            (
                "checked_time",
                "CheckedTime",
                TypeInfo(datetime.datetime),
            ),
        ]

    # A description of the status of the health check endpoint as reported by one
    # of the Amazon Route 53 health checkers.
    status: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The date and time that the health checker performed the health check in
    # [ISO 8601 format](https://en.wikipedia.org/wiki/ISO_8601) and Coordinated
    # Universal Time (UTC). For example, the value `2017-03-27T17:48:16.751Z`
    # represents March 27, 2017 at 17:48:16.751 UTC.
    checked_time: datetime.datetime = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


@dataclasses.dataclass
class Tag(ShapeBase):
    """
    A complex type that contains information about a tag that you want to add or
    edit for the specified health check or hosted zone.
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

    # The value of `Key` depends on the operation that you want to perform:

    #   * **Add a tag to a health check or hosted zone** : `Key` is the name that you want to give the new tag.

    #   * **Edit a tag** : `Key` is the name of the tag that you want to change the `Value` for.

    #   * **Delete a key** : `Key` is the name of the tag you want to remove.

    #   * **Give a name to a health check** : Edit the default `Name` tag. In the Amazon Route 53 console, the list of your health checks includes a **Name** column that lets you see the name that you've given to each health check.
    key: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The value of `Value` depends on the operation that you want to perform:

    #   * **Add a tag to a health check or hosted zone** : `Value` is the value that you want to give the new tag.

    #   * **Edit a tag** : `Value` is the new value that you want to assign the tag.
    value: str = dataclasses.field(default=ShapeBase.NOT_SET, )


class TagResourceType(Enum):
    healthcheck = "healthcheck"
    hostedzone = "hostedzone"


@dataclasses.dataclass
class TestDNSAnswerRequest(ShapeBase):
    """
    Gets the value that Amazon Route 53 returns in response to a DNS request for a
    specified record name and type. You can optionally specify the IP address of a
    DNS resolver, an EDNS0 client subnet IP address, and a subnet mask.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "hosted_zone_id",
                "HostedZoneId",
                TypeInfo(str),
            ),
            (
                "record_name",
                "RecordName",
                TypeInfo(str),
            ),
            (
                "record_type",
                "RecordType",
                TypeInfo(RRType),
            ),
            (
                "resolver_ip",
                "ResolverIP",
                TypeInfo(str),
            ),
            (
                "edns0_client_subnet_ip",
                "EDNS0ClientSubnetIP",
                TypeInfo(str),
            ),
            (
                "edns0_client_subnet_mask",
                "EDNS0ClientSubnetMask",
                TypeInfo(str),
            ),
        ]

    # The ID of the hosted zone that you want Amazon Route 53 to simulate a query
    # for.
    hosted_zone_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the resource record set that you want Amazon Route 53 to
    # simulate a query for.
    record_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The type of the resource record set.
    record_type: "RRType" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If you want to simulate a request from a specific DNS resolver, specify the
    # IP address for that resolver. If you omit this value, `TestDnsAnswer` uses
    # the IP address of a DNS resolver in the AWS US East (N. Virginia) Region
    # (`us-east-1`).
    resolver_ip: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If the resolver that you specified for resolverip supports EDNS0, specify
    # the IPv4 or IPv6 address of a client in the applicable location, for
    # example, `192.0.2.44` or `2001:db8:85a3::8a2e:370:7334`.
    edns0_client_subnet_ip: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If you specify an IP address for `edns0clientsubnetip`, you can optionally
    # specify the number of bits of the IP address that you want the checking
    # tool to include in the DNS query. For example, if you specify `192.0.2.44`
    # for `edns0clientsubnetip` and `24` for `edns0clientsubnetmask`, the
    # checking tool will simulate a request from 192.0.2.0/24. The default value
    # is 24 bits for IPv4 addresses and 64 bits for IPv6 addresses.
    edns0_client_subnet_mask: str = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


@dataclasses.dataclass
class TestDNSAnswerResponse(OutputShapeBase):
    """
    A complex type that contains the response to a `TestDNSAnswer` request.
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
                "nameserver",
                "Nameserver",
                TypeInfo(str),
            ),
            (
                "record_name",
                "RecordName",
                TypeInfo(str),
            ),
            (
                "record_type",
                "RecordType",
                TypeInfo(RRType),
            ),
            (
                "record_data",
                "RecordData",
                TypeInfo(typing.List[str]),
            ),
            (
                "response_code",
                "ResponseCode",
                TypeInfo(str),
            ),
            (
                "protocol",
                "Protocol",
                TypeInfo(str),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # The Amazon Route 53 name server used to respond to the request.
    nameserver: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name of the resource record set that you submitted a request for.
    record_name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The type of the resource record set that you submitted a request for.
    record_type: "RRType" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A list that contains values that Amazon Route 53 returned for this resource
    # record set.
    record_data: typing.List[str] = dataclasses.field(default_factory=list, )

    # A code that indicates whether the request is valid or not. The most common
    # response code is `NOERROR`, meaning that the request is valid. If the
    # response is not valid, Amazon Route 53 returns a response code that
    # describes the error. For a list of possible response codes, see [DNS
    # RCODES](http://www.iana.org/assignments/dns-parameters/dns-
    # parameters.xhtml#dns-parameters-6) on the IANA website.
    response_code: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The protocol that Amazon Route 53 used to respond to the request, either
    # `UDP` or `TCP`.
    protocol: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class ThrottlingException(ShapeBase):
    """
    The limit on the number of requests per second was exceeded.
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

    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class TooManyHealthChecks(ShapeBase):
    """
    This health check can't be created because the current account has reached the
    limit on the number of active health checks.

    For information about default limits, see
    [Limits](http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/DNSLimitations.html)
    in the _Amazon Route 53 Developer Guide_.

    For information about how to get the current limit for an account, see
    GetAccountLimit. To request a higher limit, [create a
    case](http://aws.amazon.com/route53-request) with the AWS Support Center.

    You have reached the maximum number of active health checks for an AWS account.
    To request a higher limit, [create a
    case](http://aws.amazon.com/route53-request) with the AWS Support Center.
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

    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class TooManyHostedZones(ShapeBase):
    """
    This operation can't be completed either because the current account has reached
    the limit on the number of hosted zones or because you've reached the limit on
    the number of hosted zones that can be associated with a reusable delegation
    set.

    For information about default limits, see
    [Limits](http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/DNSLimitations.html)
    in the _Amazon Route 53 Developer Guide_.

    To get the current limit on hosted zones that can be created by an account, see
    GetAccountLimit.

    To get the current limit on hosted zones that can be associated with a reusable
    delegation set, see GetReusableDelegationSetLimit.

    To request a higher limit, [create a
    case](http://aws.amazon.com/route53-request) with the AWS Support Center.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class TooManyTrafficPolicies(ShapeBase):
    """
    This traffic policy can't be created because the current account has reached the
    limit on the number of traffic policies.

    For information about default limits, see
    [Limits](http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/DNSLimitations.html)
    in the _Amazon Route 53 Developer Guide_.

    To get the current limit for an account, see GetAccountLimit.

    To request a higher limit, [create a
    case](http://aws.amazon.com/route53-request) with the AWS Support Center.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class TooManyTrafficPolicyInstances(ShapeBase):
    """
    This traffic policy instance can't be created because the current account has
    reached the limit on the number of traffic policy instances.

    For information about default limits, see
    [Limits](http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/DNSLimitations.html)
    in the _Amazon Route 53 Developer Guide_.

    For information about how to get the current limit for an account, see
    GetAccountLimit.

    To request a higher limit, [create a
    case](http://aws.amazon.com/route53-request) with the AWS Support Center.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class TooManyTrafficPolicyVersionsForCurrentPolicy(ShapeBase):
    """
    This traffic policy version can't be created because you've reached the limit of
    1000 on the number of versions that you can create for the current traffic
    policy.

    To create more traffic policy versions, you can use GetTrafficPolicy to get the
    traffic policy document for a specified traffic policy version, and then use
    CreateTrafficPolicy to create a new traffic policy using the traffic policy
    document.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class TooManyVPCAssociationAuthorizations(ShapeBase):
    """
    You've created the maximum number of authorizations that can be created for the
    specified hosted zone. To authorize another VPC to be associated with the hosted
    zone, submit a `DeleteVPCAssociationAuthorization` request to remove an existing
    authorization. To get a list of existing authorizations, submit a
    `ListVPCAssociationAuthorizations` request.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class TrafficPolicy(ShapeBase):
    """
    A complex type that contains settings for a traffic policy.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "id",
                "Id",
                TypeInfo(str),
            ),
            (
                "version",
                "Version",
                TypeInfo(int),
            ),
            (
                "name",
                "Name",
                TypeInfo(str),
            ),
            (
                "type",
                "Type",
                TypeInfo(RRType),
            ),
            (
                "document",
                "Document",
                TypeInfo(str),
            ),
            (
                "comment",
                "Comment",
                TypeInfo(str),
            ),
        ]

    # The ID that Amazon Route 53 assigned to a traffic policy when you created
    # it.
    id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The version number that Amazon Route 53 assigns to a traffic policy. For a
    # new traffic policy, the value of `Version` is always 1.
    version: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name that you specified when you created the traffic policy.
    name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The DNS type of the resource record sets that Amazon Route 53 creates when
    # you use a traffic policy to create a traffic policy instance.
    type: "RRType" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The definition of a traffic policy in JSON format. You specify the JSON
    # document to use for a new traffic policy in the `CreateTrafficPolicy`
    # request. For more information about the JSON format, see [Traffic Policy
    # Document
    # Format](http://docs.aws.amazon.com/Route53/latest/APIReference/api-
    # policies-traffic-policy-document-format.html).
    document: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The comment that you specify in the `CreateTrafficPolicy` request, if any.
    comment: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class TrafficPolicyAlreadyExists(ShapeBase):
    """
    A traffic policy that has the same value for `Name` already exists.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class TrafficPolicyInUse(ShapeBase):
    """
    One or more traffic policy instances were created by using the specified traffic
    policy.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class TrafficPolicyInstance(ShapeBase):
    """
    A complex type that contains settings for the new traffic policy instance.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "id",
                "Id",
                TypeInfo(str),
            ),
            (
                "hosted_zone_id",
                "HostedZoneId",
                TypeInfo(str),
            ),
            (
                "name",
                "Name",
                TypeInfo(str),
            ),
            (
                "ttl",
                "TTL",
                TypeInfo(int),
            ),
            (
                "state",
                "State",
                TypeInfo(str),
            ),
            (
                "message",
                "Message",
                TypeInfo(str),
            ),
            (
                "traffic_policy_id",
                "TrafficPolicyId",
                TypeInfo(str),
            ),
            (
                "traffic_policy_version",
                "TrafficPolicyVersion",
                TypeInfo(int),
            ),
            (
                "traffic_policy_type",
                "TrafficPolicyType",
                TypeInfo(RRType),
            ),
        ]

    # The ID that Amazon Route 53 assigned to the new traffic policy instance.
    id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The ID of the hosted zone that Amazon Route 53 created resource record sets
    # in.
    hosted_zone_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The DNS name, such as www.example.com, for which Amazon Route 53 responds
    # to queries by using the resource record sets that are associated with this
    # traffic policy instance.
    name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The TTL that Amazon Route 53 assigned to all of the resource record sets
    # that it created in the specified hosted zone.
    ttl: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The value of `State` is one of the following values:

    # Applied

    # Amazon Route 53 has finished creating resource record sets, and changes
    # have propagated to all Amazon Route 53 edge locations.

    # Creating

    # Amazon Route 53 is creating the resource record sets. Use
    # `GetTrafficPolicyInstance` to confirm that the
    # `CreateTrafficPolicyInstance` request completed successfully.

    # Failed

    # Amazon Route 53 wasn't able to create or update the resource record sets.
    # When the value of `State` is `Failed`, see `Message` for an explanation of
    # what caused the request to fail.
    state: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # If `State` is `Failed`, an explanation of the reason for the failure. If
    # `State` is another value, `Message` is empty.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The ID of the traffic policy that Amazon Route 53 used to create resource
    # record sets in the specified hosted zone.
    traffic_policy_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The version of the traffic policy that Amazon Route 53 used to create
    # resource record sets in the specified hosted zone.
    traffic_policy_version: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The DNS type that Amazon Route 53 assigned to all of the resource record
    # sets that it created for this traffic policy instance.
    traffic_policy_type: "RRType" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )


@dataclasses.dataclass
class TrafficPolicyInstanceAlreadyExists(ShapeBase):
    """
    There is already a traffic policy instance with the specified ID.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class TrafficPolicySummary(ShapeBase):
    """
    A complex type that contains information about the latest version of one traffic
    policy that is associated with the current AWS account.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "id",
                "Id",
                TypeInfo(str),
            ),
            (
                "name",
                "Name",
                TypeInfo(str),
            ),
            (
                "type",
                "Type",
                TypeInfo(RRType),
            ),
            (
                "latest_version",
                "LatestVersion",
                TypeInfo(int),
            ),
            (
                "traffic_policy_count",
                "TrafficPolicyCount",
                TypeInfo(int),
            ),
        ]

    # The ID that Amazon Route 53 assigned to the traffic policy when you created
    # it.
    id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The name that you specified for the traffic policy when you created it.
    name: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The DNS type of the resource record sets that Amazon Route 53 creates when
    # you use a traffic policy to create a traffic policy instance.
    type: "RRType" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The version number of the latest version of the traffic policy.
    latest_version: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The number of traffic policies that are associated with the current AWS
    # account.
    traffic_policy_count: int = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class UpdateHealthCheckRequest(ShapeBase):
    """
    A complex type that contains information about a request to update a health
    check.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "health_check_id",
                "HealthCheckId",
                TypeInfo(str),
            ),
            (
                "health_check_version",
                "HealthCheckVersion",
                TypeInfo(int),
            ),
            (
                "ip_address",
                "IPAddress",
                TypeInfo(str),
            ),
            (
                "port",
                "Port",
                TypeInfo(int),
            ),
            (
                "resource_path",
                "ResourcePath",
                TypeInfo(str),
            ),
            (
                "fully_qualified_domain_name",
                "FullyQualifiedDomainName",
                TypeInfo(str),
            ),
            (
                "search_string",
                "SearchString",
                TypeInfo(str),
            ),
            (
                "failure_threshold",
                "FailureThreshold",
                TypeInfo(int),
            ),
            (
                "inverted",
                "Inverted",
                TypeInfo(bool),
            ),
            (
                "health_threshold",
                "HealthThreshold",
                TypeInfo(int),
            ),
            (
                "child_health_checks",
                "ChildHealthChecks",
                TypeInfo(typing.List[str]),
            ),
            (
                "enable_sni",
                "EnableSNI",
                TypeInfo(bool),
            ),
            (
                "regions",
                "Regions",
                TypeInfo(typing.List[HealthCheckRegion]),
            ),
            (
                "alarm_identifier",
                "AlarmIdentifier",
                TypeInfo(AlarmIdentifier),
            ),
            (
                "insufficient_data_health_status",
                "InsufficientDataHealthStatus",
                TypeInfo(InsufficientDataHealthStatus),
            ),
            (
                "reset_elements",
                "ResetElements",
                TypeInfo(typing.List[ResettableElementName]),
            ),
        ]

    # The ID for the health check for which you want detailed information. When
    # you created the health check, `CreateHealthCheck` returned the ID in the
    # response, in the `HealthCheckId` element.
    health_check_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A sequential counter that Amazon Route 53 sets to `1` when you create a
    # health check and increments by 1 each time you update settings for the
    # health check.

    # We recommend that you use `GetHealthCheck` or `ListHealthChecks` to get the
    # current value of `HealthCheckVersion` for the health check that you want to
    # update, and that you include that value in your `UpdateHealthCheck`
    # request. This prevents Amazon Route 53 from overwriting an intervening
    # update:

    #   * If the value in the `UpdateHealthCheck` request matches the value of `HealthCheckVersion` in the health check, Amazon Route 53 updates the health check with the new settings.

    #   * If the value of `HealthCheckVersion` in the health check is greater, the health check was changed after you got the version number. Amazon Route 53 does not update the health check, and it returns a `HealthCheckVersionMismatch` error.
    health_check_version: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The IPv4 or IPv6 IP address for the endpoint that you want Amazon Route 53
    # to perform health checks on. If you don't specify a value for `IPAddress`,
    # Amazon Route 53 sends a DNS request to resolve the domain name that you
    # specify in `FullyQualifiedDomainName` at the interval that you specify in
    # `RequestInterval`. Using an IP address that is returned by DNS, Amazon
    # Route 53 then checks the health of the endpoint.

    # Use one of the following formats for the value of `IPAddress`:

    #   * **IPv4 address** : four values between 0 and 255, separated by periods (.), for example, `192.0.2.44`.

    #   * **IPv6 address** : eight groups of four hexadecimal values, separated by colons (:), for example, `2001:0db8:85a3:0000:0000:abcd:0001:2345`. You can also shorten IPv6 addresses as described in RFC 5952, for example, `2001:db8:85a3::abcd:1:2345`.

    # If the endpoint is an EC2 instance, we recommend that you create an Elastic
    # IP address, associate it with your EC2 instance, and specify the Elastic IP
    # address for `IPAddress`. This ensures that the IP address of your instance
    # never changes. For more information, see the applicable documentation:

    #   * Linux: [Elastic IP Addresses (EIP)](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html) in the _Amazon EC2 User Guide for Linux Instances_

    #   * Windows: [Elastic IP Addresses (EIP)](http://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/elastic-ip-addresses-eip.html) in the _Amazon EC2 User Guide for Windows Instances_

    # If a health check already has a value for `IPAddress`, you can change the
    # value. However, you can't update an existing health check to add or remove
    # the value of `IPAddress`.

    # For more information, see
    # UpdateHealthCheckRequest$FullyQualifiedDomainName.

    # Constraints: Amazon Route 53 can't check the health of endpoints for which
    # the IP address is in local, private, non-routable, or multicast ranges. For
    # more information about IP addresses for which you can't create health
    # checks, see the following documents:

    #   * [RFC 5735, Special Use IPv4 Addresses](https://tools.ietf.org/html/rfc5735)

    #   * [RFC 6598, IANA-Reserved IPv4 Prefix for Shared Address Space](https://tools.ietf.org/html/rfc6598)

    #   * [RFC 5156, Special-Use IPv6 Addresses](https://tools.ietf.org/html/rfc5156)
    ip_address: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The port on the endpoint on which you want Amazon Route 53 to perform
    # health checks.
    port: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The path that you want Amazon Route 53 to request when performing health
    # checks. The path can be any value for which your endpoint will return an
    # HTTP status code of 2xx or 3xx when the endpoint is healthy, for example
    # the file /docs/route53-health-check.html.

    # Specify this value only if you want to change it.
    resource_path: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Amazon Route 53 behavior depends on whether you specify a value for
    # `IPAddress`.

    # If a health check already has a value for `IPAddress`, you can change the
    # value. However, you can't update an existing health check to add or remove
    # the value of `IPAddress`.

    # **If you specify a value for** `IPAddress`:

    # Amazon Route 53 sends health check requests to the specified IPv4 or IPv6
    # address and passes the value of `FullyQualifiedDomainName` in the `Host`
    # header for all health checks except TCP health checks. This is typically
    # the fully qualified DNS name of the endpoint on which you want Amazon Route
    # 53 to perform health checks.

    # When Amazon Route 53 checks the health of an endpoint, here is how it
    # constructs the `Host` header:

    #   * If you specify a value of `80` for `Port` and `HTTP` or `HTTP_STR_MATCH` for `Type`, Amazon Route 53 passes the value of `FullyQualifiedDomainName` to the endpoint in the `Host` header.

    #   * If you specify a value of `443` for `Port` and `HTTPS` or `HTTPS_STR_MATCH` for `Type`, Amazon Route 53 passes the value of `FullyQualifiedDomainName` to the endpoint in the `Host` header.

    #   * If you specify another value for `Port` and any value except `TCP` for `Type`, Amazon Route 53 passes _`FullyQualifiedDomainName`:`Port` _ to the endpoint in the `Host` header.

    # If you don't specify a value for `FullyQualifiedDomainName`, Amazon Route
    # 53 substitutes the value of `IPAddress` in the `Host` header in each of the
    # above cases.

    # **If you don't specify a value for** `IPAddress`:

    # If you don't specify a value for `IPAddress`, Amazon Route 53 sends a DNS
    # request to the domain that you specify in `FullyQualifiedDomainName` at the
    # interval you specify in `RequestInterval`. Using an IPv4 address that is
    # returned by DNS, Amazon Route 53 then checks the health of the endpoint.

    # If you don't specify a value for `IPAddress`, Amazon Route 53 uses only
    # IPv4 to send health checks to the endpoint. If there's no resource record
    # set with a type of A for the name that you specify for
    # `FullyQualifiedDomainName`, the health check fails with a "DNS resolution
    # failed" error.

    # If you want to check the health of weighted, latency, or failover resource
    # record sets and you choose to specify the endpoint only by
    # `FullyQualifiedDomainName`, we recommend that you create a separate health
    # check for each endpoint. For example, create a health check for each HTTP
    # server that is serving content for www.example.com. For the value of
    # `FullyQualifiedDomainName`, specify the domain name of the server (such as
    # `us-east-2-www.example.com`), not the name of the resource record sets
    # (www.example.com).

    # In this configuration, if the value of `FullyQualifiedDomainName` matches
    # the name of the resource record sets and you then associate the health
    # check with those resource record sets, health check results will be
    # unpredictable.

    # In addition, if the value of `Type` is `HTTP`, `HTTPS`, `HTTP_STR_MATCH`,
    # or `HTTPS_STR_MATCH`, Amazon Route 53 passes the value of
    # `FullyQualifiedDomainName` in the `Host` header, as it does when you
    # specify a value for `IPAddress`. If the value of `Type` is `TCP`, Amazon
    # Route 53 doesn't pass a `Host` header.
    fully_qualified_domain_name: str = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # If the value of `Type` is `HTTP_STR_MATCH` or `HTTP_STR_MATCH`, the string
    # that you want Amazon Route 53 to search for in the response body from the
    # specified resource. If the string appears in the response body, Amazon
    # Route 53 considers the resource healthy. (You can't change the value of
    # `Type` when you update a health check.)
    search_string: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The number of consecutive health checks that an endpoint must pass or fail
    # for Amazon Route 53 to change the current status of the endpoint from
    # unhealthy to healthy or vice versa. For more information, see [How Amazon
    # Route 53 Determines Whether an Endpoint Is
    # Healthy](http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-
    # failover-determining-health-of-endpoints.html) in the _Amazon Route 53
    # Developer Guide_.

    # If you don't specify a value for `FailureThreshold`, the default value is
    # three health checks.
    failure_threshold: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # Specify whether you want Amazon Route 53 to invert the status of a health
    # check, for example, to consider a health check unhealthy when it otherwise
    # would be considered healthy.
    inverted: bool = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The number of child health checks that are associated with a `CALCULATED`
    # health that Amazon Route 53 must consider healthy for the `CALCULATED`
    # health check to be considered healthy. To specify the child health checks
    # that you want to associate with a `CALCULATED` health check, use the
    # `ChildHealthChecks` and `ChildHealthCheck` elements.

    # Note the following:

    #   * If you specify a number greater than the number of child health checks, Amazon Route 53 always considers this health check to be unhealthy.

    #   * If you specify `0`, Amazon Route 53 always considers this health check to be healthy.
    health_threshold: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A complex type that contains one `ChildHealthCheck` element for each health
    # check that you want to associate with a `CALCULATED` health check.
    child_health_checks: typing.List[str] = dataclasses.field(
        default_factory=list,
    )

    # Specify whether you want Amazon Route 53 to send the value of
    # `FullyQualifiedDomainName` to the endpoint in the `client_hello` message
    # during `TLS` negotiation. This allows the endpoint to respond to `HTTPS`
    # health check requests with the applicable SSL/TLS certificate.

    # Some endpoints require that HTTPS requests include the host name in the
    # `client_hello` message. If you don't enable SNI, the status of the health
    # check will be SSL alert `handshake_failure`. A health check can also have
    # that status for other reasons. If SNI is enabled and you're still getting
    # the error, check the SSL/TLS configuration on your endpoint and confirm
    # that your certificate is valid.

    # The SSL/TLS certificate on your endpoint includes a domain name in the
    # `Common Name` field and possibly several more in the `Subject Alternative
    # Names` field. One of the domain names in the certificate should match the
    # value that you specify for `FullyQualifiedDomainName`. If the endpoint
    # responds to the `client_hello` message with a certificate that does not
    # include the domain name that you specified in `FullyQualifiedDomainName`, a
    # health checker will retry the handshake. In the second attempt, the health
    # checker will omit `FullyQualifiedDomainName` from the `client_hello`
    # message.
    enable_sni: bool = dataclasses.field(default=ShapeBase.NOT_SET, )

    # A complex type that contains one `Region` element for each region that you
    # want Amazon Route 53 health checkers to check the specified endpoint from.
    regions: typing.List["HealthCheckRegion"] = dataclasses.field(
        default_factory=list,
    )

    # A complex type that identifies the CloudWatch alarm that you want Amazon
    # Route 53 health checkers to use to determine whether this health check is
    # healthy.
    alarm_identifier: "AlarmIdentifier" = dataclasses.field(
        default_factory=dict,
    )

    # When CloudWatch has insufficient data about the metric to determine the
    # alarm state, the status that you want Amazon Route 53 to assign to the
    # health check:

    #   * `Healthy`: Amazon Route 53 considers the health check to be healthy.

    #   * `Unhealthy`: Amazon Route 53 considers the health check to be unhealthy.

    #   * `LastKnownStatus`: Amazon Route 53 uses the status of the health check from the last time CloudWatch had sufficient data to determine the alarm state. For new health checks that have no last known status, the default status for the health check is healthy.
    insufficient_data_health_status: "InsufficientDataHealthStatus" = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains one `ResettableElementName` element for each
    # element that you want to reset to the default value. Valid values for
    # `ResettableElementName` include the following:

    #   * `ChildHealthChecks`: Amazon Route 53 resets HealthCheckConfig$ChildHealthChecks to null.

    #   * `FullyQualifiedDomainName`: Amazon Route 53 resets HealthCheckConfig$FullyQualifiedDomainName to null.

    #   * `Regions`: Amazon Route 53 resets the HealthCheckConfig$Regions list to the default set of regions.

    #   * `ResourcePath`: Amazon Route 53 resets HealthCheckConfig$ResourcePath to null.
    reset_elements: typing.List["ResettableElementName"] = dataclasses.field(
        default_factory=list,
    )


@dataclasses.dataclass
class UpdateHealthCheckResponse(OutputShapeBase):
    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "response_metadata",
                "ResponseMetadata",
                TypeInfo(typing.Dict[str, str]),
            ),
            (
                "health_check",
                "HealthCheck",
                TypeInfo(HealthCheck),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains information about one health check that is
    # associated with the current AWS account.
    health_check: "HealthCheck" = dataclasses.field(default_factory=dict, )


@dataclasses.dataclass
class UpdateHostedZoneCommentRequest(ShapeBase):
    """
    A request to update the comment for a hosted zone.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "id",
                "Id",
                TypeInfo(str),
            ),
            (
                "comment",
                "Comment",
                TypeInfo(str),
            ),
        ]

    # The ID for the hosted zone that you want to update the comment for.
    id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The new comment for the hosted zone. If you don't specify a value for
    # `Comment`, Amazon Route 53 deletes the existing value of the `Comment`
    # element, if any.
    comment: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class UpdateHostedZoneCommentResponse(OutputShapeBase):
    """
    A complex type that contains the response to the `UpdateHostedZoneComment`
    request.
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
                "hosted_zone",
                "HostedZone",
                TypeInfo(HostedZone),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains general information about the hosted zone.
    hosted_zone: "HostedZone" = dataclasses.field(default_factory=dict, )


@dataclasses.dataclass
class UpdateTrafficPolicyCommentRequest(ShapeBase):
    """
    A complex type that contains information about the traffic policy that you want
    to update the comment for.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "id",
                "Id",
                TypeInfo(str),
            ),
            (
                "version",
                "Version",
                TypeInfo(int),
            ),
            (
                "comment",
                "Comment",
                TypeInfo(str),
            ),
        ]

    # The value of `Id` for the traffic policy that you want to update the
    # comment for.
    id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The value of `Version` for the traffic policy that you want to update the
    # comment for.
    version: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The new comment for the specified traffic policy and version.
    comment: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class UpdateTrafficPolicyCommentResponse(OutputShapeBase):
    """
    A complex type that contains the response information for the traffic policy.
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
                "traffic_policy",
                "TrafficPolicy",
                TypeInfo(TrafficPolicy),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains settings for the specified traffic policy.
    traffic_policy: "TrafficPolicy" = dataclasses.field(default_factory=dict, )


@dataclasses.dataclass
class UpdateTrafficPolicyInstanceRequest(ShapeBase):
    """
    A complex type that contains information about the resource record sets that you
    want to update based on a specified traffic policy instance.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "id",
                "Id",
                TypeInfo(str),
            ),
            (
                "ttl",
                "TTL",
                TypeInfo(int),
            ),
            (
                "traffic_policy_id",
                "TrafficPolicyId",
                TypeInfo(str),
            ),
            (
                "traffic_policy_version",
                "TrafficPolicyVersion",
                TypeInfo(int),
            ),
        ]

    # The ID of the traffic policy instance that you want to update.
    id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The TTL that you want Amazon Route 53 to assign to all of the updated
    # resource record sets.
    ttl: int = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The ID of the traffic policy that you want Amazon Route 53 to use to update
    # resource record sets for the specified traffic policy instance.
    traffic_policy_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )

    # The version of the traffic policy that you want Amazon Route 53 to use to
    # update resource record sets for the specified traffic policy instance.
    traffic_policy_version: int = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class UpdateTrafficPolicyInstanceResponse(OutputShapeBase):
    """
    A complex type that contains information about the resource record sets that
    Amazon Route 53 created based on a specified traffic policy.
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
                "traffic_policy_instance",
                "TrafficPolicyInstance",
                TypeInfo(TrafficPolicyInstance),
            ),
        ]

    response_metadata: typing.Dict[str, str] = dataclasses.field(
        default=ShapeBase.NOT_SET,
    )

    # A complex type that contains settings for the updated traffic policy
    # instance.
    traffic_policy_instance: "TrafficPolicyInstance" = dataclasses.field(
        default_factory=dict,
    )


@dataclasses.dataclass
class VPC(ShapeBase):
    """
    (Private hosted zones only) A complex type that contains information about an
    Amazon VPC.
    """

    @classmethod
    def _get_boto_mapping(cls):
        return [
            (
                "vpc_region",
                "VPCRegion",
                TypeInfo(VPCRegion),
            ),
            (
                "vpc_id",
                "VPCId",
                TypeInfo(str),
            ),
        ]

    # (Private hosted zones only) The region in which you created an Amazon VPC.
    vpc_region: "VPCRegion" = dataclasses.field(default=ShapeBase.NOT_SET, )

    # (Private hosted zones only) The ID of an Amazon VPC.
    vpc_id: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class VPCAssociationAuthorizationNotFound(ShapeBase):
    """
    The VPC that you specified is not authorized to be associated with the hosted
    zone.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


@dataclasses.dataclass
class VPCAssociationNotFound(ShapeBase):
    """
    The specified VPC and hosted zone are not currently associated.
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

    # Descriptive message for the error response.
    message: str = dataclasses.field(default=ShapeBase.NOT_SET, )


class VPCRegion(Enum):
    us_east_1 = "us-east-1"
    us_east_2 = "us-east-2"
    us_west_1 = "us-west-1"
    us_west_2 = "us-west-2"
    eu_west_1 = "eu-west-1"
    eu_west_2 = "eu-west-2"
    eu_west_3 = "eu-west-3"
    eu_central_1 = "eu-central-1"
    ap_southeast_1 = "ap-southeast-1"
    ap_southeast_2 = "ap-southeast-2"
    ap_south_1 = "ap-south-1"
    ap_northeast_1 = "ap-northeast-1"
    ap_northeast_2 = "ap-northeast-2"
    ap_northeast_3 = "ap-northeast-3"
    sa_east_1 = "sa-east-1"
    ca_central_1 = "ca-central-1"
    cn_north_1 = "cn-north-1"
