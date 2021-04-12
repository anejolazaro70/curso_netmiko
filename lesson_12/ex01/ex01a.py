#!/usr/bin/env python

"""
Create a Netmiko script that connects to "nxos2".

In this script, use "send_command" to send a command that will fail. For example, you can send "conf t" as this will cause the terminating prompt to change.

In your script measure how long it takes "send_command" to execute both with fast_cli=False and with fast_cli=True.

You can use a pattern similar to the following to measure this time:
from datetime import datetime

try:
    # Command that send_command will fail on
    start_time = datetime.now()
    output = net_connect.send_command("conf t")
finally:
    end_time = datetime.now()

Note, since send_command will fail above, the "end_time" needs wrapped in a try/except or a try/finally statement.

How long does send_command take to fail when fast_cli=True? How long does send_command take to fail when fast_cli=False?

"""

from netmiko import ConnectHandler
from getpass import getpass
from datetime import datetime

password = getpass()

nxos2 = {
    'host': 'nxos2.lasthop.io',
    'device_type': 'cisco_nxos',
    'username': 'pyclass',
    'password': password,
    'fast_cli': False,
    'session_log': 'ex01b_nxo2.log',
    }

t0 = datetime.now()

try:
    with ConnectHandler(**nxos2) as conn:
        conn.send_command('conf t')
except Exception as error:
    print(str(error))

t1 = datetime.now()

print(f'Elapsed time={t1 - t0}, with fast_cli={conn.fast_cli}') 

