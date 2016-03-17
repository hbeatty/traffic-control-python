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

import socket
import sys

class TrafficOps(object):
   def __init__(self, url, user, password):
      self.api_version = '1.2'
      # need a try, except for the import of requests
      self.requests=__import__ ('requests')
      self.urljoin=__import__ ('requests').compat.urljoin
      self.requests.packages.urllib3.disable_warnings()
      self.s=self.requests.Session()
      self.url=url
      self.s.verify=False
      self.s.timeout=5
      __data={"u": user, "p": password}
      __headers={"Content-Type": "application/x-www-form-urlencoded"}
      try:
         r = self.s.post(url + '/login',data=__data,headers=__headers)
      except self.requests.exceptions.RequestException as e:
         print e
         sys.exit(1)
        
      self.cookie={"Cookie": r.headers['set-cookie']}
      self.s.headers.update(self.cookie)
   
   def servers(self):
      __url = self.urljoin(self.url,"/api/" + self.api_version + "/servers.json")
      r = self.get(__url)
      return r.json()['response']
   
   def get(self,url):
      try:
         return self.s.get(url)
      except requests.exceptions.RequestException as e:
         print e
         sys.exit(1)
   
   def get_federations(self):
      __url = self.urljoin(self.url,"/api/" + self.api_version + "/federations.json")
      r = self.get(__url)
      return r.json()['response']
   
   def put_federations(self,data):
      __url = self.urljoin(self.url,"/api/" + self.api_version + "/federations.json")
      r = self.s.put(__url, data=data)
   
   def config_files(self, hostname):
      __url = self.urljoin(self.url,"/ort/" + hostname + "/ort1")
      r = self.get(__url)
