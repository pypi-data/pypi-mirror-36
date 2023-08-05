import datetime
import typing
import boto3
from autoboto import ShapeBase, OutputShapeBase
from . import shapes


class Client:
    def __init__(self, *args, **kwargs):
        self._boto_client = boto3.client("efs", *args, **kwargs)

    def create_file_system(
        self,
        _request: shapes.CreateFileSystemRequest = None,
        *,
        creation_token: str,
        performance_mode: shapes.PerformanceMode = ShapeBase.NOT_SET,
        encrypted: bool = ShapeBase.NOT_SET,
        kms_key_id: str = ShapeBase.NOT_SET,
        throughput_mode: shapes.ThroughputMode = ShapeBase.NOT_SET,
        provisioned_throughput_in_mibps: float = ShapeBase.NOT_SET,
    ) -> shapes.FileSystemDescription:
        """
        Creates a new, empty file system. The operation requires a creation token in the
        request that Amazon EFS uses to ensure idempotent creation (calling the
        operation with same creation token has no effect). If a file system does not
        currently exist that is owned by the caller's AWS account with the specified
        creation token, this operation does the following:

          * Creates a new, empty file system. The file system will have an Amazon EFS assigned ID, and an initial lifecycle state `creating`.

          * Returns with the description of the created file system.

        Otherwise, this operation returns a `FileSystemAlreadyExists` error with the ID
        of the existing file system.

        For basic use cases, you can use a randomly generated UUID for the creation
        token.

        The idempotent operation allows you to retry a `CreateFileSystem` call without
        risk of creating an extra file system. This can happen when an initial call
        fails in a way that leaves it uncertain whether or not a file system was
        actually created. An example might be that a transport level timeout occurred or
        your connection was reset. As long as you use the same creation token, if the
        initial call had succeeded in creating a file system, the client can learn of
        its existence from the `FileSystemAlreadyExists` error.

        The `CreateFileSystem` call returns while the file system's lifecycle state is
        still `creating`. You can check the file system creation status by calling the
        DescribeFileSystems operation, which among other things returns the file system
        state.

        This operation also takes an optional `PerformanceMode` parameter that you
        choose for your file system. We recommend `generalPurpose` performance mode for
        most file systems. File systems using the `maxIO` performance mode can scale to
        higher levels of aggregate throughput and operations per second with a tradeoff
        of slightly higher latencies for most file operations. The performance mode
        can't be changed after the file system has been created. For more information,
        see [Amazon EFS: Performance
        Modes](http://docs.aws.amazon.com/efs/latest/ug/performance.html#performancemodes.html).

        After the file system is fully created, Amazon EFS sets its lifecycle state to
        `available`, at which point you can create one or more mount targets for the
        file system in your VPC. For more information, see CreateMountTarget. You mount
        your Amazon EFS file system on an EC2 instances in your VPC via the mount
        target. For more information, see [Amazon EFS: How it
        Works](http://docs.aws.amazon.com/efs/latest/ug/how-it-works.html).

        This operation requires permissions for the `elasticfilesystem:CreateFileSystem`
        action.
        """
        if _request is None:
            _params = {}
            if creation_token is not ShapeBase.NOT_SET:
                _params['creation_token'] = creation_token
            if performance_mode is not ShapeBase.NOT_SET:
                _params['performance_mode'] = performance_mode
            if encrypted is not ShapeBase.NOT_SET:
                _params['encrypted'] = encrypted
            if kms_key_id is not ShapeBase.NOT_SET:
                _params['kms_key_id'] = kms_key_id
            if throughput_mode is not ShapeBase.NOT_SET:
                _params['throughput_mode'] = throughput_mode
            if provisioned_throughput_in_mibps is not ShapeBase.NOT_SET:
                _params['provisioned_throughput_in_mibps'
                       ] = provisioned_throughput_in_mibps
            _request = shapes.CreateFileSystemRequest(**_params)
        response = self._boto_client.create_file_system(
            **_request.to_boto_dict()
        )

        return shapes.FileSystemDescription.from_boto_dict(response)

    def create_mount_target(
        self,
        _request: shapes.CreateMountTargetRequest = None,
        *,
        file_system_id: str,
        subnet_id: str,
        ip_address: str = ShapeBase.NOT_SET,
        security_groups: typing.List[str] = ShapeBase.NOT_SET,
    ) -> shapes.MountTargetDescription:
        """
        Creates a mount target for a file system. You can then mount the file system on
        EC2 instances via the mount target.

        You can create one mount target in each Availability Zone in your VPC. All EC2
        instances in a VPC within a given Availability Zone share a single mount target
        for a given file system. If you have multiple subnets in an Availability Zone,
        you create a mount target in one of the subnets. EC2 instances do not need to be
        in the same subnet as the mount target in order to access their file system. For
        more information, see [Amazon EFS: How it
        Works](http://docs.aws.amazon.com/efs/latest/ug/how-it-works.html).

        In the request, you also specify a file system ID for which you are creating the
        mount target and the file system's lifecycle state must be `available`. For more
        information, see DescribeFileSystems.

        In the request, you also provide a subnet ID, which determines the following:

          * VPC in which Amazon EFS creates the mount target

          * Availability Zone in which Amazon EFS creates the mount target

          * IP address range from which Amazon EFS selects the IP address of the mount target (if you don't specify an IP address in the request)

        After creating the mount target, Amazon EFS returns a response that includes, a
        `MountTargetId` and an `IpAddress`. You use this IP address when mounting the
        file system in an EC2 instance. You can also use the mount target's DNS name
        when mounting the file system. The EC2 instance on which you mount the file
        system via the mount target can resolve the mount target's DNS name to its IP
        address. For more information, see [How it Works: Implementation
        Overview](http://docs.aws.amazon.com/efs/latest/ug/how-it-works.html#how-it-
        works-implementation).

        Note that you can create mount targets for a file system in only one VPC, and
        there can be only one mount target per Availability Zone. That is, if the file
        system already has one or more mount targets created for it, the subnet
        specified in the request to add another mount target must meet the following
        requirements:

          * Must belong to the same VPC as the subnets of the existing mount targets

          * Must not be in the same Availability Zone as any of the subnets of the existing mount targets

        If the request satisfies the requirements, Amazon EFS does the following:

          * Creates a new mount target in the specified subnet.

          * Also creates a new network interface in the subnet as follows:

            * If the request provides an `IpAddress`, Amazon EFS assigns that IP address to the network interface. Otherwise, Amazon EFS assigns a free address in the subnet (in the same way that the Amazon EC2 `CreateNetworkInterface` call does when a request does not specify a primary private IP address).

            * If the request provides `SecurityGroups`, this network interface is associated with those security groups. Otherwise, it belongs to the default security group for the subnet's VPC.

            * Assigns the description `Mount target _fsmt-id_ for file system _fs-id_ ` where ` _fsmt-id_ ` is the mount target ID, and ` _fs-id_ ` is the `FileSystemId`.

            * Sets the `requesterManaged` property of the network interface to `true`, and the `requesterId` value to `EFS`.

        Each Amazon EFS mount target has one corresponding requester-managed EC2 network
        interface. After the network interface is created, Amazon EFS sets the
        `NetworkInterfaceId` field in the mount target's description to the network
        interface ID, and the `IpAddress` field to its address. If network interface
        creation fails, the entire `CreateMountTarget` operation fails.

        The `CreateMountTarget` call returns only after creating the network interface,
        but while the mount target state is still `creating`, you can check the mount
        target creation status by calling the DescribeMountTargets operation, which
        among other things returns the mount target state.

        We recommend you create a mount target in each of the Availability Zones. There
        are cost considerations for using a file system in an Availability Zone through
        a mount target created in another Availability Zone. For more information, see
        [Amazon EFS](http://aws.amazon.com/efs/). In addition, by always using a mount
        target local to the instance's Availability Zone, you eliminate a partial
        failure scenario. If the Availability Zone in which your mount target is created
        goes down, then you won't be able to access your file system through that mount
        target.

        This operation requires permissions for the following action on the file system:

          * `elasticfilesystem:CreateMountTarget`

        This operation also requires permissions for the following Amazon EC2 actions:

          * `ec2:DescribeSubnets`

          * `ec2:DescribeNetworkInterfaces`

          * `ec2:CreateNetworkInterface`
        """
        if _request is None:
            _params = {}
            if file_system_id is not ShapeBase.NOT_SET:
                _params['file_system_id'] = file_system_id
            if subnet_id is not ShapeBase.NOT_SET:
                _params['subnet_id'] = subnet_id
            if ip_address is not ShapeBase.NOT_SET:
                _params['ip_address'] = ip_address
            if security_groups is not ShapeBase.NOT_SET:
                _params['security_groups'] = security_groups
            _request = shapes.CreateMountTargetRequest(**_params)
        response = self._boto_client.create_mount_target(
            **_request.to_boto_dict()
        )

        return shapes.MountTargetDescription.from_boto_dict(response)

    def create_tags(
        self,
        _request: shapes.CreateTagsRequest = None,
        *,
        file_system_id: str,
        tags: typing.List[shapes.Tag],
    ) -> None:
        """
        Creates or overwrites tags associated with a file system. Each tag is a key-
        value pair. If a tag key specified in the request already exists on the file
        system, this operation overwrites its value with the value provided in the
        request. If you add the `Name` tag to your file system, Amazon EFS returns it in
        the response to the DescribeFileSystems operation.

        This operation requires permission for the `elasticfilesystem:CreateTags`
        action.
        """
        if _request is None:
            _params = {}
            if file_system_id is not ShapeBase.NOT_SET:
                _params['file_system_id'] = file_system_id
            if tags is not ShapeBase.NOT_SET:
                _params['tags'] = tags
            _request = shapes.CreateTagsRequest(**_params)
        response = self._boto_client.create_tags(**_request.to_boto_dict())

    def delete_file_system(
        self,
        _request: shapes.DeleteFileSystemRequest = None,
        *,
        file_system_id: str,
    ) -> None:
        """
        Deletes a file system, permanently severing access to its contents. Upon return,
        the file system no longer exists and you can't access any contents of the
        deleted file system.

        You can't delete a file system that is in use. That is, if the file system has
        any mount targets, you must first delete them. For more information, see
        DescribeMountTargets and DeleteMountTarget.

        The `DeleteFileSystem` call returns while the file system state is still
        `deleting`. You can check the file system deletion status by calling the
        DescribeFileSystems operation, which returns a list of file systems in your
        account. If you pass file system ID or creation token for the deleted file
        system, the DescribeFileSystems returns a `404 FileSystemNotFound` error.

        This operation requires permissions for the `elasticfilesystem:DeleteFileSystem`
        action.
        """
        if _request is None:
            _params = {}
            if file_system_id is not ShapeBase.NOT_SET:
                _params['file_system_id'] = file_system_id
            _request = shapes.DeleteFileSystemRequest(**_params)
        response = self._boto_client.delete_file_system(
            **_request.to_boto_dict()
        )

    def delete_mount_target(
        self,
        _request: shapes.DeleteMountTargetRequest = None,
        *,
        mount_target_id: str,
    ) -> None:
        """
        Deletes the specified mount target.

        This operation forcibly breaks any mounts of the file system via the mount
        target that is being deleted, which might disrupt instances or applications
        using those mounts. To avoid applications getting cut off abruptly, you might
        consider unmounting any mounts of the mount target, if feasible. The operation
        also deletes the associated network interface. Uncommitted writes may be lost,
        but breaking a mount target using this operation does not corrupt the file
        system itself. The file system you created remains. You can mount an EC2
        instance in your VPC via another mount target.

        This operation requires permissions for the following action on the file system:

          * `elasticfilesystem:DeleteMountTarget`

        The `DeleteMountTarget` call returns while the mount target state is still
        `deleting`. You can check the mount target deletion by calling the
        DescribeMountTargets operation, which returns a list of mount target
        descriptions for the given file system.

        The operation also requires permissions for the following Amazon EC2 action on
        the mount target's network interface:

          * `ec2:DeleteNetworkInterface`
        """
        if _request is None:
            _params = {}
            if mount_target_id is not ShapeBase.NOT_SET:
                _params['mount_target_id'] = mount_target_id
            _request = shapes.DeleteMountTargetRequest(**_params)
        response = self._boto_client.delete_mount_target(
            **_request.to_boto_dict()
        )

    def delete_tags(
        self,
        _request: shapes.DeleteTagsRequest = None,
        *,
        file_system_id: str,
        tag_keys: typing.List[str],
    ) -> None:
        """
        Deletes the specified tags from a file system. If the `DeleteTags` request
        includes a tag key that does not exist, Amazon EFS ignores it and doesn't cause
        an error. For more information about tags and related restrictions, see [Tag
        Restrictions](http://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-
        alloc-tags.html) in the _AWS Billing and Cost Management User Guide_.

        This operation requires permissions for the `elasticfilesystem:DeleteTags`
        action.
        """
        if _request is None:
            _params = {}
            if file_system_id is not ShapeBase.NOT_SET:
                _params['file_system_id'] = file_system_id
            if tag_keys is not ShapeBase.NOT_SET:
                _params['tag_keys'] = tag_keys
            _request = shapes.DeleteTagsRequest(**_params)
        response = self._boto_client.delete_tags(**_request.to_boto_dict())

    def describe_file_systems(
        self,
        _request: shapes.DescribeFileSystemsRequest = None,
        *,
        max_items: int = ShapeBase.NOT_SET,
        marker: str = ShapeBase.NOT_SET,
        creation_token: str = ShapeBase.NOT_SET,
        file_system_id: str = ShapeBase.NOT_SET,
    ) -> shapes.DescribeFileSystemsResponse:
        """
        Returns the description of a specific Amazon EFS file system if either the file
        system `CreationToken` or the `FileSystemId` is provided. Otherwise, it returns
        descriptions of all file systems owned by the caller's AWS account in the AWS
        Region of the endpoint that you're calling.

        When retrieving all file system descriptions, you can optionally specify the
        `MaxItems` parameter to limit the number of descriptions in a response. If more
        file system descriptions remain, Amazon EFS returns a `NextMarker`, an opaque
        token, in the response. In this case, you should send a subsequent request with
        the `Marker` request parameter set to the value of `NextMarker`.

        To retrieve a list of your file system descriptions, this operation is used in
        an iterative process, where `DescribeFileSystems` is called first without the
        `Marker` and then the operation continues to call it with the `Marker` parameter
        set to the value of the `NextMarker` from the previous response until the
        response has no `NextMarker`.

        The implementation may return fewer than `MaxItems` file system descriptions
        while still including a `NextMarker` value.

        The order of file systems returned in the response of one `DescribeFileSystems`
        call and the order of file systems returned across the responses of a multi-call
        iteration is unspecified.

        This operation requires permissions for the
        `elasticfilesystem:DescribeFileSystems` action.
        """
        if _request is None:
            _params = {}
            if max_items is not ShapeBase.NOT_SET:
                _params['max_items'] = max_items
            if marker is not ShapeBase.NOT_SET:
                _params['marker'] = marker
            if creation_token is not ShapeBase.NOT_SET:
                _params['creation_token'] = creation_token
            if file_system_id is not ShapeBase.NOT_SET:
                _params['file_system_id'] = file_system_id
            _request = shapes.DescribeFileSystemsRequest(**_params)
        response = self._boto_client.describe_file_systems(
            **_request.to_boto_dict()
        )

        return shapes.DescribeFileSystemsResponse.from_boto_dict(response)

    def describe_mount_target_security_groups(
        self,
        _request: shapes.DescribeMountTargetSecurityGroupsRequest = None,
        *,
        mount_target_id: str,
    ) -> shapes.DescribeMountTargetSecurityGroupsResponse:
        """
        Returns the security groups currently in effect for a mount target. This
        operation requires that the network interface of the mount target has been
        created and the lifecycle state of the mount target is not `deleted`.

        This operation requires permissions for the following actions:

          * `elasticfilesystem:DescribeMountTargetSecurityGroups` action on the mount target's file system. 

          * `ec2:DescribeNetworkInterfaceAttribute` action on the mount target's network interface.
        """
        if _request is None:
            _params = {}
            if mount_target_id is not ShapeBase.NOT_SET:
                _params['mount_target_id'] = mount_target_id
            _request = shapes.DescribeMountTargetSecurityGroupsRequest(
                **_params
            )
        response = self._boto_client.describe_mount_target_security_groups(
            **_request.to_boto_dict()
        )

        return shapes.DescribeMountTargetSecurityGroupsResponse.from_boto_dict(
            response
        )

    def describe_mount_targets(
        self,
        _request: shapes.DescribeMountTargetsRequest = None,
        *,
        max_items: int = ShapeBase.NOT_SET,
        marker: str = ShapeBase.NOT_SET,
        file_system_id: str = ShapeBase.NOT_SET,
        mount_target_id: str = ShapeBase.NOT_SET,
    ) -> shapes.DescribeMountTargetsResponse:
        """
        Returns the descriptions of all the current mount targets, or a specific mount
        target, for a file system. When requesting all of the current mount targets, the
        order of mount targets returned in the response is unspecified.

        This operation requires permissions for the
        `elasticfilesystem:DescribeMountTargets` action, on either the file system ID
        that you specify in `FileSystemId`, or on the file system of the mount target
        that you specify in `MountTargetId`.
        """
        if _request is None:
            _params = {}
            if max_items is not ShapeBase.NOT_SET:
                _params['max_items'] = max_items
            if marker is not ShapeBase.NOT_SET:
                _params['marker'] = marker
            if file_system_id is not ShapeBase.NOT_SET:
                _params['file_system_id'] = file_system_id
            if mount_target_id is not ShapeBase.NOT_SET:
                _params['mount_target_id'] = mount_target_id
            _request = shapes.DescribeMountTargetsRequest(**_params)
        response = self._boto_client.describe_mount_targets(
            **_request.to_boto_dict()
        )

        return shapes.DescribeMountTargetsResponse.from_boto_dict(response)

    def describe_tags(
        self,
        _request: shapes.DescribeTagsRequest = None,
        *,
        file_system_id: str,
        max_items: int = ShapeBase.NOT_SET,
        marker: str = ShapeBase.NOT_SET,
    ) -> shapes.DescribeTagsResponse:
        """
        Returns the tags associated with a file system. The order of tags returned in
        the response of one `DescribeTags` call and the order of tags returned across
        the responses of a multi-call iteration (when using pagination) is unspecified.

        This operation requires permissions for the `elasticfilesystem:DescribeTags`
        action.
        """
        if _request is None:
            _params = {}
            if file_system_id is not ShapeBase.NOT_SET:
                _params['file_system_id'] = file_system_id
            if max_items is not ShapeBase.NOT_SET:
                _params['max_items'] = max_items
            if marker is not ShapeBase.NOT_SET:
                _params['marker'] = marker
            _request = shapes.DescribeTagsRequest(**_params)
        response = self._boto_client.describe_tags(**_request.to_boto_dict())

        return shapes.DescribeTagsResponse.from_boto_dict(response)

    def modify_mount_target_security_groups(
        self,
        _request: shapes.ModifyMountTargetSecurityGroupsRequest = None,
        *,
        mount_target_id: str,
        security_groups: typing.List[str] = ShapeBase.NOT_SET,
    ) -> None:
        """
        Modifies the set of security groups in effect for a mount target.

        When you create a mount target, Amazon EFS also creates a new network interface.
        For more information, see CreateMountTarget. This operation replaces the
        security groups in effect for the network interface associated with a mount
        target, with the `SecurityGroups` provided in the request. This operation
        requires that the network interface of the mount target has been created and the
        lifecycle state of the mount target is not `deleted`.

        The operation requires permissions for the following actions:

          * `elasticfilesystem:ModifyMountTargetSecurityGroups` action on the mount target's file system. 

          * `ec2:ModifyNetworkInterfaceAttribute` action on the mount target's network interface.
        """
        if _request is None:
            _params = {}
            if mount_target_id is not ShapeBase.NOT_SET:
                _params['mount_target_id'] = mount_target_id
            if security_groups is not ShapeBase.NOT_SET:
                _params['security_groups'] = security_groups
            _request = shapes.ModifyMountTargetSecurityGroupsRequest(**_params)
        response = self._boto_client.modify_mount_target_security_groups(
            **_request.to_boto_dict()
        )

    def update_file_system(
        self,
        _request: shapes.UpdateFileSystemRequest = None,
        *,
        file_system_id: str,
        throughput_mode: shapes.ThroughputMode = ShapeBase.NOT_SET,
        provisioned_throughput_in_mibps: float = ShapeBase.NOT_SET,
    ) -> shapes.FileSystemDescription:
        """
        Updates the throughput mode or the amount of provisioned throughput of an
        existing file system.
        """
        if _request is None:
            _params = {}
            if file_system_id is not ShapeBase.NOT_SET:
                _params['file_system_id'] = file_system_id
            if throughput_mode is not ShapeBase.NOT_SET:
                _params['throughput_mode'] = throughput_mode
            if provisioned_throughput_in_mibps is not ShapeBase.NOT_SET:
                _params['provisioned_throughput_in_mibps'
                       ] = provisioned_throughput_in_mibps
            _request = shapes.UpdateFileSystemRequest(**_params)
        response = self._boto_client.update_file_system(
            **_request.to_boto_dict()
        )

        return shapes.FileSystemDescription.from_boto_dict(response)
