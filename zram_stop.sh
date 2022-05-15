#!/bin/bash

sudo swapoff /dev/zram0
sleep 2
sudo zramctl --reset /dev/zram0
