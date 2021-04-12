#!/usr/bin/env python

from netmiko import ConnectHandler
from getpass import getpass

password = getpass()


command = 'show ip arp'

for i in range(1,5):
    host = f'arista{i}.lasthop.io'
    device = {
        'username': 'pyclass',
        'password': password,
        'device_type': 'arista_eos',
        'session_log': f'ex01a_arista{i}.log'
        }

    with ConnectHandler(**device, host=host) as dev_con:
        print(dev_con.find_prompt())
        output = dev_con.send_command(command)
        print(output)
