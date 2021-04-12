#!/usr/bin/env python

from netmiko import ConnectHandler
from getpass import getpass
from pprint import pprint

password = getpass()

device = {
    'host': 'arista1.lasthop.io',
    'device_type': 'arista_eos',
    'username': 'pyclass',
    'password': password,
    'session_log': 'ex01a_arista1.log'
    }

command = 'show vlan'

with ConnectHandler(**device) as conn:
    output = conn.send_command(command_string=command, use_ttp=True, ttp_template='show_vlan.ttp')

pprint(output)
output = output[0][0]
vlan_7 = [(vlan['vlan_id'], vlan['name']) for vlan in output if vlan['vlan_id']=='7']
print(vlan_7[0])
