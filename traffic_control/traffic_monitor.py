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

import sys
import json

# TODO add raw param to return exactly what is returned from the API
# TODO make the convert to dict a function. the API retuns a list and I'm
#    converting to dict. make this a public function

class TrafficMonitor(object):
   """ TrafficMonitor Class """

   def __init__(self, to, raw=False):
      """
      Constructor for the TrafficMonitor class.
      """

      self.requests=__import__ ('requests')
      self.urljoin=__import__ ('requests').compat.urljoin
      self.s=self.requests.Session()
      self.servers = {}

      tmp = to.get_servers(False)
      # print json.dumps(tmp, indent=3, separators=(',', ': '))
      for i in tmp:
         if (tmp[i]['type'] == 'RASCAL'):
            self.servers[i] = tmp[i]
            self.servers[i]['url'] = "http://" + i + "." + self.servers[i]['domainName']
            self.servers[i]['fqdn'] = i + "." + self.servers[i]['domainName']

      print json.dumps(self.servers, indent=3, separators=(',', ': '))
   
   def get_cache_stats(self, tm='', hc='', stats='', wildcard='', cache=''):
      """
      /publish/CacheStats

      Statistics gathered for each cache.
      
      Parameter   Type        Description
      tm          string      Optional. Hostname (not FQDN) of one of the Traffic Monitor servers. If not specified will try each 'ONLINE' until recieves a response.
      hc          int         The history count, number of items to display.
      stats 	   string      A comma separated list of stats to display (without spaces).
      wildcard    boolean     Controls whether specified stats should be treated as partial strings.
      cache       string      optional hostname (not FQDN) of the cache to get stats for.
      """

      __url = ''
      __query = ''
      __path = "/publish/CacheStats"

      # add the cache to the path if defined
      if cache != '':
         __path = __path + "/" + cache

      # build the query
      if hc != '':
         __query = "?hc=" + str(hc)

      if wildcard != '':
         if __query != '':
            __query = __query + "&wildcard=" + wildcard
         else:
            __query = "?wildcard=" + wildcard 

      if stats != '':
         if __query != '':
            __query = __query + "&stats=" + stats
         else:
            __query = "?stats=" + stats

      # append the query if needed
      #if __query != '':
      #   __url = self.urljoin(__url,__query)

      for i in self.servers:
         if (tm != '') and (tm == i):
            __query = self.urljoin(self.servers[i][url],__path + __query)
            break
         else:
            if self.servers[i]['status'] == "ONLINE":
               #print "found online cache: " + self.servers[i]['hostName']
               __url = self.urljoin(self.servers[i]['url'], __path + __query)
               break
               
      #print __url
      r = self.s.get(__url)
      return r.json()['caches']

