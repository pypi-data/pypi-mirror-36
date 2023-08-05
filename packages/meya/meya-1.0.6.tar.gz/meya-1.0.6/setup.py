# Copyright 2018 Locl Interactive Inc. (d/b/a Meya.ai). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup

setup(
   name='meya',
   version='1.0.6',
   description='Manage Meya bots from command-line, and more.',
   long_description='Manage Meya bots from command-line, enabling you to use your favourite tools while updating live on https://meya.ai. Provides code completion for local IDE\'s.',
   author='Meya.ai',
   author_email='support@meya.ai',
   packages=[],
   install_requires=[
       'meya-cli>=1.0.5',
       'meya-components'
   ],
   entry_points={
   },
   license='Apache License 2.0'
)
