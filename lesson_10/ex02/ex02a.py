#!/usr/bin/env python

"""
Repeat exercise1, except read all of the hostnames in from an external file named "my_hosts.txt". This file should look similar to the following:
$ cat my_hosts.txt 
cisco3.lasthop.io
cisco4.lasthop.io
nxos1.lasthop.io
nxos2.lasthop.io
vmx1.lasthop.io
vmx2.lasthop.io 

After you have discovered the device_type for each device programmatically create a YAML output file that contains an entry similar to the following for all six of the hosts.
cisco3:
  device_type: cisco_ios
  hostname: cisco3.lasthop.io
"""

from netmiko import SSHDetect
from getpass import getpass
from concurrent.futures import ThreadPoolExecutor, as_completed
from yaml import dump

password = getpass()

dev_base = {
    'device_type': 'autodetect',
    'username': 'pyclass',
    'password': password,
    }

with open('my_hosts.txt', 'r') as fh:
    devs = fh.readlines()
    devices = [d.strip() for d in devs]

max_threads = 5 
all_sessions = list()
all_devs = dict()

future = ThreadPoolExecutor(max_threads)

for d in devices:
    dev = dev_base.copy()
    dev['host'] = d
    dev['session_log'] = f"ex01a_{d.split('.')[0]}.log"
    session = future.submit(SSHDetect, **dev)
    all_sessions.append(session)
    host = d.split('.')[0]
    all_devs[host] = dict()
    all_devs[host]['device_type'] = session
    all_devs[host]['hostname'] = d

for sess in as_completed(all_sessions):
    for host, values in all_devs.items():
        if values['device_type'] == sess:
            values['device_type'] =  sess.result().autodetect()
            print(host)
            break

with open('my_hosts.yaml', 'w') as fh:
    output = dump(all_devs, fh)
