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

import sys
import json

class TrafficOps(object):
   """ TrafficOps Class """

   def __init__(self, url, user = '', password = '', token = ''):
      """
      Constructor for the TrafficOps class.
      """

      self.api_version = '1.2'
      # need a try, except for the import of requests
      self.requests = __import__ ('requests')
      self.urljoin=__import__ ('requests').compat.urljoin
      self.requests.packages.urllib3.disable_warnings()
      self.s = self.requests.Session()
      self.url = url
      self.s.verify=False
      self.s.timeout=5
      __headers={"Content-Type": "application/x-www-form-urlencoded"}

      if password and (password != ''):
         #print "password matched"
         __data={"u": user, "p": password}
         try:
            r = self.s.post(url + '/login',data=__data,headers=__headers)
            #print r.text
         except self.requests.exceptions.RequestException as e:
            print e
            sys.exit(1)
      else:
         #print "trying token"
         __data={"t": token}
         try:
            r = self.s.post(url + '/api/' + self.api_version + '/user/login/token', data=json.dumps(__data), headers=__headers)
            #print r.headers
            #print r.text
         except self.requests.exceptions.RequestException as e:
            print e
            sys.exit(1)
        
      self.cookie={"Cookie": r.headers['set-cookie']}
      self.s.headers.update(self.cookie)
   
   def get(self,url):
      try:
         return self.s.get(url)
      except requests.exceptions.RequestException as e:
         print e
         sys.exit(1)

   # Servers
   def get_servers(self, raw=False):
      """
      Retrieves a list of servers in JSON format as a list
      """
      __servers = {}
      __url = self.urljoin(self.url,"/api/" + self.api_version + "/servers.json")
      r = self.get(__url)
      if raw:
         __servers = r.json()
      else:
         for i in r.json()['response']:
            __servers[i['hostName']] = i
            __servers[i['hostName']]['fqdn'] = i['hostName'] + "." + i['domainName']
      #return r.json()['response']
      return __servers

   def get_server(self,name):
     """
     Retrieves a single server
     """
     __url = self.urljoin(self.url,"/api/" + self.api_version + "/servers/hostname/" + name + "/details.json")
     r = self.get(__url)
     __server = r.json()
     return __server

   # Cache Groups
   def get_cachegroups(self, raw=False):
     """
     Retrieves a list of cache groups in JSON format as a list
     """
     __cg = {}
     __url = self.urljoin(self.url,"/api/" + self.api_version + "/cachegroups.json")
     r = self.get(__url)
     if raw:
        __cg = r.json()
     else:
        for i in r.json()['response']:
         __cg[i['name']] = i
     #return r.json()['response']
     return __cg
   
   # Federations
   def get_federations(self):
      """
      Retrieves a list of federations
      """
      __url = self.urljoin(self.url,"/api/" + self.api_version + "/federations.json")
      r = self.get(__url)
      return r.json()['response']
   
   def put_federations(self,data):
      """
      Overwrites all federations from JSON input
      """
      __url = self.urljoin(self.url,"/api/" + self.api_version + "/federations.json")
      r = self.s.put(__url, data=data)
   
   def config_files(self, hostname):
      __url = self.urljoin(self.url,"/ort/" + hostname + "/ort1")
      r = self.get(__url)

   # TO extenstions
   def get_to_extensions(self):
      """
      Retrieves a JSON formatted list of extensions
      """
      __url = self.urljoin(self.url,"/api/" + self.api_version + "/to_extensions.json")
      r = self.get(__url)
      #return r.json()['response']
      return r.json()

   def add_to_extension(self, name, script_ver, info_url, script_file, isactive, additional_config, description, servercheck_short_name, script_type):
      """
      Adds TO extension
      """
      __data = {'name': name,
              'version': script_ver,
              'info_url': info_url,
              'script_file': script_file,
              'isactive': isactive,
              'additional_config_json': additional_config,
              'description': description,
              'servercheck_short_name': servercheck_short_name,
              'type': script_type}

      #print json.dumps(__data)
      #data = json.dumps(data)

      __url = self.urljoin(self.url,"/api/" + self.api_version + "/to_extensions")
      r = self.s.post(__url, data = json.dumps(__data))

      print r.headers
      print r.text

      #return r.json()['response']
      return 1

   # Serverchecks
   def get_serverchecks(self,raw=False):
      """
      Retrieves a JSON formatted list of the server checks
      """
      __serverchecks = {}
      __url = self.urljoin(self.url,"/api/" + self.api_version + "/servers/checks.json")
      r = self.get(__url)
      if raw:
         #print r.json()['response']
         return r.json()['response']
      else:
         for i in r.json()['response']:
            __serverchecks[i['hostName']] = i

         return __serverchecks

   def post_serverchecks(self, server_id, hostname, check_name, value):
      """
      Post an update to server checks
      """
      __data = {'id': server_id,
                'hostname': hostname,
                'servercheck_short_name': check_name,
                'value': value}

      __url = self.urljoin(self.url,"/api/" + self.api_version + "/servercheck")
      r = self.s.post(__url, data = json.dumps(__data))
      return r.text

   # Delivery Services
   def get_deliveryservices(self):
      """
      Retrieves a JSON formatted list of Delivery Services
      """
      __url = self.urljoin(self.url,"/api/" + self.api_version + "/deliveryservices.json")
      r = self.get(__url)
      return r.json()['response']

   def get_profiles(self):
      """
      Retrieves a JSON formatted list of Profiles and return a list
      """
      data = []
      url = self.urljoin(self.url,"/api/" + self.api_version + "/profiles/trimmed.json")
      profiles = self.get(url)

      if not profiles:
        return data

      for profile in profiles.json():    
        data.append(profile['name'])

      return data

   def get_profile_parameters(self, profile=None, raw=False, include_config_filter=None, include_name_filter=None):
     """
     Retrieve profile parameters and return value
     Filtering: If you are filtering, you need to at least specify a list of keywords in include_config_filter.
     """
     data = []
     if profile == None:
       url = self.urljoin(self.url,"/api/" + self.api_version + "/parameters.json")
     else:
       url = self.urljoin(self.url,"/api/" + self.api_version + "/parameters/profile/" + profile + ".json")
     r = self.get(url)

     if not r:
       return data
  
     return r.json()['response']
              

