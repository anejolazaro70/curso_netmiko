#!/usr/bin/env python

from netmiko import ConnectHandler
from concurrent.futures import ProcessPoolExecutor, as_completed
from getpass import getpass
from yaml import load
from datetime import datetime

password = getpass()

def load_devices(inv_file=None):
    with open(inv_file, 'r') as fh:
        devices = load(fh)
    return devices

def command(dev_type=None):
    cmd_line = {'cisco_xe': 'show ip arp',
                'arista_eos': 'show ip arp',
                'juniper_junos': 'show arp',
                'cisco_nxos': 'show ip arp vrf management'}
    try:
        cmd = cmd_line[dev_type]
    except Exception as error:
        print(str(error))
        cmd = None

    return cmd

def send_cmd(dev_name=None, data=None, cmd=None):
    try:
        with ConnectHandler(**data) as conn:
            output = conn.send_command(cmd)
    except Exception:
        print('error en argumentos')
        output = None
    return dev_name, output

def  main():

    t0 = datetime.now()

    inventory = 'inventory.yaml'
    max_threads = 10
    futures_list = list()

    devices = load_devices(inventory)

    pool = ProcessPoolExecutor(max_threads)

    for dev, data in devices.items():
        cmd = command(data['device_type'])
        if cmd:
            dev_name = data['host']
            data['password'] = password
            future = pool.submit(send_cmd, dev_name=dev_name, data=data, cmd=cmd)
            futures_list.append(future)
        else:
            print(f'Device {dev} not supported')
            continue

    for future in as_completed(futures_list):
        device, output = future.result()
        print(40*'=')
        print(f'Device: {device}')
        print(40*'=')
        print(output)
    t1 = datetime.now()
    print(f'Elapsed time: {t1 - t0}')

if __name__ == '__main__':
    main()
