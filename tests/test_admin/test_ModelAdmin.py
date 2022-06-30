import pytest
from httpx import AsyncClient

from fastapi_amis_admin import admin
from fastapi_amis_admin.admin import AdminSite
from tests.models import User, Article


async def test_register_router(site: AdminSite):
    site.register_admin(admin.ModelAdmin)
    with pytest.raises(AssertionError) as exc:
        ins = site.get_admin_or_create(admin.ModelAdmin)
    assert exc.match('model is None')
    site.unregister_admin(admin.ModelAdmin)

    @site.register_admin
    class UserAdmin(admin.ModelAdmin):
        model = User

    ins = site.get_admin_or_create(UserAdmin)
    assert ins.engine
    assert ins.fields
    site.register_router()
    # test openapi
    openapi = site.fastapi.openapi()
    paths = openapi['paths']
    assert f'{ins.router_prefix}/list' in paths
    assert f'{ins.router_prefix}/item' in paths
    assert f'{ins.router_prefix}/item/{{item_id}}' in paths


async def test_list_display(site: AdminSite, async_client: AsyncClient):
    @site.register_admin
    class UserAdmin(admin.ModelAdmin):
        model = User
        list_display = [User.id, User.username]

    site.register_router()
    ins = site.get_admin_or_create(UserAdmin)
    assert "username" in ins.schema_list.__fields__

    # test schemas
    openapi = site.fastapi.openapi()
    schemas = openapi['components']['schemas']
    assert "username" in schemas['UserAdminList']['properties']


async def test_list_display_join(site: AdminSite, async_client: AsyncClient):
    @site.register_admin
    class ArticleAdmin(admin.ModelAdmin):
        model = Article
        list_display = [Article.title, User.username, 'description']

    site.register_router()

    ins = site.get_admin_or_create(ArticleAdmin)
    assert 'user_username' in ins.schema_list.__fields__
    assert 'description' in ins.schema_list.__fields__

    # test schemas
    site.fastapi.openapi_schema = None
    openapi = site.fastapi.openapi()
    schemas = openapi['components']['schemas']
    assert 'user__username' in schemas['ArticleAdminList']['properties']
