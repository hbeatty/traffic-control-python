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


# example cron entry
# 0 * * * * root /opt/traffic_ops/app/bin/checks/ToRX_ERRCheck.py -c "{\"base_url\": \"https://localhost\", \"check_name\": \"RX_ERR\", \"name\": \"RX error check\"}" -v 6 >> /var/log/traffic_ops/extensionCheck.log 2>&1
#
# example cron entry with syslog
# 0 * * * * root /opt/traffic_ops/app/bin/checks/ToRX_ERRCheck.py -c "{\"base_url\": \"https://localhost\", \"check_name\": \"RX_ERR\", \"name\": \"RX error check\", \"syslog_facility\": \"local0\"}" > /dev/null 2>&1

import json
import syslog
import argparse

from traffic_control import TrafficOps as to
from traffic_control import TrafficMonitor as tm

version = '0.0.1'

class switch(object):
   def __init__(self, value):
      self.value = value
      self.fall = False

   def __iter__(self):
      """Return the match method once, then stop"""
      yield self.match
      raise StopIteration

   def match(self, *args):
      """Indicate whether or not to enter a case suite"""
      if self.fall or not args:
         return True
      elif self.value in args:
         self.fall = True
         return True
      else:
         return False

sslg = False

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-c", "--conf", required=True, help="""json formatted list of variables
base_url: required
   URL of the Traffic Ops server.
check_name: optional (default: RX_ERR). Must match column name in serverchecks table.
name: optional
   The long name of this check. used in conjuction with syslog_facility.
syslog_facility: optional
   The syslog facility to send messages. Requires the \"name\" option to
   be set. Syslog facilities are kern, user, mail, daemon, auth, lpr,
   news, uucp, cron, syslog and local0 to local7""")
parser.add_argument("-f", "--force", type=int, help="""Force a FAIL or OK message (recommend adding -q as well)
   1: FAIL: Forces the rx errors 1000 higher than the previous rx errors and disregards actual current.
   2: OK: Makes current rx errors same as previous and disregards actual current.""")
parser.add_argument("-q", "--quiet", action="store_true", help="Don't post to Traffic Ops")
parser.add_argument("-v", "--verbosity", type=int, help="Level of output 1-7. Corresponds to syslog levels")
args = parser.parse_args()

conf = json.loads(args.conf)

if 'base_url' not in conf:
   print "base_url must be defined."
   parser.print_help()
   exit()

if 'check_name' not in conf:
   conf['check_name'] = 'RX_ERR'

if 'syslog_facility' in conf:
   sslg = True
   #print conf['syslog_facility']
   facility = ''
   for case in switch(conf['syslog_facility']):
      if case('kern'):
         facility = syslog.LOG_KERN
         break
      if case('user'):
         facility = syslog.LOG_USER
         break
      if case('mail'):
         facility = syslog.LOG_MAIL
         break
      if case('daemon'):
         facility = syslog.LOG_DAEMON
         break
      if case('auth'):
         facility = syslog.LOG_AUTH
         break
      if case('lpr'):
         facility = syslog.LOG_LPR
         break
      if case('news'):
         facility = syslog.LOG_NEWS
         break
      if case('uucp'):
         facility = syslog.LOG_UUCP
         break
      if case('cron'):
         facility = syslog.LOG_CRON
         break
      if case('syslog'):
         facility = syslog.LOG_SYSLOG
         break
      if case('local0'):
         facility = syslog.LOG_LOCAL0
         break
      if case('local1'):
         facility = syslog.LOG_LOCAL1
         break
      if case('local2'):
         facility = syslog.LOG_LOCAL2
         break
      if case('local3'):
         facility = syslog.LOG_LOCAL3
         break
      if case('local4'):
         facility = syslog.LOG_LOCAL4
         break
      if case('local5'):
         facility = syslog.LOG_LOCAL5
         break
      if case('local6'):
         facility = syslog.LOG_LOCAL6
         break
      if case('local7'):
         facility = syslog.LOG_LOCAL7
         break
      if case():
         #TODO this should go somewhere
         print "unable to match syslog facility"
         parser.print_help()
         exit()
   syslog.openlog('ToChecks',syslog.LOG_NOWAIT,facility)

to_conn = to(conf['base_url'], token = '91504CE6-8E4A-46B2-9F9F-FE7C15228498')
servers = to_conn.get_servers(False)
#print json.dumps(servers, indent=3, separators=(',', ': '))

tm_conn = tm(to_conn)

# get the current value
to_serverchecks = to_conn.get_serverchecks(False)
#print json.dumps(to_serverchecks, indent=3, separators=(',', ': '))

cache_stats = tm_conn.get_cache_stats(stats="system.proc.net.dev",hc="1")

for cache in cache_stats:
   if_stats = cache_stats[cache]['system.proc.net.dev'][-1]['value'].split()
   if 3 not in if_stats:
      next
   current = int(if_stats[3]) # current rx errors
   if not args.quiet:
      # post current value
      to_conn.post_serverchecks(servers[cache]['id'], cache, 'RX_ERR', current)
   #print cache
   previous = int(to_serverchecks[cache]['checks']['RX_ERR'])

   if args.force == 1:
      current = previous + 1000
   elif args.force == 2:
      current = previous

   #print "previous: "+str(previous)
   #print "current: "+str(current)
   if sslg:
      if current > previous:
         num_errors = current - previous
         syslog.syslog(syslog.LOG_ERR,"hostname="+servers[cache]['fqdn']+" check="+conf['check_name']+" name=\""+conf['name']+"\" result=FAIL status="+servers[cache]['status']+" msg=\"There were "+str(num_errors)+" RX errors\"")
      else:
         syslog.syslog(syslog.LOG_INFO,"hostname="+servers[cache]['fqdn']+" check="+conf['check_name']+" name=\""+conf['name']+"\" result=OK status="+servers[cache]['status']+" msg=\"No RX errors\"")

syslog.closelog()
