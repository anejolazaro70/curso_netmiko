#!/usr/bin/env python

from netmiko import ConnectHandler
from getpass import getpass
import logging

logging.basicConfig(filename='test.log', level=logging.DEBUG)
logger = logging.getLogger('netmiko')

password = getpass()


command = 'disable'
dev_list = ['cisco3.lasthop.io', 'cisco4.lasthop.io']

device = {
    'username': 'pyclass',
    'password': password,
    'device_type': 'cisco_ios',
    }

for host in dev_list:
    session_log = f'{host}.log'
    with ConnectHandler(**device, host=host, session_log=session_log) as dev_con:
        print(dev_con.find_prompt())
        output = dev_con.send_command_timing(command)
        print(dev_con.find_prompt())
