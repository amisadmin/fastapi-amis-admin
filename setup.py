import setuptools
import fastapi_amis_admin


def get_long_description():
    with open("README.md", encoding="utf8") as f:
        return f.read()


setuptools.setup(
    name="fastapi_amis_admin",
    python_requires=">=3.6.1",
    version=fastapi_amis_admin.__version__,
    license="Apache",
    author="Atomi",
    author_email="1456417373@qq.com",
    description="fastapi-amis-admin is a high-performance, efficient and easily extensible FastAPI admin framework. "
                "Inspired by Django-admin, and has as many powerful functions as Django-admin.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url=fastapi_amis_admin.__url__,
    install_requires=[
        "fastapi>=0.68.0",
        "sqlmodel>=0.0.4",
        "ujson>=4.0.1",
        "python-multipart>=0.0.5",
    ],
    packages=setuptools.find_packages(exclude=["tests*"]),
    package_data={"": ["*.md"], "fastapi_amis_admin.amis": ["templates/*.html"]},
    include_package_data=True,
    classifiers=[
        "Framework :: FastAPI",
        "Environment :: Web Environment",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    project_urls={  # Optional
        'Documentation': 'http://docs.amis.work/',
    },
)
