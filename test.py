#!/usr/bin/env python
"""
@copyright: 2016
@author: Steve Malenfant http://github.com/smalenfant
@author: Hank Beatty http://github.com/hbeatty
@organization: Cox Communications Inc. - Advanced Network Platforms
@license: Apache-2.0
"""
#  This file is part of traffic-control-python.
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

import json

from traffic_control import TrafficOps as to

base_url = "https://cdn3cdcms0001.coxlab.net"
#base_url = "https://cms.kabletown.net"
x = to(base_url, token = '91504CE6-8E4A-46B2-9F9F-FE7C15228498');

servers = x.get_servers()
for i in servers:
   print i

to_extensions = x.get_to_extensions()
for i in to_extensions:
   print i

deliveryservices = x.get_deliveryservices()
for i in deliveryservices:
   print i

res = x.add_to_extension('TX_ERR', '0.0.1', '-', 'test.py', '1', '', 'Checks for TX errors', 'TX_ERR', 'CHECK_EXTENSION_BOOL')
print res

res = x.add_to_extension('RX_ERR', '0.0.1', '-', 'test.py', '1', '', 'Checks for RX errors', 'RX_ERR', 'CHECK_EXTENSION_NUM')
print res

for i in servers:
   print i['hostName']
   #print i['response']['id'] + " "  i['response']['hostName']
   if (i['type'] == 'MID') or (i['type'] == 'EDGE'):
      res = x.post_serverchecks(i['id'], i['hostName'], 'RX_ERR', 21)
      print res
