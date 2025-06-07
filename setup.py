from setuptools import setup, find_packages

setup(
    name="dataoperator",
    version="0.1.0",
    description="",
    author="Joe Fusaro",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
)