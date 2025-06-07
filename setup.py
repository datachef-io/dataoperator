from setuptools import setup, find_packages

setup(
    name="dataoperator",
    version="0.1.0",
    description="",
    author="Joe Fusaro",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    # install_requires=[
    #     # List any dependencies your package needs, e.g. 'pandas>=1.0'
    # ],
    python_requires=">=3.7",
)