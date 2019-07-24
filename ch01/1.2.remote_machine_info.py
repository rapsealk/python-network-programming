#!/usr/bin/python3

import socket

def get_remote_machine_info():
	remote_host = 'www.python.org'
	try:
		print("IP address of %s: %s" %(remote_host, socket.gethostbyname(remote_host)))
	except socket.gaierror as e:
		print("%s: %s" %(remote_host, e))


if __name__ == "__main__":
	get_remote_machine_info()
