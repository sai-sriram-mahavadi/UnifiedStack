# Set Log level
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
url --url=http://19.19.15/cblr/links/rhel-server-7.0-x86_64
# If any cobbler repo definitions were referenced in the kickstart profile, include them here.

# Network information
network --bootproto=dhcp --device=enp1s0f0 --onboot=on  

# Reboot after installation
reboot

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



# Enable installation monitoring

%end

%post
set -x -v
exec 1>/root/ks-post.log 2>&1

# Start yum configuration

# End yum configuration



# Start post_install_network_config generated code
# End post_install_network_config generated code

#


# Start download cobbler managed config files (if applicable)
# End download cobbler managed config files (if applicable)
# Start koan environment setup

# End koan environment setup

# begin Red Hat Network certificate-based server registration
# not configured to use Certificate-based RHN (ok)
# end Red Hat Network certificate-based server registration

## Begin cobbler registration
# cobbler registration is disabled in /etc/cobbler/settings
# End cobbler registration

# Enable post-install boot notification

# Start final steps

# End final steps
%end

