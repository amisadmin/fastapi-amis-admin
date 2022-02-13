from fastapi_amis_admin.amis.components import Page, PageSchema


def test_Page():
    page = Page(title='标题', body='Hello World!')
    page_json = r'{"type":"page","title":"\u6807\u9898","body":"Hello World!"}'
    assert page.amis_json() == page_json
    assert page.amis_dict() == {'type': 'page', 'title': '标题', 'body': 'Hello World!'}
    assert page.amis_html().find(page_json)


def test_PageSchema():
    tmp = PageSchema(schema=Page(), children=[PageSchema()], tmp_field='tmp field')  # type: ignore
    amis_json = '{"schema":{"type":"page"},"children":[{}],"tmp_field":"tmp field"}'
    assert tmp.amis_json() == amis_json
