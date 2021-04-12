#!/usr/bin/env python

from netmiko import ConnectHandler
from getpass import getpass
from datetime import datetime

password = getpass()

device = {
    'host': 'cisco3.lasthop.io',
    'device_type': 'cisco_ios',
    'username': 'pyclass',
    'password': password,
    'session_log': 'ex03a_cisco3.log',
    'fast_cli': True,
    }

before = datetime.now()

with ConnectHandler(**device) as conn:
    output = conn.find_prompt()
    print(output)

after = datetime.now()

print(f'Total executed time: {after - before}')
