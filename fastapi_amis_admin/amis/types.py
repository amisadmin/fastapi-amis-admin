from typing import Dict, Any, Union, List
import ujson
from pydantic import BaseModel, Extra

Expression = str
Template = Union[str, "Tpl"]
SchemaNode = Union[Template, "AmisNode", List["AmisNode"], dict]
OptionsNode = Union[List[dict], List[str]]


class BaseAmisModel(BaseModel):
    class Config:
        extra = Extra.allow
        json_loads = ujson.loads
        json_dumps = ujson.dumps

    def amis_json(self):
        return self.json(exclude_none=True, by_alias=True)

    def amis_dict(self):
        return self.dict(exclude_none=True, by_alias=True)

    def update_from_dict(self, kwargs: Dict[str, Any]):
        for k, v in kwargs.items():
            setattr(self, k, v)
        return self

    def update_from_kwargs(self, **kwargs):
        self.update_from_dict(kwargs)
        return self


class BaseAmisApiOut(BaseAmisModel):
    """api接口输出数据格式"""
    status: int = 0
    msg: str = ''
    data: dict = None


class AmisNode(BaseAmisModel):
    """组件配置"""
    type: str = None  # 组件类型
    visible: bool = None  # 显示
    hidden: bool = None  # 隐藏
    visibleOn: Expression = None  # 条件显示
    hiddenOn: Expression = None  # 条件显示


class AmisAPI(BaseAmisModel):
    url: Template  # 当前接口 Api 地址
    method: str = 'GET'  # 请求方式 持：get、post、put、delete
    data: Union[str, dict] = None  # 请求的数据体,支持数据映射
    dataType: str = None  # 默认为 json 可以配置成 form 或者 form-data。当 data 中包含文件时，自动会采用 form-data（multipart/form-data） 格式。当配置为 form 时为 application/x-www-form-urlencoded 格式。
    qsOptions: Union[
        str, dict] = None  # 当 dataType 为 form 或者 form-data 的时候有用。具体参数请参考这里，默认设置为: { arrayFormat: 'indices', encodeValuesOnly: true }
    headers: Dict[str, Any] = None  # 请求的头部信息
    sendOn: Expression = None  # 配置请求条件
    cache: int = None  # 设置cache来设置缓存时间，单位是毫秒，在设置的缓存时间内，同样的请求将不会重复发起，而是会获取缓存好的请求响应数据。
    requestAdaptor: str = None  # 发送适配器 , amis 的 API 配置，如果无法配置出你想要的请求结构，那么可以配置requestAdaptor发送适配器
    responseData: Dict[
        str, Any] = None  # 如果接口返回的数据结构不符合预期，可以通过配置 responseData来修改，同样支持数据映射，可用来映射的数据为接口的实际数据（接口返回的 data 部分），额外加 api 变量。其中 api.query 为接口发送的 query 参数，api.body 为接口发送的内容体原始数据。
    replaceData: bool = None  # 返回的数据是否替换掉当前的数据，默认为 false，即：追加，设置成 true 就是完全替换。
    adaptor: str = None  # 接收适配器, 如果接口返回不符合要求，可以通过配置一个适配器来处理成 amis 需要的。同样支持 Function 或者 字符串函数体格式
    responseType: str = None  # 返回类型 ,如果是下载需要设置为 'blob'
    autoRefresh: bool = None  # 配置是否需要自动刷新接口。
    trackExpression: str = None  # 配置跟踪变量表达式,当开启自动刷新的时候，默认是 api 的 url 来自动跟踪变量变化的。 如果你希望监控 url 外的变量，请配置 traceExpression。


API = Union[str, AmisAPI, dict]
