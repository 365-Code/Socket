import socket
import os

# host = socket.gethostbyname('LAPTOP-NCLJ4M38') #siddiqul
# host = socket.gethostbyname('LAPTOP-LLHFBHBJ') #musharraf
# host = socket.gethostbyname('LAPTOP-EHJ8VBPC') #musharraf

host = '127.0.0.1'
port = 23000
ADDR = (host, port)
SIZE = 1024
DISCONNNECT_PROTOCOL = "disconnect"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

print("Client is conected")

# files = os.listdir('./files')

def sendFiles():
    msg = client.recv(SIZE).decode()
    print(msg)
    data = input("Enter File Path : ")
    pth = os.path.abspath(data)
    files = os.listdir(pth)

    for file in files:
        client.send(file.encode())
        msg = client.recv(SIZE).decode()
        if(msg == "__TEXT__"):
            with open(f"{pth}/{file}") as f:
                msg = f.read()
                client.send(msg.encode())
    
    msg = "__SENT__" 
    client.send(msg.encode())
    msg = client.recv(SIZE).decode()
    print(msg)

def sendName():
    nameSent = False
    while not nameSent:
        data = input("Enter Unique Name: ");
        client.send(data.encode())
        msg = client.recv(SIZE).decode()
        if msg == f"{data} Name Received":
            nameSent = True
        print(msg)

def sendClient():
    msg = ""
    # Sending another Client name to Connect
    data = input("Enter Client Name: ")
    client.send(data.encode())
    msg = client.recv(SIZE).decode()
    print(msg)
    if(msg == "No Client Found"):
        return
    
    clientConnection = True
    while clientConnection:
        data = input(f"Enter Your Msg to {data}: ")
        client.send(data.encode())
        if(data == DISCONNNECT_PROTOCOL):
            clientConnection = False
        msg = client.recv(SIZE).decode()
        print(msg)
    return

def main():
    connected = True
    print("Client = ", client)
    # SENDING NAME
    sendName()
    # NAME SENT

    while connected:
        data = input("Enter Msg : ")
        client.send(data.encode())
        
        if (data == "countFiles()"):
            sendFiles()
        
        elif (data == "sendMsg()"):
            sendClient()

        elif (data == "disconnect"):
            msg = client.recv(SIZE).decode()
            print(msg)
            client.close()
            connected = False
        
        elif (data == "getMsg()") :
            msg = client.recv(SIZE).decode()
            print(msg)

        else:
            # print("Waiting for server...")
            msg = client.recv(SIZE).decode()
            print(msg)
    

if __name__ == "__main__" :
    main()