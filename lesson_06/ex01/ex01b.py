#!/usr/bin/env python
"""
1b. Now add a passphrase to your SSH keyfile (this will cause the SSH key file to be encrypted). In order to do this, execute the following command in the lab environment:
$ ssh-keygen -o -p -f ~/.ssh/student_key
Enter new passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved with the new passphrase.

At this point, if you manually SSH to cisco4 using your SSH key, then you should be prompted for the passphrase.
$ ssh -i ~/.ssh/student_key student1@cisco4.lasthop.io
Enter passphrase for key '/home/kbyers/.ssh/student_key':

cisco4#

Update your Netmiko script such that it properly handles the SSH passphrase. You can accomplish this by adding a "password" argument and setting the value of this argument to the SSH passphrase.

Once again the passphrase is being used to decrypt the local SSH key file (in-memory) and then this SSH key is being used to authenticate to the remote device.
"""
from netmiko import ConnectHandler

cisco3 = {
    'host': 'cisco3.lasthop.io',
    'device_type': 'cisco_ios',
    'username': 'student1',
    'use_keys': True,
    'key_file': '~/.ssh/student_key',
    'password': 'p3peR0',
    'session_log': 'ex01b_cisco3.log',
    }

cisco4 = {
    'host': 'cisco4.lasthop.io',
    'device_type': 'cisco_ios',
    'username': 'student1',
    'password': 'p3peR0',
    'use_keys': True,
    'key_file': '~/.ssh/student_key',
    'session_log': 'ex01b_cisco4.log',
    }

for dev in (cisco3, cisco4):
    with ConnectHandler(**dev) as conn:
       output = conn.send_command('show ip arp')
       print(output)
