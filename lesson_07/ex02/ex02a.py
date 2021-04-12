#!/usr/bin/env python
"""
Retry the Netmiko connection attempt, but on the second attempt use the correct password. After the connection is successful use send_command() to retrieve "show ip arp vrf management". Print this ARP output to standard out.
"""

from netmiko import ConnectHandler
from netmiko import NetmikoAuthenticationException
from netmiko import NetmikoTimeoutException

nxos2 = {
    'host': 'nxos2.lasthop.io',
    'device_type': 'cisco_nxos',
    'username': 'pyclass',
    'password': 'invalid',
    'session_log': 'ex02a_nxos2.log',
    'port': 8022,
    }

try:
    with ConnectHandler(**nxos2) as conn:
        output = conn.send_command('show ip arp vrf management')
except NetmikoAuthenticationException as error:
    output =f'Authentication failure to {nxos2.get("host")}' 
except NetmikoTimeoutException as error:
    output =f'TCP connection failure to {nxos2.get("host")}' 

print(output)
