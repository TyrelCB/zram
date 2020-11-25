# ZRAM

Create a Systemd System Service to manage a ZRAM swap based on a multiplier that you supply (default is 2)

## Setup

1. Clone Repository

    `git clone git@github.com:TyrelCB/zram.git`

2. cd into cloned directory

    `cd zram`
  
3. run service creation python script as **Privleged User!**

    `sudo python3 zram_service_creation.py`


## Verify ZRAM

Use one of the following:
- `bpytop` 
- `htop`
- `top -n 1 -E g -b |head`
- `free` 
- `cat /proc/meminfo |grep Total |grep "Mem\|Swap"`

## Stop/Start/Check Service

```
sudo systemctl stop zram.service
sudo systemctl start zram.service
sudo systemctl status zram.service
```
