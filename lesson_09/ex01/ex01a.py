#!/usr/bin/env python

"""Create a text file that contains the following configuration commands:
no ip name-server 1.1.1.1
no ip name-server 1.0.0.1
ip name-server 8.8.8.8
ip name-server 8.8.4.4
ip domain name lasthop.io

Construct a Netmiko script that uses secure copy to transfer the above text file to both Cisco3 and Cisco4. After the file has been transferred to the remote device, merge the above configuration file into the device's running-config.

The syntax of this command is:
# Replace "your_file_name.txt" with the actual name of your file
copy flash:/your_file_name.txt system:running-config

Note, this command will prompt you to verify the destination filename so you will need to properly handle this prompting.

Also, note, depending on the current configuration of the device, the "ip name-server 1.1.1.1" and the "ip name-server 1.0.0.1" commands may or may not exist in the current running-config. If these commands don't exist in the configuration, then you will receive an error similar to the following: "%Error: Removing name-server 1.1.1.1" (when you try to remove the given name-server). It is fine if this happens, the rest of your configuration commands will still be properly loaded.

After you have merged your configuration into the running-config, verify that the name-servers and the domain-name are now correct. Your end running-configuration should contain the following lines:
ip domain name lasthop.io
# The order of name-servers might vary
ip name-server 8.8.4.4 8.8.8.8
"""

from netmiko import ConnectHandler, file_transfer
from getpass import getpass
from yaml import load
from ipdb import set_trace

password = getpass()

def load_inventory(filename=None):
    with open(filename, 'r') as fh:
        inventory = load(fh)
    return inventory

def transfer_file(conn=None, device=None, src_f=None, dst_f=None, fs=None, act=None):
    result = file_transfer(conn, source_file=src_f, dest_file=dst_f, file_system=fs, direction=act)

    print(f'\n\nResult of transfer file {src_f} to {device}')
    print(50*'=')
    print(f'{result}')
    print(50*'=')
    print('\n')

    return result

def main():
    inventory = 'inventory.yaml'
    src_f = 'ex01a_ns_config.txt'
    dst_f = 'jall_ns_config.txt'
    fs = 'flash:'
    act = 'put'

    devices = load_inventory(inventory)
    for dev in devices.values():
        dev['password'] = password
        device = dev['host']
        with ConnectHandler(**dev) as conn:
            transfer_r = transfer_file(conn, device, src_f =src_f, dst_f=dst_f, fs=fs, act=act)
            f_exist = transfer_r['file_exists']
            f_md5 = transfer_r['file_verified']
            if f_exist and f_md5:
                cmd = f'copy {fs}/{dst_f} system:running-config'
                output = conn.send_command_expect(cmd, expect_string='running-config', strip_prompt=False, strip_command=False)
                cmd = '\n'    
                output = conn.send_command(cmd)
                print(output)
            cmd = 'show running-config | include ip domain name' 
            expected_str = 'ip domain name lasthop.io'
            output = conn.send_command(cmd, strip_prompt=False, strip_command=False)
            if expected_str in output:
                print(f'Domain name correctly configured in {device}')
            #set_trace()            
            cmd = 'show running-config | include ip name-server'
            ns1 = '8.8.4.4'
            ns2 = '8.8.8.8'
            output = conn.send_command(cmd)

            if len(output.split()) != 4:
                print('More or less servers configured')
            if ns1 in output or ns2 in output:
                print(f'Domain servers correctly configured in {device}')


if __name__ == '__main__':
    main()
