# System authorization information
auth  --useshadow  --enablemd5
# System bootloader configuration
bootloader --location=mbr
# Partition clearing information
clearpart --all --initlabel
# Use text mode install
#text
# Firewall configuration
firewall --disable
# System keyboard
keyboard us
# System language
lang en_US
# Use network installation
url --url=http://192.168.3.31/cblr/links/rhel-server-7.0-x86_64
# If any cobbler repo definitions were referenced in the kickstart profile, include them here.

# Network information
# Using "new" style networking config, by matching networking information to the physical interface's 
# MAC-address
%include /tmp/pre_install_network_config

# Reboot after installation
#reboot

#Root password
rootpw --iscrypted $1$wXrga6Zv$XeJri29DN5WODwQNytnFy0
# SELinux configuration
selinux --disabled
# Do not configure the X Window System
#skipx
# System timezone
timezone  America/New_York
# Install OS instead of upgrade
install
# Clear the Master Boot Record
zerombr
# Allow anaconda to partition the system as needed
ignoredisk --only-use=sda
autopart

%packages
@ base
@ core
%end

%pre
set -x -v
exec 1>/tmp/ks-pre.log 2>&1

# Once root's homedir is there, copy over the log.
while : ; do
    sleep 10
    if [ -d /mnt/sysimage/root ]; then
        cp /tmp/ks-pre.log /mnt/sysimage/root/
        logger "Copied %pre section log to system"
        break
    fi
done &


wget "http://192.168.3.31/cblr/svc/op/trig/mode/pre/system/cvf3-server-a4" -O /dev/null
# Start pre_install_network_config generated code
# generic functions to be used later for discovering NICs
mac_exists() {
  if which ip 2>/dev/null >/dev/null; then
    ip -o link | grep -i "$1" 2>/dev/null >/dev/null
    return $?
  elif which esxcfg-nics 2>/dev/null >/dev/null; then
    esxcfg-nics -l | grep -i "$1" 2>/dev/null >/dev/null
    return $?
  else
    ifconfig -a | grep -i "$1" 2>/dev/null >/dev/null
    return $?
  fi
}
get_ifname() {
  if which ip 2>/dev/null >/dev/null; then
    IFNAME=$(ip -o link | grep -i "$1" | sed -e 's/^[0-9]*: //' -e 's/:.*//')
  elif which esxcfg-nics 2>/dev/null >/dev/null; then
    IFNAME=$(esxcfg-nics -l | grep -i "$1" | cut -d " " -f 1)
  else
    IFNAME=$(ifconfig -a | grep -i "$1" | cut -d " " -f 1)
    if [ -z $IFNAME ]; then
      IFNAME=$(ifconfig -a | grep -i -B 2 "$1" | sed -n '/flags/s/:.*$//p')
    fi
  fi
}

# Start of code to match cobbler system interfaces to physical interfaces by their mac addresses
#  Start eth2
# Configuring eth2 (b0:fa:eb:97:6b:00)
if mac_exists b0:fa:eb:97:6b:00
then
  get_ifname b0:fa:eb:97:6b:00
  echo "network --device=$IFNAME --bootproto=dhcp --hostname=cvf3-server-a4" >> /tmp/pre_install_network_config
fi
# End pre_install_network_config generated code

# Enable installation monitoring

%end

%post
set -x -v
exec 1>/root/ks-post.log 2>&1

# Start yum configuration

# End yum configuration



# Start post_install_network_config generated code

# create a working directory for interface scripts
mkdir /etc/sysconfig/network-scripts/cobbler
cp /etc/sysconfig/network-scripts/ifcfg-lo /etc/sysconfig/network-scripts/cobbler/

# set the hostname in the network configuration file
grep -v HOSTNAME /etc/sysconfig/network > /etc/sysconfig/network.cobbler
echo "HOSTNAME=cvf3-server-a4" >> /etc/sysconfig/network.cobbler
rm -f /etc/sysconfig/network
mv /etc/sysconfig/network.cobbler /etc/sysconfig/network

# Also set the hostname now, some applications require it
# (e.g.: if we're connecting to Puppet before a reboot).
/bin/hostname cvf3-server-a4

# Start configuration for eth2
echo "DEVICE=eth2" > /etc/sysconfig/network-scripts/cobbler/ifcfg-eth2
echo "ONBOOT=yes" >> /etc/sysconfig/network-scripts/cobbler/ifcfg-eth2
echo "HWADDR=B0:FA:EB:97:6B:00" >> /etc/sysconfig/network-scripts/cobbler/ifcfg-eth2
IFNAME=$(ip -o link | grep -i 'B0:FA:EB:97:6B:00' | sed -e 's/^[0-9]*: //' -e 's/:.*//')
if [ -f "/etc/modprobe.conf" ] && [ $IFNAME ]; then
    grep $IFNAME /etc/modprobe.conf | sed "s/$IFNAME/eth2/" >> /etc/modprobe.conf.cobbler
    grep -v $IFNAME /etc/modprobe.conf >> /etc/modprobe.conf.new
    rm -f /etc/modprobe.conf
    mv /etc/modprobe.conf.new /etc/modprobe.conf
fi
echo "TYPE=Ethernet" >> /etc/sysconfig/network-scripts/cobbler/ifcfg-eth2
echo "BOOTPROTO=dhcp" >> /etc/sysconfig/network-scripts/cobbler/ifcfg-eth2
# End configuration for eth2

sed -i 's/ONBOOT=yes/ONBOOT=no/g' /etc/sysconfig/network-scripts/ifcfg-eth*

rm -f /etc/sysconfig/network-scripts/ifcfg-eth2
mv /etc/sysconfig/network-scripts/cobbler/* /etc/sysconfig/network-scripts/
rm -r /etc/sysconfig/network-scripts/cobbler
if [ -f "/etc/modprobe.conf" ]; then
cat /etc/modprobe.conf.cobbler >> /etc/modprobe.conf
rm -f /etc/modprobe.conf.cobbler
fi
# End post_install_network_config generated code

#


# Start download cobbler managed config files (if applicable)
# End download cobbler managed config files (if applicable)
# Start koan environment setup
echo "export COBBLER_SERVER=192.168.3.31" > /etc/profile.d/cobbler.sh
echo "setenv COBBLER_SERVER 192.168.3.31" > /etc/profile.d/cobbler.csh
# End koan environment setup

# begin Red Hat Network certificate-based server registration
# not configured to use Certificate-based RHN (ok)
# end Red Hat Network certificate-based server registration

## Begin cobbler registration
# skipping for system-based installation
# End cobbler registration

# Enable post-install boot notification

# Start final steps

wget "http://192.168.3.31/cblr/svc/op/ks/system/cvf3-server-a4" -O /root/cobbler.ks
wget "http://192.168.3.31/cblr/svc/op/trig/mode/post/system/cvf3-server-a4" -O /dev/null
wget "http://192.168.3.31/cblr/svc/op/nopxe/system/cvf3-server-a4" -O /dev/null
# End final steps
%end

