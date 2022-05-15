#!/bin/bash

modprobe zram
sudo zramctl --find --size 24G
sudo mkswap /dev/zram0
sudo swapon /dev/zram0

