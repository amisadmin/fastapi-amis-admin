from typing import Any, Dict, List, Optional, Union

from fastapi_amis_admin.utils.pydantic import AllowExtraModelMixin

Expression = str


OptionsNode = Union[List[Dict[str, Any]], List[str]]


class BaseAmisModel(AllowExtraModelMixin):
    """Base model for amis"""

    def amis_json(self):
        return self.json(exclude_none=True, by_alias=True)

    def amis_dict(self):
        return self.dict(exclude_none=True, by_alias=True)

    def update_from_dict(self, kwargs: Dict[str, Any]):
        for k, v in kwargs.items():
            setattr(self, k, v)
        return self

    def update_from_kwargs(self, **kwargs):
        return self.update_from_dict(kwargs)


class BaseAmisApiOut(BaseAmisModel):
    """api interface output data format"""

    status: int = 0
    msg: str = ""
    data: Optional[dict] = None


class AmisNode(BaseAmisModel):
    """Component configuration"""

    type: Optional[str] = None  # component type
    visible: Optional[bool] = None  # show
    hidden: Optional[bool] = None  # hide
    visibleOn: Optional[Expression] = None  # conditional display
    hiddenOn: Optional[Expression] = None  # conditional display
    id: Optional[str] = None
    name: Optional[str] = None  # In other components, when used as a variable map
    value: Optional[Any] = None  # The value of the component
    onEvent: Optional[dict] = None
    events: Optional[Dict[str, Any]] = None  # Specifies the amis behavior triggered by the component


SchemaNode = Union[str, AmisNode, List[AmisNode], Dict[str, Any], List[Dict[str, Any]]]


class AmisAPI(BaseAmisModel):
    url: str  # Current interface API address
    method: Optional[str] = None  # 'GET' # Request method: get, post, put, delete
    data: Union[str, dict, None] = None  # The requested data body, supports data mapping
    dataType: Optional[str] = None  # The default is json and can be configured as form or form-data.
    # When data contains files, it will automatically use form-data (multipart/form-data) format.
    # When configured as form, the format is application/x-www-form-urlencoded.
    qsOptions: Union[str, dict, None] = None  # Useful when dataType is form or form-data.
    # For specific parameters, please refer to here, the default setting is: { arrayFormat: 'indices',
    # encodeValuesOnly: true }
    headers: Optional[Dict[str, Any]] = None  # Request header information
    sendOn: Optional[Expression] = None  # Configure request conditions
    cache: Optional[int] = None  # Set cache to set the cache time, the unit is milliseconds. During the set cache time,
    # the same request will not be repeated, but the cached request response data will be obtained.
    requestAdaptor: Optional[str] = None  # Send adapter, API configuration of amis, if you can't configure the request
    # structure you want, you can configure the requestAdaptor send adapter
    responseData: Optional[Dict[str, Any]] = None  # If the data structure returned by the interface is not as expected, it can
    # be modified by configuring responseData, which also supports data mapping. The data that can be used for
    # mapping is the actual data of the interface (the data part returned by the interface), plus the api variable.
    # Among them, api.query is the query parameter sent by the interface, and api.body is the original data of the
    # content body sent by the interface.
    replaceData: Optional[bool] = None  # Whether the returned data replaces the current data, the default is false, that is:
    # append, set to true to completely replace.
    adaptor: Optional[str] = None  # Receive adapter, if the interface return does not meet the requirements, you can configure
    # an adapter to handle it as required by amis.  Also supports Function or string function body format
    responseType: Optional[str] = None  # Return type, if it is a download, it needs to be set to 'blob'
    autoRefresh: Optional[bool] = None  # Configure whether to automatically refresh the interface.
    trackExpression: Optional[str] = None  # Configure the tracking variable expression. When automatic refresh is enabled,
    # the default is the url of the api to automatically track variable changes. If you want to monitor variables
    # outside the url, configure traceExpression.


API = Union[str, AmisAPI, dict]


class Tpl(AmisNode):
    type: str = "tpl"  # Specify as Tpl component
    tpl: str  # configuration template
    className: Optional[str] = None  # The class name of the outer Dom


Template = Union[str, Tpl]


class Event(BaseAmisModel):
    actionType: Optional[str] = None  # Action name
    args: Optional[dict] = None  # Action parameter {key:value}, support data mapping
    preventDefault: Union[bool, Expression, None] = None  # "False" # Prevent event default behavior, > 1.10.0 and above
    # support expressions
    stopPropagation: Union[bool, Expression, None] = None  # "False" # Stop subsequent action execution, > 1.10.0 and above
    # supports expressions
    expression: Union[bool, Expression, None] = None  # Execution condition, not set means default execution
    outputVar: Optional[str] = None  # output data variable name
