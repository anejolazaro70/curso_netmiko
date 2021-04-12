#!/usr/bin/env python

from netmiko import ConnectHandler
from getpass import getpass

password = getpass()

devices = [
    {
        "host": "nxos1.lasthop.io",
        "device_type": "cisco_nxos",
        "username": "pyclass",
        "password": password,
        "session_log": "ex03a_nxos1.log",
    },
]

config = ["terminal width 80", "hostname verylonghostnamefornxos"]
command = " show ip interface brief vrf management | include management"

config_after = "hostname nxos1"

for dev in devices:
    with ConnectHandler(**dev) as conn:
        output = conn.find_prompt()
        print(output)
        if output != "verylonghostnamefornxos#":
            output = conn.send_config_set(config)
            print(output)
        try:
            output = conn.send_command(command)
            print(output)
        except NetmikoTimeoutException:
            print("... long command failed with an exception")
        finally:
            output = conn.send_config_set(config_after)
            print(output)
