#!/usr/bin/env python
"""
@copyright: 2016
@author: Steve Malenfant http://github.com/smalenfant
@author: Hank Beatty http://github.com/hbeatty
@organization:
@license: Apache-2.0
"""
#  This file is part of traffic-control-python.
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
import time

from traffic_control import TrafficOps as to
from traffic_control import TrafficMonitor as tm

# base_url = "https://cms2.kabletown.test"
# to_conn = to(base_url, token = '91504CE6-8E4A-46B2-9F9F-FE7C15228498');
to_conn = to(base_url, user = 'user', password = 'password');

#servers = to_conn.get_servers()
#print json.dumps(servers, indent=3, separators=(',', ': '))
#
#cg = to_conn.get_cachegroups()
#for i in cg:
#  print (i)
#  #print json.dumps(i, indent=3, separators=(',', ': '))
#
#server = to_conn.get_server('atledge01')
#print server


#start_time = int(time.time())
#profiles = to_conn.get_profiles()
#for profile in profiles:
#  print profile
#  params = to_conn.get_profile_parameters(profile=profile,include_config_filter=['grub.conf','kickstart'])
#  print params
#response_time = int((time.time() - start_time) * 1000)
#print "Time to get profiles 1 by 1: %f" % response_time

#start_time = int(time.time())
# Test geting all parameters for all profiles (takes a while)
#params = to_conn.get_profile_parameters()
# print (params)
#response_time = int((time.time() - start_time) * 1000)
#print "Time to get profiles in bulk: %f" % response_time

#serverchecks = to_conn.get_serverchecks()
#print json.dumps(serverchecks, indent=3, separators=(',', ': '))

#res = to_conn.add_to_extension('TX_ERR', '0.0.1', '-', 'test.py', '1', '', 'Checks for TX errors', 'TX_ERR', 'CHECK_EXTENSION_BOOL')
#print res
#
#res = to_conn.add_to_extension('RX_ERR', '0.0.1', '-', 'test.py', '1', '', 'Checks for RX errors', 'RX_ERR', 'CHECK_EXTENSION_NUM')
#print res

# res = to_conn.add_to_extension('SYNCDS_ERR_CNT', '0.0.1', '-', 'traffic_ops_ort.pl', '1', '', 'Sync DS Errors', 'SYNCDS', 'CHECK_EXTENSION_NUM')
# print res

#to_extensions = to_conn.get_to_extensions()
#print json.dumps(to_extensions, indent=3, separators=(',', ': '))

#deliveryservices = to_conn.get_deliveryservices()
#for i in deliveryservices:
#   print json.dumps(i, indent=3, separators=(',', ': '))
#
#
#for i in servers:
#   print i['hostName']
#   #print i['response']['id'] + " "  i['response']['hostName']
#   if (i['type'] == 'MID') or (i['type'] == 'EDGE'):
#      res = to_conn.post_serverchecks(i['id'], i['hostName'], 'RX_ERR', 21)
#      print res

tm_conn = tm(to_conn)

print json.dumps(tm_conn.servers, indent=3, separators=(',', ': '))

#cache_stats = y.get_cache_stats(stats="ats.proxy.process.cluster.write_bytes,ats.proxy.process.cluster.connections_open",hc="2")
#print json.dumps(cache_stats, indent=3, separators=(',', ': '))

