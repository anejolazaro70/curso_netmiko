#!/usr/bin/env python
"""On Cisco IOS and Cisco IOS-XE devices, you can execute a "show" command and save the result into the local file-system. For example:
show ip int brief | redirect flash:/show_ip_int_brief.txt

This will create a file named "show_ip_int_brief.txt" on the flash file-system that contains the output of the given command.

Using the above "redirect" method, execute "show interfaces" on cisco3 and save the contents to a file on the flash file system. Make sure you properly handle the confirmation prompting if the file already exists. You should ensure your created filename is somehow unique (for example, by adding your initials to the file name).

After you have saved the contents of the file to flash, execute "more flash:/file_name.txt" to verify the file exists and that on a quick verification it looks valid.

Finally, using Netmikos secure copy, retrieve the file you just created from the remote network device.
"""

from netmiko import ConnectHandler, file_transfer
from getpass import getpass

password = getpass()

cisco3 = {
    'host': 'cisco3.lasthop.io',
    'device_type': 'cisco_xe',
    'username': 'pyclass',
    'password': password,
    'session_log': 'ex02a_cisco3.log',
    }

file = 'jall_show_ip_int_brief.txt'
cmd = f'show ip int brief | redirect flash:/{file}'
file_confirm = 'confirm'


with ConnectHandler(**cisco3) as conn:
    output = conn.send_command_expect(cmd, expect_string=file_confirm, strip_command=False, strip_prompt=False )
    cmd = f'more {file}' 
    output = conn.send_command(cmd)
    print(output)
    result = file_transfer(conn, source_file=file, dest_file=file, file_system='flash:', direction='get')
    print(result)
