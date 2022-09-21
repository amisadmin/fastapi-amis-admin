from fastapi_amis_admin.amis.components import Page, PageSchema


def test_Page():
    page = Page(title="标题", body="Hello World!")
    page_json = r'{"type":"page","title":"\u6807\u9898","body":"Hello World!"}'
    assert page.amis_json() == page_json
    assert page.amis_dict() == {"type": "page", "title": "标题", "body": "Hello World!"}
    assert page.amis_html().find(page_json)


def test_extra_fields():
    tmp = PageSchema(schema=Page(), children=[PageSchema()], extra_field="extra field")  # type: ignore
    assert tmp.amis_dict().get("extra_field") == "extra field"
