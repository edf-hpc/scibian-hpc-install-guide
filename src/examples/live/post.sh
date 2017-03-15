#!/bin/bash -e

# Fix Timezone data
echo GMT > /etc/timezone
dpkg-reconfigure -f noninteractive tzdata

# Fix hostname
echo "localhost" > /etc/hostname

# Create needed directory for Puppet
mkdir -p /var/lib/puppet/facts.d/

# Enable setuid on /bin/ping to let users run it because AUFS does not support
# xattr and therefore capabilities.
chmod 4755 /bin/ping
