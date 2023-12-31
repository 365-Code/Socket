import socket
import threading

# Diffe helmen
# One to one client

host = '127.0.0.1'
# host = socket.gethostname()
port = 23000
ADDR = (host, port)
SIZE = 1024
DISCONNNECT_PROTOCOL = "disconnect"

userList = {}
msgList = {}

def countFiles(conn, addr):
    data = "[SERVER]: ready to receive"
    conn.send(data.encode())

    ftp = True
    count = 0
    msg = ""
    data = ""
    compData = ""

    while ftp:
        wordcount = 1
        msg = conn.recv(SIZE).decode()
        if (msg == "__SENT__"):

            data = f"[SERVER]: Total Files Count: {count}\n{compData}"
            # data = data + compData

            conn.send(data.encode())
            ftp = False
        else:
            f = msg.split(".")
            if len(f)>=2:
                count += 1

            data = "[SERVER]: FILE RECEIVED"
            if "txt" in f:
                data = "__TEXT__"
                conn.send(data.encode())
                file = conn.recv(SIZE).decode()

                file.strip()

                if not file:
                    compData = f"{compData}{msg}(wordcount): 0\n"
                
                else:
                    charFlag = 0
                    for char in file:
                        if (char == " " or char == "\n") and charFlag:
                            charFlag = 0
                            wordcount += 1
                        else:
                            charFlag = 1

                    # compData = compData + f"{msg}(wordcount): " + str(wordcount) + "\n"
                    compData = f"{compData}{msg}(wordcount): {wordcount}\n"

                # print(file)
                # conn.send( data.encode() )
            else:
                conn.send(data.encode())

def handleClient(conn, addr):
    
    client = {}
    msg = ""
    clientConnection = False

    # Client Name
    clientName = conn.recv(SIZE).decode()

    # Searching Client
    for addr, user in userList.items():
        print(user)
        uname = user[0]
        uconn = user[1]
        if uname == clientName:
            client = {"name":uname, "conn":uconn}
            clientConnection = True
            msg = f"{client.get('name')} Connected"
            conn.send(msg.encode())
            break

    
    if not clientConnection:
        msg = "No Client Found"
        conn.send(msg.encode())
        clientConnection = False
        return
    
    # Searching Sender
    sender = {}
    for addr, user in userList.items():
        uname = user[0]
        uconn = user[1]
        if uconn == conn:
            sender = {"name": uname, "conn": uconn}
            break
    
    # While Connection is going
    clientConnection = True
    while clientConnection:
        msg = conn.recv(SIZE).decode()
        if(msg == DISCONNNECT_PROTOCOL):
            clientConnection = False
            msg = f"DISCONNECTED TO {client.get('name')}\n"
            conn.send(msg.encode())

        elif (msg == "getMsg()"):
            getMsg()

        else:
            msg = f"[{sender['name']}]: {msg}\n"
            data = msgList.get(clientName) + msg
            msgList[clientName] = data
            # client['conn'].send(msg.encode())
            msg = f"SENT to {client.get('name')}"
            conn.send(msg.encode())

    return

def setName(conn, addr):
    # RECEIVE NAME
    nameReceived = False;
    while not nameReceived:
        name = conn.recv(SIZE).decode()
        flag = 0
        
        if (userList.get(addr)):
            msg = "Name Already Exist, ReEnter"
        else:
            msg = f"{name} Name Received"
            nameReceived = True
            userList[addr] = [name, conn]
            msgList[name] = ""
        conn.send(msg.encode())
    
    # NAME RECEIVED

def removeName(conn, addr):
    userList.pop(addr)

def getMsg(conn,addr):
    client = userList.get(addr)[0]
    data = msgList.get(client)
    if not data:
        data = "No new messages"
    msgList[client] = ""
    conn.send(data.encode())

def handleConnections(conn, addr):
    print(f"[NEW CONNECTION] {addr} CONNECTED")
    connected = True

    setName(conn, addr)
    while connected:
        msg = conn.recv(SIZE).decode()
        print(f"[CLIENT-{addr}] : {msg}")
        if(msg == "countFiles()"):
            countFiles(conn, addr)
        elif (msg == "sendMsg()"):
            handleClient(conn, addr)
        elif ( msg == DISCONNNECT_PROTOCOL ):
            data = f"[SERVER] : DISCONNECTED SUCCESSFULLY\n"
            conn.send(data.encode())
            connected = False
            removeName(conn, addr)
        elif (msg == "getMsg()"):
            # client = userList.get(addr)[0]
            # data = msgList.get(client)
            # msgList[client] = ""
            # conn.send(data.encode())
            getMsg(conn, addr)
            # continue
        else:
            data = f"[SERVER] : {msg} RECEIVED\n"
            conn.send(data.encode())
    conn.close()

def main():
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()

    print(f"[LISTENING] server is listening on {ADDR}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handleConnections, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    server.close()

if __name__ == "__main__":
    main()