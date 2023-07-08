from fastapi_amis_admin.admin import Settings


def test_settings_valid_url():
    settings = Settings(site_url="/")
    assert settings.site_url == ""
    settings = Settings(amis_cdn="https://unpkg.com/")
    assert settings.amis_cdn == "https://unpkg.com"
    settings = Settings(site_path="/admin/")
    assert settings.site_path == "/admin"
    settings = Settings(site_path="/admin")
    assert settings.site_path == "/admin"


def test_settings_valid_database_url():
    settings = Settings()
    assert settings.database_url_async
    settings = Settings(database_url_async="sqlite+aiosqlite:///amisadmin.db?check_same_thread=False")
    assert settings.database_url == ""
    assert settings.database_url_async
    settings = Settings(database_url="sqlite:///amisadmin.db?check_same_thread=False")
    assert settings.database_url
    assert settings.database_url_async == ""
