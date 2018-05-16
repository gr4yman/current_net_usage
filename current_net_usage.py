#!/usr/bin/env python3

'''
Name         : current_net_usage.py
Author       : grayman <grayman@zr0s.org>
Description  : Get's current RX/TX Bytes per second for each network device on
               a Linux system.
'''

import os, sys, math, time

sysdir = '/sys/class/net/'

# Get the statistics by interface, then return them
def get_stats(iface):
	statdir = sysdir + iface + '/statistics/'
	
	# open the rx/tx bytes statistics files
	rx = open(statdir + 'rx_bytes', 'r')
	tx = open(statdir + 'tx_bytes', 'r')
	
	rx_read = int(rx.read().rstrip())
	tx_read = int(tx.read().rstrip())
	
	rx.close()
	tx.close()
	
	return (rx_read, tx_read)

# Convert bytes to human readable and return the string
def byte_convert(byte):
	if(byte == 0):
		result = '%6s kB/s' % 0
	else:
		byte_type = ("k", "M", "G", "T", "P", "E", "Z", "Y")
		
		i = int(math.floor(math.log(byte,1024)))
		r = str(round(byte/(math.pow(1024,i)),2))
		
		result = '%6s %sB/s' % (r, byte_type[i])

	return result
	
def main():
	devices = os.listdir(sysdir)

	# get the stats, sleep for 1 sec, get the diff, and report Bs
	for i in devices:
		(rx1, tx1) = get_stats(i)
		time.sleep(1)
		(rx2, tx2) = get_stats(i)
		
		tx_format = byte_convert(tx2 - tx1)
		rx_format = byte_convert(rx2 - rx1)
		
		print("Device: %-14s Rx: %-14s Tx: %s" % (i, rx_format, tx_format))
	
if __name__ == "__main__":
        main()
