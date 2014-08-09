#!/bin/bash

function die {
    echo "PROBLEMS ${1}"
    exit 1
}

if [ "$(fdisk -l /dev/sda | grep sda1 | wc -l)" == "0" ] ; then
    die "No USB dribve!"
fi

mount /dev/sda1 /mnt || die "unable to mount!"

mkdir -p /mnt/backups || die "unable to mkdir!"

rsync -r /var/log/nginx /mnt/backups || die "unable to rsync nginx!"
rsync -r /var/lib/collectd/tribesthatmaybe /mnt/backups || die "unable top rsync tribesthatmaybe!"

umount /mnt || die "unable to unmount!"
