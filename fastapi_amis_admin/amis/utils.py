import os
from functools import lru_cache
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@lru_cache()
def amis_templates(template_name: str = 'page.html', template_path: str = ''):
    """页面模板"""
    template_path = template_path or f'{BASE_DIR}/templates/{template_name}'
    with open(template_path, encoding='utf8') as f:
        tmp = f.read()
    return tmp
