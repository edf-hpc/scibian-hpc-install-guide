#!/bin/sh

# This is needed with bind 9.5 to make it:
#
# - start listening on new interfaces
# - stop listening on interfaces that don't exist anymore
#
# This becomes useless starting from bind >= 9.10 thanks to new
# automatic-interface-scan feature.

rndc reconfig
