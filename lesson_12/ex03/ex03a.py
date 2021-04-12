#!/usr/bin/env python

"""
On vmx1, use send_config_set() to configure the following two items:
    cfg_commands = [ 
        "set system syslog archive size 110k files 3",
        "set system time-zone America/New_York",
    ]   

Commit the change on vmx1 using the commit() method. Add a comment to your commit; the comment should indicate that the commit was performed using Netmiko and also include your initials.

After the commit is completed, use send_command() to execute "show system commit". This command will show you the commit history. Extract the most recent commit including its associated comment.

Print out this last commit and comment.  Hopefully, this is your commit and your comment.
"""

from netmiko import ConnectHandler
from getpass import getpass
from datetime import datetime
from time import sleep

password = getpass()

vmx1 = {
    'host': 'vmx1.lasthop.io',
    'device_type': 'juniper_junos',
    'username': 'pyclass',
    'password': password,
    'session_log': 'ex03a_vmx1.log',
    }

cfg_commands = [ 
        "set system syslog archive size 110k files 3",
        "set system time-zone America/New_York",
    ]

t0 = datetime.now()

try:
    with ConnectHandler(**vmx1) as conn:
        conn.send_config_set(cfg_commands)
        output = conn.commit(comment='commit done by jall using netmiko')
        print(output)
        import ipdb; ipdb.set_trace()
        output = conn.send_command('show system commit')
        output = output.strip()
        output = output.splitlines()
        print(output)
except Exception as error:
    print(str(error))

t1 = datetime.now()

print(f'Elapsed time={t1 - t0}') 

