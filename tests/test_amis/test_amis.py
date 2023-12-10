from fastapi_amis_admin import amis


def test_Page():
    page = amis.Page(title="Title", body="HelloWorld!")
    page_json = r'{"type":"page","title":"Title","body":"HelloWorld!"}'
    assert page.amis_json().replace(" ", "") == page_json
    assert page.amis_dict() == {"type": "page", "title": "Title", "body": "HelloWorld!"}
    assert page.amis_html().find(page_json)


def test_extra_fields():
    tmp = amis.PageSchema(schema=amis.Page(), children=[amis.PageSchema()], extra_field="extra field")  # type: ignore
    assert tmp.amis_dict().get("extra_field") == "extra field"
