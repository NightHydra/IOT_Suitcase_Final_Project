#!/bin/bash

################################
# Launches a B.A.T.M.A.N. ad-hoc network on startup of the raspberry pi
# Must append "/usr/local/bin/setup-batman.sh &" to the end of /etc/rc.local right before the line that says "exit 0" for this script to autostart
# Author: Joe Pizzimenti
################################

#Disable NetworkManager in case its running (this is in case the user forgets to disable the service before setting this up)
systemctl stop NetworkManager
systemctl stop dhcpcd

# Added logs here for debug purposes. Script is now functional and ready to go
exec >> /var/log/batman-setup.log 2>&1
echo "Running BATMAN setup at $(date)"

# Wait 10 seconds for wlan0 to exist and be ready
sleep 2

# Setup ad-hoc network on wlan0
ip link set wlan0 down
iwconfig wlan0 mode ad-hoc
iwconfig wlan0 essid my-adhoc-net
iwconfig wlan0 channel 1
ip link set wlan0 up

# Wait a moment to make sure changes stick
sleep 2

# Load BATMAN service to the kernel and get this party started
modprobe batman-adv

# Attach to batman and configure IP
batctl if add wlan0
ip link set up dev bat0
ip addr add 192.168.199.X/24 dev bat0  # Replace X with desired IP. Joe=1, Alek=2, Julian=3

echo "BATMAN setup complete at $(date)"
