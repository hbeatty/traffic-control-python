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
from traffic_control import TrafficMonitor as tm

base_url = "https://cms.kabletown.net"
to_conn = to(base_url, token = '91504CE6-8E4A-46B2-9F9F-FE7C15228498');

#servers = to_conn.get_servers()
#for i in servers:
#   print json.dumps(i, indent=3, separators=(',', ': '))

serverchecks = to_conn.get_serverchecks()
print json.dumps(serverchecks, indent=3, separators=(',', ': '))
#for i in serverchecks:
#   print json.dumps(serverchecks[i], indent=3, separators=(',', ': '))

#to_extensions = to_conn.get_to_extensions()
#for i in to_extensions:
#   print json.dumps(i, indent=3, separators=(',', ': '))
#
#deliveryservices = to_conn.get_deliveryservices()
#for i in deliveryservices:
#   print json.dumps(i, indent=3, separators=(',', ': '))
#
#res = to_conn.add_to_extension('TX_ERR', '0.0.1', '-', 'test.py', '1', '', 'Checks for TX errors', 'TX_ERR', 'CHECK_EXTENSION_BOOL')
#print res
#
#res = to_conn.add_to_extension('RX_ERR', '0.0.1', '-', 'test.py', '1', '', 'Checks for RX errors', 'RX_ERR', 'CHECK_EXTENSION_NUM')
#print res
#
#for i in servers:
#   print i['hostName']
#   #print i['response']['id'] + " "  i['response']['hostName']
#   if (i['type'] == 'MID') or (i['type'] == 'EDGE'):
#      res = to_conn.post_serverchecks(i['id'], i['hostName'], 'RX_ERR', 21)
#      print res
#
#tm_conn = tm(to_conn)

#print json.dumps(tm_conn.servers, indent=3, separators=(',', ': '))
#
#cache_stats = y.get_cache_stats(stats="ats.proxy.process.cluster.write_bytes,ats.proxy.process.cluster.connections_open",hc="2")
#print json.dumps(cache_stats, indent=3, separators=(',', ': '))
