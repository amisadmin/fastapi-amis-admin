import pytest
from httpx import AsyncClient

from fastapi_amis_admin import admin
from fastapi_amis_admin.admin import AdminSite
from tests.models import Category, Article

pytestmark = pytest.mark.asyncio


async def test_register_router(site: AdminSite):
    site.register_admin(admin.ModelAdmin)
    with pytest.raises(AssertionError) as exc:
        ins = site.get_admin_or_create(admin.ModelAdmin)
    assert exc.match('model is None')
    site.unregister_admin(admin.ModelAdmin)

    @site.register_admin
    class CategoryAdmin(admin.ModelAdmin):
        model = Category

    ins = site.get_admin_or_create(CategoryAdmin)
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
    class CategoryAdmin(admin.ModelAdmin):
        model = Category
        list_display = [Category.id, Category.name]

    site.register_router()
    ins = site.get_admin_or_create(CategoryAdmin)
    assert 'name' in ins.schema_list.__fields__

    # test schemas
    openapi = site.fastapi.openapi()
    schemas = openapi['components']['schemas']
    assert 'name' in schemas['CategoryAdminList']['properties']


async def test_list_display_join(site: AdminSite, async_client: AsyncClient):
    @site.register_admin
    class ArticleAdmin(admin.ModelAdmin):
        model = Article
        list_display = [Article.title, Category.name, 'description']

    site.register_router()

    ins = site.get_admin_or_create(ArticleAdmin)
    assert 'category_name' in ins.schema_list.__fields__
    assert 'description' in ins.schema_list.__fields__

    # test schemas
    site.fastapi.openapi_schema = None
    openapi = site.fastapi.openapi()
    schemas = openapi['components']['schemas']
    assert 'category__name' in schemas['ArticleAdminList']['properties']
