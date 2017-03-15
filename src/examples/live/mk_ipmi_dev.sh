#!/bin/sh

DEVICE='/dev/ipmi0'

if [ -e ${DEVICE} ]
then
  exit 0
else
  MAJOR=$(grep ipmidev /proc/devices | awk '{print $1}')
  mknod --mode=0600 ${DEVICE} c ${MAJOR} 0 
fi
