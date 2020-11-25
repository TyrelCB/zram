#!/bin/bash

modprobe zram
sudo zramctl --find --size 32G
sudo mkswap /dev/zram0
sudo swapon /dev/zram0

