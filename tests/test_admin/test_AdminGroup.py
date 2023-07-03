from fastapi_amis_admin import admin
from fastapi_amis_admin.admin import AdminSite
from fastapi_amis_admin.admin.admin import AdminGroup


class DocsAdmin(admin.IframeAdmin):
    src = "https://docs.amis.work"


class TmpLinkAdmin(admin.LinkAdmin):
    link = "https://www.baidu.com"


async def test_AdminGroup(site: AdminSite):
    group = site.get_admin_or_create(AdminGroup)
    docs_admin = DocsAdmin(site)
    link_admin = TmpLinkAdmin(site)

    # test append_child
    group.append_child(link_admin)
    group.append_child(docs_admin)
    assert docs_admin in group

    # test get_page_schema_child
    admin, parent = group.get_page_schema_child(docs_admin.unique_id)
    assert admin is docs_admin
    assert parent is group

    # test get_page_schema_children
    children = await group.get_page_schema_children(None)  # type: ignore
    assert len(children) == 2

    # test site.get_page_schema_child
    admin, parent = site.get_page_schema_child(docs_admin.unique_id)
    assert admin is docs_admin
    assert parent is group

    # test site.get_page_schema_children
    children = await site.get_page_schema_children(None)  # type: ignore
    assert len(children) == 1
    assert len(children[0].children) == 2

    # test remove_child
    group.remove_child(docs_admin.unique_id)
    assert docs_admin not in group

    # test get_page_schema_child
    admin, parent = group.get_page_schema_child(docs_admin.unique_id)
    assert admin is None
    assert parent is None

    # test get_page_schema_children
    children = await group.get_page_schema_children(None)  # type: ignore
    assert len(children) == 1

    # test site.get_page_schema_child
    admin, parent = site.get_page_schema_child(docs_admin.unique_id)
    assert admin is None
    assert parent is None

    # test site.get_page_schema_children
    children = await site.get_page_schema_children(None)  # type: ignore
    assert len(children) == 1
    assert len(children[0].children) == 1
