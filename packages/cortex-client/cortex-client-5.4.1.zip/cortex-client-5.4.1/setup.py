"""
Copyright 2018 Cognitive Scale, Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from setuptools import setup
from setuptools import find_packages


setup(name='cortex-client',
      description="Python SDK for Cognitive Scale's Cortex 5 AI Platform",
      long_description="Python SDK for Cognitive Scale's Cortex 5 AI Platform",
      version='5.4.1',
      author='CognitiveScale',
      author_email='info@cognitivescale.com',
      url='https://docs.cortex.insights.ai',
      license='CognitiveScale Inc.',
      platforms=['linux', 'osx'],
      packages=find_packages(),
      include_package_data=True,
      install_requires=['requests>=2.12.4,<3',
                        'requests-toolbelt==0.8.0',
                        'Flask==1.0',
                        'diskcache>=3.0.5,<3.1',
                        'ipython>=6.4.0',
                        'pyjwt>=1.6.1',
                        'discovery-transitioning-utils>=1.3.50',
                        'dill==0.2.8.2',
                        'dataclasses>=0.6; python_version == "3.6"',
                        'seaborn>=0.9.0',
                        'matplotlib>=2.2.2',
                        'more_itertools>=4.3.0',
                        'pyyaml>=3.13',
                        'cuid>=0.3',
                        'maya==0.5.0',
                        'docker==3.5.0'
                       ],
      tests_require=['mocket>=2.0.0,<3',
                     'mock>=2,<3',
                     'pytest>=3.1,<4'],
      classifiers=[
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 3.6',
          ],
      )
