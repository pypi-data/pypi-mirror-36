# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from setuptools import setup, find_packages
from setuptools.command.install import install
from subprocess import check_call

class InstallPluginCommand(install):
    def run(self):
        install.run(self)
        check_call(['pulumi', 'plugin', 'install', 'resource', 'azure', 'v0.15.2'])

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='pulumi_azure',
      version='0.15.2',
      description='A Pulumi package for creating and managing Microsoft Azure cloud resources.',
      long_description=readme(),
      cmdclass={
          'install': InstallPluginCommand,
      },
      keywords='pulumi azure',
      url='https://pulumi.io',
      project_urls={
          'Repository': 'https://github.com/pulumi/pulumi-azure'
      },
      license='Apache 2.0',
      packages=find_packages(),
      install_requires=[
          'pulumi>=0.15.1,<0.16.0'
      ],
      zip_safe=False)
