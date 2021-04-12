#!/usr/bin/env python

from netmiko import ConnectHandler
from getpass import getpass
import logging

logging.basicConfig(filename='test_ex02b.log', level=logging.DEBUG)
logger = logging.getLogger('netmiko')

password = getpass()


command = 'disable'

device = {
    'host': 'cisco3.lasthop.io',
    'username': 'pyclass',
    'password': password,
    'device_type': 'cisco_ios',
    'session_log': 'ex02b.log',
    }

with ConnectHandler(**device) as dev_con:
    print(dev_con.find_prompt())
    output = dev_con.send_command(command, expect_string=r'>')
    print(dev_con.find_prompt())
