#!/usr/bin/env python
# coding: utf-8

# # Purpose
#
# Create Systemd System Service


import subprocess
import sys


def run_cmd(command,do_print=False):
    output = subprocess.run(command,capture_output=True,shell=True,check=False,text=True)
    #print(output)
    if output.returncode == 0:
        if output.stdout:
            if do_print:print(output.stdout)
            result = output.stdout
        else:
            result = 'Success'
    else:
        if output.stderr:
            if do_print:print(output.stderr)
            result = output.stderr
        else:
            result = 'Failure'
    return result

if len(sys.argv) > 1:
    multiplier = int(sys.argv[1])
else:
    print('ZRAM multiplier? (Default = 2)')
    user_input = input()
    if user_input:
        multiplier = int(user_input)
    else:
        multiplier = 2

# aws mod
aws = False
cmd = 'uname -a'
result = run_cmd(cmd)
if '-aws' in result:
    aws = True
    cmd = 'sudo apt-get -y install linux-modules-extra-aws'
    run_cmd(cmd)
    round_up_size = 2
else:
    top_info = run_cmd('top -n 1 -E g -b |head')
    total_mem = top_info.splitlines()[3].split()[3]
    total_mem = float(total_mem)
    round_up_mem = int((total_mem // 1) + (total_mem % 1 > 0))
    round_up_mem
    print('Current Memory {} GB '.format(round_up_mem))
    size = float(round_up_mem)*multiplier
    round_up_size = int((size // 1) + (size % 1 > 0))
    round_up_size
    print('ZRAM Size {} GB '.format(round_up_size))

print('>>> Updating zram_start.sh')
start_script = '''#!/bin/bash

sudo modprobe zram
modprobe zram
sleep 2
sudo zramctl --find --size 2G
sudo mkswap /dev/zram0
sudo swapon /dev/zram0
'''.format(round_up_size)
print(start_script)

directory = run_cmd('pwd').strip()
result = run_cmd('sudo echo "{}" > {}/zram_start.sh'.format(start_script,directory))
print(result)

print('>>> Creating Service File')

service_file = '''
[Unit]
Description=Swap with zram
After=multi-user.target

[Service]
Type=oneshot
RemainAfterExit=true
ExecStart={}/zram_start.sh
ExecStop={}/zram_stop.sh

[Install]
WantedBy=multi-user.target
'''.format(directory,directory)


print(service_file)


result = run_cmd('sudo echo "{}" > /etc/systemd/system/zram.service'.format(service_file))
print(result)
if 'Permission' in result:
    print('>>> Need Sudo Privlige! sudo python3 zram_service_creation.py')
    quit()

# ## Enable Service and Start

result = run_cmd('systemctl daemon-reload')
print(result)
result = run_cmd('systemctl enable zram.service')
print(result)
result = run_cmd('systemctl restart zram.service')
print(result)
result = run_cmd('systemctl status zram.service')
print(result)

# if aws:
#     run_cmd('sudo systemctl reboot')
