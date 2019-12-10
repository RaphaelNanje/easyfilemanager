from setuptools import setup

setup(
        name='easyfilemanager',
        version='0.4.2',
        description='A library that makes managing data files simple',
        author='Raphael',
        author_email='rtnanje@gmail.com',
        packages=['easyfilemanager'],  # same as name
        install_requires=['logzero', 'pyyaml', 'pandas'],
        # external packages as dependencies
)
