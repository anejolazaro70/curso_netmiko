#!/usr/bin/env python

"""
In this exercise, we are going to artificially recreate a terminal server. We will do this by "bouncing" through a Cisco IOS device. At a high-level the process will be:
      * Connect to cisco3.lasthop.io using a standard Netmiko SSH connection,
      * From "cisco3" use Netmiko to execute "ssh -l pyclass 10.220.88.31" (10.220.88.31 is the internal IP address for "arista4"),
      * Handle the password prompting and successfully login to the "arista4" device,
      * Use redispatch to properly change the class to the Arista EOS class.

Write a Netmiko program that properly accomplishes these items.
"""

from netmiko import ConnectHandler, redispatch
from getpass import getpass
from time import sleep

password = getpass()

cisco3 = {
    'host': 'cisco3.lasthop.io',
    'device_type': 'cisco_xe',
    'username': 'pyclass',
    'password': password,
    'session_log': 'ex01c_cisco3.log',
    }

with ConnectHandler(**cisco3) as conn:
    output = conn.find_prompt()
    if 'cisco3#' in output:
        print(type(conn))
        pass
    else:
        print(f'not connected to {conn.host.split(".")[0]}')
        raise ValueError
    cmd = 'ssh -l pyclass 10.220.88.31'
    output = conn.send_command(cmd, expect_string='assword:')
#    import ipdb;ipdb.set_trace()
    if 'assword' in output:
        conn.write_channel(f'{password}\r')
        sleep(1)
        output = conn.read_channel()

    if 'arista4#' in output:
        print(type(conn))
        pass
    else:
        print('not connected to arista4')
        raise ValueError
    redispatch(conn, device_type='arista_eos')
    output = conn.send_command('show version')
    print(output)
    print(type(conn))
    import ipdb;ipdb.set_trace()
    conn.write_channel('exit\r')
    sleep(1)
    output = conn.read_channel()
    print(output)
    redispatch(conn, device_type='cisco_xe')
    output = conn.find_prompt()
    if 'cisco3#' in output:
        print(type(conn))
        print('connected to cisco3#')
    else:
        print('not connected to cisco3#')
        raise ValueError
