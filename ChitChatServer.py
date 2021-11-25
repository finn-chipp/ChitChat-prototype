# Edited with GNU Nano so the tabbing's pretty strange on this one:
import socket, threading, os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("", 1515))
server.listen(30)

clients = []

def message(message):
	for i in clients:
		i.send(bytes(f"{len(message):<64}{message}", "ascii"))
	with open("log", "a") as f:
		f.write(message)

def handle(client, address, username):
	message(f"-----user \"{username}\" connected-----\n")
	while True:
		incoming = client.recv(int(client.recv(64).decode("ascii"))).decode("ascii")
		space = int(os.popen("tput cols").read().strip()) - len(f"{address[0]} : {address[1]}")
		if incoming == "stop":
			clients.remove(client)
			client.close()
			print(f"{'disconnection':<{space}}{address[0]} : {address[1]}")
			message(f"-----user \"{username}\" disconnected-----\n")
			break
		
		message(incoming)

		print(f"{'message':<{space}}{address[0]} : {address[1]}")
while True:
	client, address = server.accept()
	
	space = int(os.popen("tput cols").read().strip()) - len(f"{address[0]} : {address[1]}")

	print(f"{'connection':<{space}}{address[0]} : {address[1]}")
	
	clients.append(client)
	
	with open("log", "r") as f:
		history = f.read()
		client.send(bytes(f"{len(history):<64}{history}", "ascii"))

	client_thread = threading.Thread(target = handle, args = [client, address, client.recv(int(client.recv(64).decode("ascii"))).decode("ascii")])

	client_thread.start()
