#!/usr/bin/env python
"""
2. Now that your SSH key file is encrypted, set up an SSH agent such that your passphrase is remembered once you have entered it.

Start the 'ssh-agent' as follows (note, the ssh-agent command below is wrapped in backticks, not quotes). This basically starts the ssh-agent and sets some environment variables related to the SSH agent.
$ eval `ssh-agent`
Agent pid 31383

Next you need to add the "student_key" into the SSH agent and provide the key's passphrase (so the SSH agent can access the key and decrypt it).
$ ssh-add ~/.ssh/student_key
Enter passphrase for /home/kbyers/.ssh/student_key: 
Identity added: /home/kbyers/.ssh/student_key (/home/kbyers/.ssh/student_key)

Now you can test that the SSH agent is working properly. You can do this by SSHing into "cisco4" using the "student_key" (at this point, you should NOT be prompted for a passphrase).
$ ssh -i ~/.ssh/student_key student1@cisco4.lasthop.io

cisco4#

Now update your Netmiko code from exercise 1b. Your updated Netmiko code should use the SSH agent (i.e. set use_agent=True). You should NOT need to provide the SSH passphrase in your Netmiko code.
"""
from netmiko import ConnectHandler

cisco3 = {
    'host': 'cisco3.lasthop.io',
    'device_type': 'cisco_ios',
    'username': 'student1',
    'use_keys': True,
    'key_file': '~/.ssh/student_key',
    'allow_agent': True,
    'session_log': 'ex02a_cisco3.log',
    }

cisco4 = {
    'host': 'cisco4.lasthop.io',
    'device_type': 'cisco_ios',
    'username': 'student1',
    'allow_agent': True,
    'use_keys': True,
    'key_file': '~/.ssh/student_key',
    'session_log': 'ex02a_cisco4.log',
    }

for dev in (cisco3, cisco4):
    with ConnectHandler(**dev) as conn:
       output = conn.send_command('show ip arp')
       print(output)
