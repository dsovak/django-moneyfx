from setuptools import setup, find_packages

setup(
    name="django-moneyfx",
    version="0.1.0",
    packages=[
        'moneyfx',
        'moneyfx.migrations'
    ],
    install_requires=[
        "django>=3",
        "django-money>=3.0",
        "requests>=2.31.0",
        "djangorestframework>=3.15.0",
    ],
    author="Dávid Sovák",
    description="Multi-currency utilities for Django",
    include_package_data=True,
)
