#!/bin/bash
S_FILE="/var/lib/apt/periodic/update-success-stamp"
T_FILE="/tmp/apt-touchstamp-${RANDOM}"
touch -d '-15 minutes' $T_FILE
if [ -e $S_FILE ] ; then
    if [ $T_FILE -nt $S_FILE ] ; then
        echo true
    else
        echo false
    fi
else
    echo true
fi
rm -f $T_FILE
exit