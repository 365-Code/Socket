import socket

# host = socket.gethostbyname('LAPTOP-NCLJ4M38') # siddiqul
# host = socket.gethostbyname('LAPTOP-LLHFBHBJ') # musharraf
host = '127.0.0.1'
port = 23000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

print("Client is conected")
connected = True

while connected:
    data = input("Enter Client Message : ")
    client.send(data.encode())
    if(data == "disconnect"):
        client.close()
        connected = False
        print("Client Disconnected")
    else:
        print("Waiting for server...")
        msg = client.recv(1024).decode()
        print(f"Server: {msg}")