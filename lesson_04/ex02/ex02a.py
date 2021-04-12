#!/usr/bin/env python

from netmiko import ConnectHandler
from getpass import getpass

password = getpass()

device = {
    'host': 'cisco3.lasthop.io',
    'device_type': 'cisco_ios',
    'username': 'pyclass',
    'password': password,
    'session_log': 'ex02a_cisco3.log',
    }

command = 'copy flash:testx.txt flash:test-jall.txt'

with ConnectHandler(**device) as conn:
    output = conn.send_command('dir flash:test-jall.txt', expect_string='#', strip_prompt=False, strip_command=False)
    if 'No such file or directory' in output:
        output += conn.send_command(command, expect_string='Destination filename', strip_prompt=False, strip_command=False)
        output += conn.send_command('\n', expect_string='#', strip_prompt=False, strip_command=False)
    else:
        output += conn.send_command(command, expect_string='Destination filename', strip_prompt=False, strip_command=False)
        output += conn.send_command('\n', expect_string='confirm', strip_prompt=False, strip_command=False)
        if 'over write' in output:
            overwrite = input('File already exists. Overwrite (y/n)?')
            output += conn.send_command(overwrite, expect_string='#', strip_prompt=False, strip_command=False)
    print(output)
