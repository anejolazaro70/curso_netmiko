#!/usr/bin/env python

from netmiko import ConnectHandler
from getpass import getpass
from datetime import datetime

password = getpass()

device = {
    'host': 'cisco4.lasthop.io',
    'device_type': 'cisco_ios',
    'username': 'pyclass',
    'password': password,
    'session_log': 'ex04a_cisco4.log',
    'fast_cli': False,
    }

command = 'show run'

before = datetime.now()

with ConnectHandler(**device) as conn:
    output = conn.send_command(command, delay_factor=5, max_loops=1000)
    print(output)

after = datetime.now()

print(f'Total executed time: {after - before}')
