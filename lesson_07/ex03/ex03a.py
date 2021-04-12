#!/usr/bin/env python
"""
Retry the Netmiko connection attempt, but on the second attempt use the correct password. After the connection is successful use send_command() to retrieve "show ip arp vrf management". Print this ARP output to standard out.
"""

import logging
from netmiko import ConnectHandler
from netmiko import NetmikoAuthenticationException
from netmiko import NetmikoTimeoutException
from getpass import getpass

password = getpass()

logging.basicConfig(
    filename='netmiko_class7.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    )
logger = logging.getLogger(__name__)
logger.error('Send out an error message')
logger.info('Send out an info message')

vmx1 = {
    'host': 'invalid.lasthop.io',
    'device_type': 'juniper_junos',
    'username': 'pyclass',
    'password': password,
    'session_log': 'ex03a_vmx1.log',
    'port': 22,
    }

vmx2 = {
    'host': 'vmx2.lasthop.io',
    'device_type': 'juniper_junos',
    'username': 'pyclass',
    'password': password,
    'session_log': 'ex03a_vmx2.log',
    'port': 8022,
    }

nxos1 = {
    'host': 'nxos1.lasthop.io',
    'device_type': 'cisco_nxos',
    'username': 'pyclass',
    'password': 'invalid',
    'session_log': 'ex03a_nxos1.log',
    'port': 22,
    }

nxos2 = {
    'host': 'nxos2.lasthop.io',
    'device_type': 'cisco_nxos',
    'username': 'pyclass',
    'password': password,
    'session_log': 'ex03a_nxos2.log',
    'port': 22,
    }

devices = (vmx1, vmx2, nxos1, nxos2)

for dev in devices:
    try:
        with ConnectHandler(**dev) as conn:
            output = conn.find_prompt()
    except NetmikoAuthenticationException as error:
        output =f'Authentication failure to {dev.get("host")}' 
    except NetmikoTimeoutException as error:
        if 'DNS' in str(error):
            output = f'DNS invalid host for {dev.get("host")}'
        elif 'port' in str(error):
            output =f'TCP connection failure to {dev.get("host")}' 

    print(output)
