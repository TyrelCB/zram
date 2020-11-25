#!/bin/bash

sudo swapoff /dev/zram0
sudo zramctl --reset /dev/zram0
