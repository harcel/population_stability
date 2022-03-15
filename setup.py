from setuptools import setup

setup(
    name="unstable_populations",
    version="0.2.1",
    author="Marcel Haas, Joris Huese, Lisette Sibbald",
    author_email="datascience@marcelhaas.com",
    packages=["unstable_populations", "unstable_populations.test"],
    url="http://pypi.python.org/pypi/PackageName/",
    license=open("LICENSE").read(),
    description="Package to calculate Unstable Population Indicator and related population stability indices.",
    long_description=open("README.md").read(),
    install_requires=[
        "numpy >= 1.0.0",
        "pytest",
    ],
)
