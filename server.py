import socket

# host = '127.0.0.1'
host = socket.gethostname()
port = 23000

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((host, port))


socket.listen()

print(f"Server is listening {host}")


while True:
    conn, addr = socket.accept()

    print(f"Connected to {addr}")
    connected = True

    while(connected):
        
        print("Waiting for client...")
        msg = conn.recv(1024).decode()
        print(f"Client: {msg}")
        if(msg == "disconnect"):
            conn.close()
            connected = False
        else:
            data = input("Enter Server Message : ")
            conn.send(data.encode())
    break