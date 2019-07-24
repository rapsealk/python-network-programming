#!/usr/bin/python3

import os
import socket
import threading
import socketserver

SERVER_HOST = "localhost"
SERVER_PORT = 0	# tells the kernel to pickup a port dynamically
BUF_SIZE = 1024
ECHO_MSG = "Hello echo server!"

class ForkedClient():

	def __init__(self, ip, port):
		# Create a socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Connect to the server
		self.sock.connect((ip, port))

	def run(self):
		# Send the data to server
		current_process_id = os.getpid()
		print("PID %s sending echo message to the server: %s" % (current_process_id, ECHO_MSG))
		sent_data_length = self.sock.send(ECHO_MSG.encode("utf-8"))
		print("Sent: %d characters, so far..." % sent_data_length)

		# Display server response
		response = self.sock.recv(BUF_SIZE).decode("utf-8")
		print("PID %s received: %s" % (current_process_id, response[5:]))

	def shutdown(self):
		self.sock.close()

class ForkingServerRequestHandler(socketserver.BaseRequestHandler):

	def handle(self):
		# self.request is the TCP socket connected to the client.
		# Send the echo back to the client
		print("ForkingServerRequestHandler::handle()")
		print("client_address:", self.client_address[0])
		data = self.request.recv(BUF_SIZE).decode("utf-8")
		current_process_id = os.getpid()
		response = '%s: %s' % (current_process_id, data)
		print("Server sending response [current_process_id: data] = [%s]" % response)
		self.request.sendall(response.encode("utf-8"))

class ForkingServer(socketserver.ForkingMixIn, socketserver.TCPServer,):
	pass


def main():
	# Launch the server
	server = ForkingServer((SERVER_HOST, SERVER_PORT), ForkingServerRequestHandler)
	ip, port = server.server_address	# Retrieve the port number
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.daemon=True#.setDaemon(True)	# don't hang on exit
	server_thread.start()
	print("Server loop running PID: %s" % os.getpid())

	# Launch the client(s)
	client1 = ForkedClient(ip, port)
	client1.run()

	client2 = ForkedClient(ip, port)
	client2.run()

	# Clean them up
	server.shutdown()
	client1.shutdown()
	client2.shutdown()
	server.socket.close()
	server.server_close()


if __name__ == "__main__":
	main()
