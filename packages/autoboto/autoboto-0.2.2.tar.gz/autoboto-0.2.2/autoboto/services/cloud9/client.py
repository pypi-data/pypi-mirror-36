import datetime
import typing
import boto3
from autoboto import ShapeBase, OutputShapeBase
from . import shapes


class Client:
    def __init__(self, *args, **kwargs):
        self._boto_client = boto3.client("cloud9", *args, **kwargs)

    def create_environment_ec2(
        self,
        _request: shapes.CreateEnvironmentEC2Request = None,
        *,
        name: str,
        instance_type: str,
        description: str = ShapeBase.NOT_SET,
        client_request_token: str = ShapeBase.NOT_SET,
        subnet_id: str = ShapeBase.NOT_SET,
        automatic_stop_time_minutes: int = ShapeBase.NOT_SET,
        owner_arn: str = ShapeBase.NOT_SET,
    ) -> shapes.CreateEnvironmentEC2Result:
        """
        Creates an AWS Cloud9 development environment, launches an Amazon Elastic
        Compute Cloud (Amazon EC2) instance, and then connects from the instance to the
        environment.
        """
        if _request is None:
            _params = {}
            if name is not ShapeBase.NOT_SET:
                _params['name'] = name
            if instance_type is not ShapeBase.NOT_SET:
                _params['instance_type'] = instance_type
            if description is not ShapeBase.NOT_SET:
                _params['description'] = description
            if client_request_token is not ShapeBase.NOT_SET:
                _params['client_request_token'] = client_request_token
            if subnet_id is not ShapeBase.NOT_SET:
                _params['subnet_id'] = subnet_id
            if automatic_stop_time_minutes is not ShapeBase.NOT_SET:
                _params['automatic_stop_time_minutes'
                       ] = automatic_stop_time_minutes
            if owner_arn is not ShapeBase.NOT_SET:
                _params['owner_arn'] = owner_arn
            _request = shapes.CreateEnvironmentEC2Request(**_params)
        response = self._boto_client.create_environment_ec2(
            **_request.to_boto_dict()
        )

        return shapes.CreateEnvironmentEC2Result.from_boto_dict(response)

    def create_environment_membership(
        self,
        _request: shapes.CreateEnvironmentMembershipRequest = None,
        *,
        environment_id: str,
        user_arn: str,
        permissions: shapes.MemberPermissions,
    ) -> shapes.CreateEnvironmentMembershipResult:
        """
        Adds an environment member to an AWS Cloud9 development environment.
        """
        if _request is None:
            _params = {}
            if environment_id is not ShapeBase.NOT_SET:
                _params['environment_id'] = environment_id
            if user_arn is not ShapeBase.NOT_SET:
                _params['user_arn'] = user_arn
            if permissions is not ShapeBase.NOT_SET:
                _params['permissions'] = permissions
            _request = shapes.CreateEnvironmentMembershipRequest(**_params)
        response = self._boto_client.create_environment_membership(
            **_request.to_boto_dict()
        )

        return shapes.CreateEnvironmentMembershipResult.from_boto_dict(response)

    def delete_environment(
        self,
        _request: shapes.DeleteEnvironmentRequest = None,
        *,
        environment_id: str,
    ) -> shapes.DeleteEnvironmentResult:
        """
        Deletes an AWS Cloud9 development environment. If an Amazon EC2 instance is
        connected to the environment, also terminates the instance.
        """
        if _request is None:
            _params = {}
            if environment_id is not ShapeBase.NOT_SET:
                _params['environment_id'] = environment_id
            _request = shapes.DeleteEnvironmentRequest(**_params)
        response = self._boto_client.delete_environment(
            **_request.to_boto_dict()
        )

        return shapes.DeleteEnvironmentResult.from_boto_dict(response)

    def delete_environment_membership(
        self,
        _request: shapes.DeleteEnvironmentMembershipRequest = None,
        *,
        environment_id: str,
        user_arn: str,
    ) -> shapes.DeleteEnvironmentMembershipResult:
        """
        Deletes an environment member from an AWS Cloud9 development environment.
        """
        if _request is None:
            _params = {}
            if environment_id is not ShapeBase.NOT_SET:
                _params['environment_id'] = environment_id
            if user_arn is not ShapeBase.NOT_SET:
                _params['user_arn'] = user_arn
            _request = shapes.DeleteEnvironmentMembershipRequest(**_params)
        response = self._boto_client.delete_environment_membership(
            **_request.to_boto_dict()
        )

        return shapes.DeleteEnvironmentMembershipResult.from_boto_dict(response)

    def describe_environment_memberships(
        self,
        _request: shapes.DescribeEnvironmentMembershipsRequest = None,
        *,
        user_arn: str = ShapeBase.NOT_SET,
        environment_id: str = ShapeBase.NOT_SET,
        permissions: typing.List[shapes.Permissions] = ShapeBase.NOT_SET,
        next_token: str = ShapeBase.NOT_SET,
        max_results: int = ShapeBase.NOT_SET,
    ) -> shapes.DescribeEnvironmentMembershipsResult:
        """
        Gets information about environment members for an AWS Cloud9 development
        environment.
        """
        if _request is None:
            _params = {}
            if user_arn is not ShapeBase.NOT_SET:
                _params['user_arn'] = user_arn
            if environment_id is not ShapeBase.NOT_SET:
                _params['environment_id'] = environment_id
            if permissions is not ShapeBase.NOT_SET:
                _params['permissions'] = permissions
            if next_token is not ShapeBase.NOT_SET:
                _params['next_token'] = next_token
            if max_results is not ShapeBase.NOT_SET:
                _params['max_results'] = max_results
            _request = shapes.DescribeEnvironmentMembershipsRequest(**_params)
        response = self._boto_client.describe_environment_memberships(
            **_request.to_boto_dict()
        )

        return shapes.DescribeEnvironmentMembershipsResult.from_boto_dict(
            response
        )

    def describe_environment_status(
        self,
        _request: shapes.DescribeEnvironmentStatusRequest = None,
        *,
        environment_id: str,
    ) -> shapes.DescribeEnvironmentStatusResult:
        """
        Gets status information for an AWS Cloud9 development environment.
        """
        if _request is None:
            _params = {}
            if environment_id is not ShapeBase.NOT_SET:
                _params['environment_id'] = environment_id
            _request = shapes.DescribeEnvironmentStatusRequest(**_params)
        response = self._boto_client.describe_environment_status(
            **_request.to_boto_dict()
        )

        return shapes.DescribeEnvironmentStatusResult.from_boto_dict(response)

    def describe_environments(
        self,
        _request: shapes.DescribeEnvironmentsRequest = None,
        *,
        environment_ids: typing.List[str],
    ) -> shapes.DescribeEnvironmentsResult:
        """
        Gets information about AWS Cloud9 development environments.
        """
        if _request is None:
            _params = {}
            if environment_ids is not ShapeBase.NOT_SET:
                _params['environment_ids'] = environment_ids
            _request = shapes.DescribeEnvironmentsRequest(**_params)
        response = self._boto_client.describe_environments(
            **_request.to_boto_dict()
        )

        return shapes.DescribeEnvironmentsResult.from_boto_dict(response)

    def list_environments(
        self,
        _request: shapes.ListEnvironmentsRequest = None,
        *,
        next_token: str = ShapeBase.NOT_SET,
        max_results: int = ShapeBase.NOT_SET,
    ) -> shapes.ListEnvironmentsResult:
        """
        Gets a list of AWS Cloud9 development environment identifiers.
        """
        if _request is None:
            _params = {}
            if next_token is not ShapeBase.NOT_SET:
                _params['next_token'] = next_token
            if max_results is not ShapeBase.NOT_SET:
                _params['max_results'] = max_results
            _request = shapes.ListEnvironmentsRequest(**_params)
        response = self._boto_client.list_environments(
            **_request.to_boto_dict()
        )

        return shapes.ListEnvironmentsResult.from_boto_dict(response)

    def update_environment(
        self,
        _request: shapes.UpdateEnvironmentRequest = None,
        *,
        environment_id: str,
        name: str = ShapeBase.NOT_SET,
        description: str = ShapeBase.NOT_SET,
    ) -> shapes.UpdateEnvironmentResult:
        """
        Changes the settings of an existing AWS Cloud9 development environment.
        """
        if _request is None:
            _params = {}
            if environment_id is not ShapeBase.NOT_SET:
                _params['environment_id'] = environment_id
            if name is not ShapeBase.NOT_SET:
                _params['name'] = name
            if description is not ShapeBase.NOT_SET:
                _params['description'] = description
            _request = shapes.UpdateEnvironmentRequest(**_params)
        response = self._boto_client.update_environment(
            **_request.to_boto_dict()
        )

        return shapes.UpdateEnvironmentResult.from_boto_dict(response)

    def update_environment_membership(
        self,
        _request: shapes.UpdateEnvironmentMembershipRequest = None,
        *,
        environment_id: str,
        user_arn: str,
        permissions: shapes.MemberPermissions,
    ) -> shapes.UpdateEnvironmentMembershipResult:
        """
        Changes the settings of an existing environment member for an AWS Cloud9
        development environment.
        """
        if _request is None:
            _params = {}
            if environment_id is not ShapeBase.NOT_SET:
                _params['environment_id'] = environment_id
            if user_arn is not ShapeBase.NOT_SET:
                _params['user_arn'] = user_arn
            if permissions is not ShapeBase.NOT_SET:
                _params['permissions'] = permissions
            _request = shapes.UpdateEnvironmentMembershipRequest(**_params)
        response = self._boto_client.update_environment_membership(
            **_request.to_boto_dict()
        )

        return shapes.UpdateEnvironmentMembershipResult.from_boto_dict(response)
