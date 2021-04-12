#!/usr/bin/env python

from netmiko import ConnectHandler
from netmiko import NetmikoTimeoutException
from getpass import getpass

password = getpass()

devices = [
    {'host': 'nxos1.lasthop.io',
     'device_type': 'cisco_nxos',
     'username': 'pyclass',
     'password': password,
     'session_log': 'ex03d_nxos1.log',
    },
]

config = ['terminal width 80', 'hostname verylonghostnamefornxos']
command = ' show ip interface brief vrf management | include management'

config_after = 'hostname nxos1'

for dev in devices:
    conn = ConnectHandler(**dev)
    output = conn.find_prompt()
    conn.global_cmd_verify = False
    if output != 'verylonghostnamefornxos#':
        output = conn.send_config_set(config)
        print(output)
    try:
        output = conn.send_command_timing(command)
    except NetmikoTimeoutException:
        print('... long command failed with an exception')
    finally:
        output = conn.send_config_set(config_after)
        conn.disconnect()
