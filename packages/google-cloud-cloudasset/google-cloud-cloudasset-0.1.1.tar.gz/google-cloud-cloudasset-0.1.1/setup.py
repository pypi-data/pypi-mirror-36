# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import os

import setuptools

# Package metadata.

name = 'google-cloud-cloudasset'
description = 'Cloud Asset API API client library'
version = '0.1.1'
# Should be one of:
# 'Development Status :: 3 - Alpha'
# 'Development Status :: 4 - Beta'
# 'Development Status :: 5 - Production/Stable'
release_status = 'Development Status :: 7 - Inactive'
dependencies = [
]

setuptools.setup(
    name=name,
    version=version,
    description="This package is obsolete. Please install `google-cloud-asset`.",
    author='Google LLC',
    author_email='googleapis-packages@google.com',
    license='Apache 2.0',
    url='https://github.com/GoogleCloudPlatform/google-cloud-python',
    classifiers=[
        release_status,
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
        'Topic :: Internet',
    ],
    platforms='Posix; MacOS X; Windows',
    include_package_data=True,
    zip_safe=False,
)
