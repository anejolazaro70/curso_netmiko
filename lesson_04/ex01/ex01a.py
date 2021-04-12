#!/usr/bin/env python

from netmiko import ConnectHandler
from getpass import getpass

password = getpass()

device = {
    'host': 'cisco3.lasthop.io',
    'device_type': 'cisco_ios',
    'username': 'pyclass',
    'password': password,
    'session_log': 'ex01a_cisco3.log',
    }

command = 'copy flash:testx.txt flash:test-jall.txt'

with ConnectHandler(**device) as conn:
    output = conn.send_command_timing(command, strip_prompt=False, strip_command=False)
    output += conn.send_command_timing('\n', strip_prompt=False, strip_command=False)
    if 'over write' in output:
        overwrite = input('File already exists. Overwrite (y/n)?')
        output += conn.send_command_timing(overwrite, strip_prompt=False, strip_command=False)
    print(output)
    output = conn.send_command_timing('dir flash:test-jall.txt')
    print(output)
