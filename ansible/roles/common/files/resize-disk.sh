#!/bin/sh

echo ", +" | sfdisk -N 4 -a --no-reread /dev/vda
partprobe
btrfs filesystem resize 1:max /
