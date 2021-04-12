#!/usr/bin/env python
"""
1a. Authenticate to the cisco3 and cisco4 IOS-XE devices, using the SSH key-file located at "~/.ssh/student_key". Print out "show ip arp" from each of those devices. The "student1" username is the user on the Cisco devices that is associated with that SSH key.

Note, you can verify that the SSH key is working properly by SSHing to one of the devices as follows:
$ ssh -i ~/.ssh/student_key student1@cisco4.lasthop.io

cisco4#

No password is required for this authentication.
"""
from netmiko import ConnectHandler

cisco3 = {
    'host': 'cisco3.lasthop.io',
    'device_type': 'cisco_ios',
    'username': 'student1',
    'use_keys': True,
    'key_file': '~/.ssh/student_key',
    'session_log': 'ex01a_cisco3.log',
    }

cisco4 = {
    'host': 'cisco4.lasthop.io',
    'device_type': 'cisco_ios',
    'username': 'student1',
    'use_keys': True,
    'key_file': '~/.ssh/student_key',
    'session_log': 'ex01a_cisco4.log',
    }

for dev in (cisco3, cisco4):
    with ConnectHandler(**dev) as conn:
       output = conn.send_command('show ip arp')
       print(output)
