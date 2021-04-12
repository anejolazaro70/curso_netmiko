#!/usr/bin/env python

"""
Connect to the "cisco4" device.

Change the device's hostname to "cisco4-testing" except do not use send_config_set() instead use config_mode(), write_channel(), and exit_config_mode() to accomplish this.

Use the find_prompt() method to print the prompt before going into config mode, when in config mode, and after you have exited configuration mode.
"""

from netmiko import ConnectHandler
from getpass import getpass
from datetime import datetime
from time import sleep

password = getpass()

cisco4 = {
    'host': 'cisco4.lasthop.io',
    'device_type': 'cisco_xe',
    'username': 'pyclass',
    'password': password,
    'session_log': 'ex02a_cisco4.log',
    }

t0 = datetime.now()

try:
    with ConnectHandler(**cisco4) as conn:
        output = conn.find_prompt()
        print(output)
        output = conn.config_mode()
        print(output)
        conn.write_channel('hostname cisco4')
        sleep(1)
        output = conn.read_channel()
        print(output)
        output = conn.exit_config_mode()
        print(output)
        output = conn.find_prompt()
        print(output)
except Exception as error:
    print(str(error))

t1 = datetime.now()

print(f'Elapsed time={t1 - t0}') 

