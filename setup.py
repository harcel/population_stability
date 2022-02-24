# Example!! Still to adapt.

from setuptools import setup

setup(
    name="unstable_populations",
    version="0.1.0",
    author="An Awesome Coder",
    author_email="aac@example.com",
    packages=["unstable_populations", "unstable_populations.test"],
    # scripts=['bin/','bin/script2'],
    url="http://pypi.python.org/pypi/PackageName/",
    license="LICENSE",
    description="An awesome package that does something",
    long_description=open("README.txt").read(),
    install_requires=[
        "numpy >= 1.0.0",
        "pytest",
    ],
)
