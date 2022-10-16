from fastapi_amis_admin.amis.components import Page, PageSchema


def test_Page():
    page = Page(title="Title", body="Hello World!")
    page_json = r'{"type":"page","title":"Title","body":"Hello World!"}'
    assert page.amis_json() == page_json
    assert page.amis_dict() == {"type": "page", "title": "Title", "body": "Hello World!"}
    assert page.amis_html().find(page_json)


def test_extra_fields():
    tmp = PageSchema(schema=Page(), children=[PageSchema()], extra_field="extra field")  # type: ignore
    assert tmp.amis_dict().get("extra_field") == "extra field"
