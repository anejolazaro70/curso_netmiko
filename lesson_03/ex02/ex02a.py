#!/usr/bin/env python

from netmiko import ConnectHandler
from getpass import getpass
from pprint import pprint

password = getpass()

device = {
    'host': 'nxos1.lasthop.io',
    'device_type': 'cisco_nxos',
    'username': 'pyclass',
    'password': password,
    'session_log': 'ex02a_nxos1.log'
    }

command = 'show lldp neighbors detail'

with ConnectHandler(**device) as conn:
    output = conn.send_command(command_string=command, use_genie=True)

output = output['interfaces']
for itf, data in output.items():
    pprint(f'Local Intf: {itf}')
    print('__________________________')
    data = data['port_id'][itf]['neighbors']
    for nb, nb_data in data.items():
        print(f'Neighbor: {nb}')
        print(f'Remote port: {nb_data["port_description"]}')
        print(f'MGMT IP: {nb_data["management_address_v4"]}')
        # print(data.values())
        print('__________________________\n')
# pprint(output)
# pprint(local_if, remote_name, remote_if, mgmt_ip)
