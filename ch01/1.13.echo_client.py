#!/usr/bin/python3

import sys
import socket
import argparse

host = "localhost"

def echo_client(port):
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Connect the socket to the server
	server_address = (host, port)
	print("Connecting to %s port %s" % server_address)
	sock.connect(server_address)

	# Send data
	try:
		message = "Test message. This will be echoed"
		print("Sending: %s" % message)
		sock.sendall(message.encode("utf-8"))
		# Look for the response
		amount_received = 0
		amount_expected = len(message)
		while amount_received < amount_expected:
			data = sock.recv(16)
			amount_received += len(data)
			print("Received: %s" % data)
	except socket.errno as e:
		print("Socket error: %s" % e)
	except Exception as e:
		print("Other exception: %s" % e)
	finally:
		print("Closing connection to the server")
		sock.close()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Socket client example")
	parser.add_argument('--port', action="store", dest="port", type=int, required=True)
	args = parser.parse_args()
	port = args.port
	echo_client(port)
