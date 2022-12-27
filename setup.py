from setuptools import setup, find_packages
from codecs import open

from django_ipfs import __version__


try:
    import pypandoc

    long_description = pypandoc.convert("README.md", "rst")
except (IOError, ImportError):
    with open("README.rst", encoding="utf-8") as f:
        long_description = f.read()


setup(
    name="django-ipfs",
    description="IPFS storage backend for Django.",
    long_description=long_description,
    keywords="django ipfs storage",
    version=__version__,
    author_email="kalinin.mitko@gmail.com",
    url="https://github.com/null-none/django-ipfs",
    classifiers=(
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Framework :: Django",
    ),
    packages=find_packages(),
    install_requires=(
        "django",
        "ipfsapi",
    ),
    setup_requires=("pypandoc",),
)
