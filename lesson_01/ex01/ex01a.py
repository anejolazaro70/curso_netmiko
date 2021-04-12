#!/usr/bin/env python
from netmiko import ConnectHandler
from getpass import getpass

password = getpass()

conn = ConnectHandler(
    host="nxos1.lasthop.io",
    username="pyclass",
    password=password,
    device_type="cisco_nxos",
)
print(conn.find_prompt())
