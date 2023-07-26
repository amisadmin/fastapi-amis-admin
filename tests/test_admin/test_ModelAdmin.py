import pytest
from httpx import AsyncClient
from pydantic import Field
from sqlalchemy.sql import Select
from starlette.requests import Request

from fastapi_amis_admin import admin
from fastapi_amis_admin.admin import AdminSite
from fastapi_amis_admin.crud.parser import LabelField
from fastapi_amis_admin.utils.pydantic import model_fields


async def test_register_router(site: AdminSite, models):
    site.register_admin(admin.ModelAdmin)
    with pytest.raises(AssertionError) as exc:
        ins = site.get_admin_or_create(admin.ModelAdmin)
    assert exc.match("model is None")
    site.unregister_admin(admin.ModelAdmin)

    @site.register_admin
    class UserAdmin(admin.ModelAdmin):
        model = models.User

    ins = site.get_admin_or_create(UserAdmin)
    assert ins.engine
    assert ins.fields
    site.register_router()
    # test openapi
    openapi = site.fastapi.openapi()
    paths = openapi["paths"]
    assert f"{ins.router_prefix}/list" in paths
    assert f"{ins.router_prefix}/item" in paths
    assert f"{ins.router_prefix}/item/{{item_id}}" in paths


async def test_list_display(site: AdminSite, async_client: AsyncClient, models):
    @site.register_admin
    class UserAdmin(admin.ModelAdmin):
        model = models.User
        list_display = [models.User.id, models.User.username]

    site.register_router()
    ins = site.get_admin_or_create(UserAdmin)
    assert "username" in model_fields(ins.schema_list)

    # test schemas
    openapi = site.fastapi.openapi()
    schemas = openapi["components"]["schemas"]
    assert "username" in schemas["UserAdminList"]["properties"]


async def test_list_display_join(site: AdminSite, async_client: AsyncClient, models):
    @site.register_admin
    class ArticleAdmin(admin.ModelAdmin):
        model = models.Article
        list_display = [
            models.Article.title,
            models.User.username,
            "description",
            models.User.username.label("nickname"),
            LabelField(
                label=models.User.password.label("pwd"),
                field=Field(None, title="pwd_title"),
            ),
        ]

        async def get_select(self, request: Request) -> Select:
            sel = await super().get_select(request)
            return sel.outerjoin(models.User, models.User.id == models.Article.user_id)

    site.register_router()

    ins = site.get_admin_or_create(ArticleAdmin)
    # test schemas
    assert "id" in model_fields(ins.schema_list)
    assert "user_username" in model_fields(ins.schema_list)
    assert "description" in model_fields(ins.schema_list)
    assert "nickname" in model_fields(ins.schema_list)
    assert "pwd" in model_fields(ins.schema_list)
    assert model_fields(ins.schema_list)["pwd"].field_info.title == "pwd_title"

    assert "user_username" in model_fields(ins.schema_filter)
    assert "nickname" in model_fields(ins.schema_filter)
    assert "pwd" in model_fields(ins.schema_filter)

    # test openapi
    site.fastapi.openapi_schema = None
    openapi = site.fastapi.openapi()
    schemas = openapi["components"]["schemas"]
    assert "user__username" in schemas["ArticleAdminList"]["properties"]
    assert "description" in schemas["ArticleAdminList"]["properties"]
    assert "nickname" in schemas["ArticleAdminList"]["properties"]
    assert "pwd" in schemas["ArticleAdminList"]["properties"]


async def test_list_filter(site: AdminSite, async_client: AsyncClient, models):
    @site.register_admin
    class UserAdmin(admin.ModelAdmin):
        model = models.User
        list_filter = [models.User.id, models.User.username.label("name")]
        search_fields = [models.User.username]

    site.register_router()
    ins = site.get_admin_or_create(UserAdmin)
    assert "username" in model_fields(ins.schema_filter)

    # test schemas
    openapi = site.fastapi.openapi()
    schemas = openapi["components"]["schemas"]
    assert "id" in schemas["UserAdminFilter"]["properties"]
    assert "username" in schemas["UserAdminFilter"]["properties"]
    assert "name" in schemas["UserAdminFilter"]["properties"]
    assert "password" not in schemas["UserAdminFilter"]["properties"]


async def test_list_filter_default(site: AdminSite, async_client: AsyncClient, models):
    @site.register_admin
    class UserAdmin(admin.ModelAdmin):
        model = models.User

    site.register_router()
    ins = site.get_admin_or_create(UserAdmin)
    assert "username" in model_fields(ins.schema_filter)

    # test schemas
    openapi = site.fastapi.openapi()
    schemas = openapi["components"]["schemas"]
    assert "username" in schemas["UserAdminFilter"]["properties"]
    assert "id" in schemas["UserAdminFilter"]["properties"]
    assert "password" in schemas["UserAdminFilter"]["properties"]
