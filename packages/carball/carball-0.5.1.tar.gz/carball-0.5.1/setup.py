import setuptools
from setuptools import setup
import os
from carball.analysis.analysis_manager import AnalysisManager

if os.path.isfile('README.md'):
    with open("README.md", "r") as readme_file:
        long_description = readme_file.read()
else:
    long_description = ''

subversion = 1
version_string = '0.' + str(AnalysisManager.PROTOBUF_VERSION) + '.' + str(subversion)
setup(
    name='carball',
    version=version_string,
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['pandas==0.23.4', 'protobuf==3.6.1', 'xlrd'],
    url='https://github.com/SaltieRL/ReplayAnalysis',
    keywords=['rocket-league'],
    license='Apache 2.0',
    author='Matthew Mage, Harry Xie, David Turner',
    author_email='sciguymjm@gmail.com',
    description='Rocket League replay parsing and analysis.',
    long_description=long_description,
    exclude_package_data={'': ['.gitignore', '.git/*', '.git/**/*', 'replays/*']}
)
