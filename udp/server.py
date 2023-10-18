import socket

host='127.0.0.1'
port=1234
srvAddr=(host, port)


socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind(srvAddr)
print(f"Server is Listening at {srvAddr}")


while True:
    connected = True
    while connected:
        msg, addr = socket.recvfrom(1024)
        msg = msg.decode()
        print(f"{addr}-Client : {msg}")
        if(msg == "disconnect"):
            print(f"{addr} disconnected")
            connected = False
            break
        else:
            data = input("Enter your msg: ")
            socket.sendto(msg.encode(), addr)
            if(data == "disconnect"):
                print(f"Server shutting down")
                connected = False
                break
    break