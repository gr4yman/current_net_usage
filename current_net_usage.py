#!/usr/bin/env python3
'''
Name         : current_net_usage.py
Author       : grayman <grayman@zr0s.org>
Description  : Get's current RX/TX Bytes per second for each network device on
               a Linux system.
'''

import os, sys, math, time

# Get the statistics by interface, then return them
def get_stats(iface):
	# the statistics directory for the interface
	statdir = f'{sysdir}{iface}/statistics/'
	
	# create a couple empty variables for rx/tx
	rx_read = tx_read = ''

	# Open the tx and rx files, read the count, convert to int, and return it
	with open(statdir + 'rx_bytes', 'r') as rx:
		rx_read = int(rx.read().rstrip())

	with open(statdir + 'tx_bytes', 'r') as tx:
		tx_read = int(tx.read().rstrip())
	
	return (rx_read, tx_read)

# Convert bytes to human readable and return the string
def byte_convert(byte):
	if(byte == 0): # If 0 bytes, return 0
		result = '0 kB/s'
	else: # Convert and return in bytes. 
		byte_type = ("k", "M", "G", "T", "P", "E", "Z", "Y")
		
		i = int(math.floor(math.log(byte,1024)))
		r = str(round(byte/(math.pow(1024,i)),2))
		
		result = f'{r} {byte_type[i]}B/s'

	return result
	
def main():
	# Variables
	global sysdir 
	sysdir = '/sys/class/net/'
	devices = os.listdir(sysdir) # List the ethernet devices

	# Get the stats, sleep for 1 sec, get the diff, and report Bs
	for i in devices:
		(rx1, tx1) = get_stats(i)
		time.sleep(1)
		(rx2, tx2) = get_stats(i)
		
		tx_format = byte_convert(tx2 - tx1)
		rx_format = byte_convert(rx2 - rx1)
		
		print(f"Device: {i:18} Rx: {rx_format:18} Tx: {tx_format}")
	
if __name__ == "__main__":
        main()