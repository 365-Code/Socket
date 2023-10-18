import socket

host='127.0.0.1'
port=1234
srvAddr=(host, port)


socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



connected=True
while connected:

    data = input("Enter your msg : ")
    socket.sendto(data.encode(), srvAddr)
    if(data == "disconnect"):
        connected=False
        break
    else:
        msg, srvAddr = socket.recvfrom(1024)
        msg = msg.decode()
        print (f"Server: {msg}")
        if(msg == "disconnect"):
            connected = False
            break
