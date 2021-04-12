#!/usr/bin/env python

"""
Using threading from Class8, write a Python program that performs SSH auto-detection against the following devices:
cisco3.lasthop.io
cisco4.lasthop.io
nxos1.lasthop.io
nxos2.lasthop.io
vmx1.lasthop.io
vmx2.lasthop.io """

from netmiko import SSHDetect
from getpass import getpass
from concurrent.futures import ThreadPoolExecutor, as_completed

password = getpass()

dev_base = {
    'device_type': 'autodetect',
    'username': 'pyclass',
    'password': password,
    }

devices = [
    'cisco3.lasthop.io',
    'cisco4.lasthop.io',
    'nxos1.lasthop.io',
    'nxos2.lasthop.io',
    'vmx1.lasthop.io',
    'vmx2.lasthop.io'
    ]

max_threads = 5 
all_sessions = list()

future = ThreadPoolExecutor(max_threads)

#import ipdb
#ipdb.set_trace()
for d in devices:
    dev = dev_base.copy()
    dev['host'] = d
    dev['session_log'] = f"ex01a_{d.split('.')[0]}.log"
    session = future.submit(SSHDetect, **dev)
    all_sessions.append(session)

for sess in as_completed(all_sessions):
    dev_type = sess.result().autodetect()
    print(dev_type)


