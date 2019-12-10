from setuptools import setup

setup(
        name='easyfilemanager',
        version='2.0.1',
        description='A library that makes managing data files simple',
        author='Raphael',
        author_email='rtnanje@gmail.com',
        packages=['easyfilemanager'],  # same as name
        install_requires=['logzero', 'pyyaml'],
        # external packages as dependencies
)
