from fastapi_amis_admin import admin
from fastapi_amis_admin.admin import AdminSite, FieldPermEnum


async def test_perm_fields(site: AdminSite, models):
    @site.register_admin
    class ArticleAdmin(admin.BaseAuthFieldModelAdmin):
        model = models.Article
        read_fields = [
            models.Article.id,
            models.Article.title,
            models.Article.description,
            models.Article.status,
            models.Article.category_id,
        ]
        perm_fields = {
            FieldPermEnum.VIEW: ["id", "title"],
            FieldPermEnum.UPDATE: ["status"],
            FieldPermEnum.CREATE: ["description", "status"],
        }

    site.register_router()
    ins = site.get_admin_or_create(ArticleAdmin)
    # create_permission_fields
    assert "description" in ins.create_permission_fields
    assert "status" in ins.create_permission_fields
    assert "category_id" not in ins.create_permission_fields

    # update_permission_fields
    assert "status" in ins.update_permission_fields
    assert "category_id" not in ins.update_permission_fields

    # read_permission_fields
    assert "id" in ins.read_permission_fields
    # title not in read_permission_fields, because title is required in schema_read
    assert "title" not in ins.read_permission_fields
    assert "category_id" not in ins.read_permission_fields

    # list_permission_fields
    assert "id" in ins.list_permission_fields
    assert "title" in ins.list_permission_fields
    assert "category_id" not in ins.create_permission_fields

    # filter_permission_fields
    assert "id" in ins.filter_permission_fields
    assert "title" in ins.filter_permission_fields
    assert "category_id" not in ins.create_permission_fields


async def test_perm_fields_exclude(site: AdminSite, models):
    @site.register_admin
    class ArticleAdmin(admin.BaseAuthFieldModelAdmin):
        model = models.Article
        read_fields = [
            models.Article.id,
            models.Article.title,
            models.Article.description,
            models.Article.status,
            models.Article.category_id,
        ]
        perm_fields_exclude = {
            FieldPermEnum.VIEW: ["id", "title"],
            FieldPermEnum.UPDATE: ["status"],
            FieldPermEnum.CREATE: ["description", "status"],
        }

    site.register_router()
    ins = site.get_admin_or_create(ArticleAdmin)
    # create_permission_fields
    assert "description" not in ins.create_permission_fields
    assert "status" not in ins.create_permission_fields
    assert "category_id" in ins.create_permission_fields

    # update_permission_fields
    assert "status" not in ins.update_permission_fields
    assert "category_id" in ins.update_permission_fields

    # read_permission_fields
    assert "id" not in ins.read_permission_fields
    # title not in read_permission_fields, because title is required in schema_read
    assert "title" not in ins.read_permission_fields
    assert "category_id" in ins.read_permission_fields

    # list_permission_fields
    assert "id" not in ins.list_permission_fields
    assert "title" not in ins.list_permission_fields
    assert "category_id" in ins.create_permission_fields

    # filter_permission_fields
    assert "id" not in ins.filter_permission_fields
    assert "title" not in ins.filter_permission_fields
    assert "category_id" in ins.create_permission_fields


async def test_perm_fields_and_exclude(site: AdminSite, models):
    @site.register_admin
    class ArticleAdmin(admin.BaseAuthFieldModelAdmin):
        model = models.Article
        read_fields = [
            models.Article.id,
            models.Article.title,
            models.Article.description,
            models.Article.status,
            models.Article.category_id,
        ]
        perm_fields = {
            FieldPermEnum.VIEW: ["id", "title"],
            FieldPermEnum.UPDATE: ["status", "title"],
            FieldPermEnum.CREATE: ["description", "status"],
        }
        perm_fields_exclude = {
            FieldPermEnum.VIEW: ["title"],
            FieldPermEnum.UPDATE: ["status"],
            FieldPermEnum.CREATE: ["description"],
        }

    site.register_router()
    ins = site.get_admin_or_create(ArticleAdmin)
    # create_permission_fields
    assert "description" not in ins.create_permission_fields
    assert "status" in ins.create_permission_fields
    assert "category_id" not in ins.create_permission_fields

    # update_permission_fields
    assert "title" in ins.update_permission_fields
    assert "status" not in ins.update_permission_fields
    assert "category_id" not in ins.update_permission_fields

    # read_permission_fields
    assert "id" in ins.read_permission_fields
    # title not in read_permission_fields, because title is required in schema_read
    assert "title" not in ins.read_permission_fields
    assert "category_id" not in ins.read_permission_fields

    # list_permission_fields
    assert "id" in ins.list_permission_fields
    assert "title" not in ins.list_permission_fields
    assert "category_id" not in ins.create_permission_fields

    # filter_permission_fields
    assert "id" in ins.filter_permission_fields
    assert "title" not in ins.filter_permission_fields
    assert "category_id" not in ins.create_permission_fields
