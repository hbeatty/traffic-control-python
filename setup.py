"""
Setup file for egg builds
@copyright: 2016
@author: Steve Malenfant http://github.com/smalenfant
@author: Hank Beatty http://github.com/hbeatty
@organization: Cox Communications Inc. - Advanced Network Platforms
@license: Apache-2.0
"""
#  This file is part of traffic-ops-python.
#
#  Copyright 2016 Cox Communications Inc.
#  
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  
#      http://www.apache.org/licenses/LICENSE-2.0
#  
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import re

from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'traffic_control', '__init__.py')) as f:
    version = re.search("__version__ = '([^']+)'", f.read()).group(1)

# setup meta data and entry points
setup(
    name='traffic-control',
    version = version,
    description="Traffic Control Python API",
    author="Steve Malenfant, Hank Beatty",
    author_email="smalenfant@users.noreply.github.com, hbeatty@users.noreply.github.com",
    license="Apache-2.0",

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        #'Topic :: Software Development :: ',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache-2.0',
        'Operating System :: OS Independent',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3',
        #'Programming Language :: Python :: 3.3',
        #'Programming Language :: Python :: 3.4',
        #'Programming Language :: Python :: 3.5',
    ],

    install_requires = ['requests','argparse'],
    packages=find_packages(),
    package_data={'traffic-control':['docs/*','traffic_control/*']},
    include_package_data=True    
    )
