import datetime
import typing
import boto3
from autoboto import ShapeBase, OutputShapeBase
from . import shapes


class Client:
    def __init__(self, *args, **kwargs):
        self._boto_client = boto3.client(
            "marketplace-entitlement", *args, **kwargs
        )

    def get_entitlements(
        self,
        _request: shapes.GetEntitlementsRequest = None,
        *,
        product_code: str,
        filter: typing.Dict[shapes.GetEntitlementFilterName, typing.List[str]
                           ] = ShapeBase.NOT_SET,
        next_token: str = ShapeBase.NOT_SET,
        max_results: int = ShapeBase.NOT_SET,
    ) -> shapes.GetEntitlementsResult:
        """
        GetEntitlements retrieves entitlement values for a given product. The results
        can be filtered based on customer identifier or product dimensions.
        """
        if _request is None:
            _params = {}
            if product_code is not ShapeBase.NOT_SET:
                _params['product_code'] = product_code
            if filter is not ShapeBase.NOT_SET:
                _params['filter'] = filter
            if next_token is not ShapeBase.NOT_SET:
                _params['next_token'] = next_token
            if max_results is not ShapeBase.NOT_SET:
                _params['max_results'] = max_results
            _request = shapes.GetEntitlementsRequest(**_params)
        response = self._boto_client.get_entitlements(**_request.to_boto_dict())

        return shapes.GetEntitlementsResult.from_boto_dict(response)
