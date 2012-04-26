from setuptools import setup

import elements

setup(
    name="django-elements",
    version=elements.__version__,
    license="MIT",
    url="https://github.com/wnielson/django-elements",
    author="Weston Nielson",
    author_email="wnielson@github",
    description="Enhanced Markdown editing for Django projects.",
    keywords="django markdown macros",
    packages=[
        "elements",
        "elements.extensions",
        "elements.templatetags"
    ],
    include_package_data = True,
    package_data={
        "elements": [
            "static/elements/markitup/markdown/*.js",
            "static/elements/markitup/markdown/*.css",
            "static/elements/markitup/markdown/images/*.png",
            "templates/elements/*.html"
        ]
    },
    zip_safe=False,
    install_requires=[
        "markdown",
        "markdown-macros"
    ]
)