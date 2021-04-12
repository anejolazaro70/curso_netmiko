#!/usr/bin/env python

from netmiko import ConnectHandler
from getpass import getpass

password = getpass()

config = ['ip domain-lookup', 'ip domain-name bogus.com']

devices = [
    {'host': 'nxos1.lasthop.io',
     'device_type': 'cisco_nxos',
     'username': 'pyclass',
     'password': password,
     'session_log': 'ex01a_nxos1.log',
    },
    {'host': 'nxos2.lasthop.io',
     'device_type': 'cisco_nxos',
     'username': 'pyclass',
     'password': password,
     'session_log': 'ex01a_nxos2.log',
    }
]

for dev in devices:
    with ConnectHandler(**dev) as conn:
        output = conn.send_config_set(config)
        print(output)
