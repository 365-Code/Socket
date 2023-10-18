import socket
import os

# host = socket.gethostbyname('LAPTOP-NCLJ4M38') #siddiqul
# host = socket.gethostbyname('LAPTOP-LLHFBHBJ') #musharraf
host = socket.gethostbyname('LAPTOP-EHJ8VBPC') #musharraf

# host = '127.0.0.1'
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
        # print(msg)

    msg = "__SENT__" 
    client.send(msg.encode())
    msg = client.recv(SIZE).decode()
    print(msg) 

def main():
    connected = True
    while connected:
        data = input("Enter Msg : ")
        client.send(data.encode())
        
        if(data == "countFiles()"):
            sendFiles()

        elif(data == "disconnect"):
            msg = client.recv(SIZE).decode()
            print(msg)
            client.close()
            connected = False

        else:
            # print("Waiting for server...")
            msg = client.recv(SIZE).decode()
            print(msg)
    

if __name__ == "__main__" :
    main()
