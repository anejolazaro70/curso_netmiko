#!/usr/bin/env python
"""
3. Create a new SSH keyfile using ssh-keygen (leave the passphrase blank):
# Replace "user" below with your username
$ ssh-keygen 
Generating public/private rsa key pair.
Enter file in which to save the key (/home/user/.ssh/id_rsa): /home/user/.ssh/my_ssh_key

Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/user/.ssh/my_ssh_key.
Your public key has been saved in /home/user/.ssh/my_ssh_key.pub.
The key fingerprint is:
SHA256:jDSLE4RmEmGQfW1lYDCHnAn2n8uj8DaHzmz/u+bPvY8 kbyers@pydev1

Next, set up your lab environment such that you can SSH to localhost using the SSH key that you just generated. Make sure that you use the SSH key that you just generated (so that it is unique to you). You can do this by executing the following two commands:
# Change directory into the .ssh directory
# This is located in your home directory.
$ cd ~/.ssh/

# Add your public keyfile into a file named authorized_keys
$ cat my_ssh_key.pub >> authorized_keys
 
# Set the permissions to 600 (read/write only by you)
$ chmod 600 authorized_keys

At this point, you should be able to SSH back into your local system ONLY using the SSH key (i.e. no additional password is required).
$ ssh -i ./my_ssh_key kbyers@localhost
Last login: Tue Feb  2 14:18:37 2021 from localhost

       __|  __|_  )
       _|  (     /   Amazon Linux AMI
      ___|\___|___|

https://aws.amazon.com/amazon-linux-ami/2018.03-release-notes/

$ 

Now that we have a working SSH trust (albeit all on the same system), we are going to set up an SSH config file to SSH proxy through localhost (i.e. through the same server). I recognize this is not real world, but the mechanics of the steps are very similar to proxying through a remote system.

Now let's set up an SSH config file in the lab environment. Your SSH config file should look similar to the following:
$ cat my_ssh_config 
host jumphost
  IdentitiesOnly yes
  IdentityFile ~/.ssh/my_ssh_key  # Use the SSH keyfile you created
  User {{ your_username }}        # replace with your local user name
  HostName server1.lasthop.io     # replace with your lab server name

host * !jumphost
  User pyclass
  # Force usage of this SSH config file
  # Update this line to the proper path to this file
  ProxyCommand ssh -F ~/path/to/my_ssh_config -W %h:%p jumphost   

Now that you have set up an SSH config file and created an SSH trust, let's test using the SSH config file.

Notice, here we are specifying the '-F ./my_ssh_config' which instructs 'ssh' to use that specific SSH config file. Also notice the end device that we are connecting to is 'cisco3.lasthop.io'. The below command should cause you to SSH proxy through localhost. The "password" that is requested is the password for the "cisco3" router.
$ ssh -F ./my_ssh_config cisco3.lasthop.io
Password: 

cisco3#

Now that you have a working SSH proxy configuration (albeit all on the local machine), create a Netmiko program to use this SSH proxy. Your script should connect to the "cisco3" device and print the output of the "show users" command (all why doing an SSH proxy via localhost).
"""

from netmiko import ConnectHandler
from getpass import getpass

cisco3 = {
    'host': 'cisco3.lasthop.io',
    'device_type': 'cisco_ios',
    'username': 'pyclass',
    'password': getpass(),
    'ssh_config_file': '~/.ssh/my_ssh_config',
    'session_log': 'ex03a_cisco3.log',
    }

with ConnectHandler(**cisco3) as conn:
    output = conn.send_command('show users')

print(output)
