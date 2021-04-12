#!/usr/bin/env python

"""
Establish a normal Netmiko SSH connection to cisco3.lasthop.io. Inside this Netmiko SSH connection use write_channel() to execute "telnet 10.220.88.22\n" (this command is actually creating a telnet connection back to "cisco3" itself). Once again using only write_channel() and read_channel(), handle the username and password prompting such that you successfully login to this telnet connection. Your interaction with the device should be similar to the following:

cisco3#telnet 10.220.88.22
Trying 10.220.88.22 ... Open

User Access Verification

Username: pyclass
Password: 

cisco3#

After you have completely logged in, use write_channel to send "exit\n" to logout of the inner telnet connection. At this point you can disconnect normally from the device using Netmiko. Print sufficient information to standard output such that you can verify the inner telnet connection worked properly.
"""

from netmiko import ConnectHandler
from getpass import getpass
import time

cisco3 = {
    'host': 'cisco3.lasthop.io',
    'device_type': 'cisco_xe',
    'username': 'pyclass',
    'password': getpass(),
    'session_log': 'ex03a_cisco3.log',
    }

with ConnectHandler(**cisco3) as conn:
    cmd = 'telnet 10.220.88.22\n'
    #import ipdb; ipdb.set_trace()
    output = conn.write_channel(cmd)
    time.sleep(1)
    output = conn.read_channel()
    print(output)
    conn.write_channel(f'{cisco3["username"]}\n')
    time.sleep(1)
    output = conn.read_channel()
    print(output)
    conn.write_channel(f'{cisco3["password"]}\n')
    time.sleep(1)
    output = conn.read_channel()
    print(output)
    conn.write_channel('exit\n')
    time.sleep(1)
    output = conn.read_channel()
    print(output)
     
