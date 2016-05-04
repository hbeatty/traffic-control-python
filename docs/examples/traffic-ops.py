#!/usr/bin/env python
"""
@copyright: 2016
@author: Steve Malenfant http://github.com/smalenfant
@author: Hank Beatty http://github.com/hbeatty
@organization: Cox Communications Inc. - Advanced Network Platforms
@license: Apache-2.0
"""
# -*- coding: utf-8 -*-
#
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

######################################################################

#usage: traffic-ops.py [--list] [--host HOST]

from __future__ import print_function

import os
import sys
import argparse
import string

try:
    import json
except:
    import simplejson as json


try:
    from traffic_control import TrafficOps

except ImportError:
    print("Error: Traffic Control library must be installed: pip install traffic-control.",
          file=sys.stderr)
    sys.exit(1)


class TrafficOpsInventory(object):
    def __init__(self):

        parser = argparse.ArgumentParser()
        parser.add_argument('--host')
        parser.add_argument('--list', action='store_true')

        options = parser.parse_args()
        try:
            self.to = TrafficOps('https://cms.kabletown.net', user='chs', password='w@term@rk')
        except:
            print("Error: Could not connect to Traffic Ops API", file=sys.stderr)

        if options.host:
            data = self.get_host(options.host)
            #print(json.dumps(data, indent=3))

        elif options.list:
            data = self.get_list()
            print(json.dumps(data, indent=3))
        else:
            print("usage: --list | --host <hostname>",
                  file=sys.stderr)
            sys.exit(1)

    def get_host(self, name):
        host = self.to.get_server(name)
        data = {}
        if not host:
            return data
        if 'cachegroup' in host:
            data['group'] = host['cachegroup']
        for k, v in host.iteritems():
            data[k] = host[k]
        return data

    def get_list(self):
        profiles = []
        data = {
            '_meta': {
                'hostvars': {},
            },
        }

        hosts = self.to.get_servers()
        if not hosts:
            return data

        for host in hosts['response']:
            fqdn = host['hostName']+"."+host['domainName']

            # check to see if the type (edge, mid, chs, crs, etc) exists
            if host['type'] not in data:
                data[host['type']] = {}
                data[host['type']]['children'] = []

            # check to see if the cachegroup is already in the type
            if host['cachegroup'] not in data[host['type']]['children']:
                data[host['type']]['children'].append(host['cachegroup'])

            # check to see if the cachegroup (a.k.a. Ansible group) exits
            if host['cachegroup'] not in data:
                data[host['cachegroup']] = {}
                data[host['cachegroup']]['hosts'] = []

            # add this host to the cachegroup (a.k.a. Ansible group)
            if fqdn not in data[host['cachegroup']]['hosts']:
                data[host['cachegroup']]['hosts'].append(fqdn)

            # add this host's vars to _meta
            data['_meta']['hostvars'][fqdn] = host

            ### EXPERIMENTAL ###
            #if 'profile' in host:
            #    if host['profile'] not in profiles:
            #        profiles.append(host['profile'])
            ### END 



        ### EXPERIMENTAL ###
        #profiles = self.to.get_profiles()
        #config_filter = ['grub.conf','kickstart']
        #
        #for profile in profiles:
        #    #print (profile)
        #    data['_meta']['profiles'][profile] = {}
        #    params = self.to.get_profile_parameters(profile=profile)
        #    for p in params:
        #        if p['configFile'] in config_filter:
        #            if 'grub.conf' in p['configFile'] and 'ramdisk_size' in p['name']:
        #                data['_meta']['profiles'][profile]['ramdisk_size'] = string.split(p['value'], '=')[1]
        #            elif 'kickstart' in p['configFile'] and 'ondisk' in p['name']:
        #                data['_meta']['profiles'][profile]['ondisk'] = p['value']
        ### END EXPERIMENTAL ###

        return data

if __name__ == '__main__':
    TrafficOpsInventory()

