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

def countFiles(conn, addr):

    data = "[SERVER]: ready to receive"
    conn.send(data.encode())

    ftp = True
    count = 0
    msg = ""
    data = ""

    while ftp:
        msg = conn.recv(SIZE).decode()
        if (msg == "__SENT__"):
            data = f"[SERVER]: Total Files Count: {count}"
            conn.send(data.encode())
            ftp = False
        else:
            f = msg.split(".")
            if len(f) >= 2:
                count += 1
            data = "[SERVER]: FILE RECEIVED"
            conn.send(data.encode())

def handleConnections(conn, addr):
    print(f"[NEW CONNECTION] {addr} CONNECTED")
    connected = True
    while connected:
        msg = conn.recv(SIZE).decode()
        print(f"[CLIENT-{addr}] : {msg}")
        if(msg == "countFiles()"):
            countFiles(conn, addr)

        elif ( msg == DISCONNNECT_PROTOCOL ):
            data = f"[SERVER] : DISCONNECTED SUCCESSFULLY"
            conn.send(data.encode())
            connected = False
        else:
            data = f"[SERVER] : {msg} RECEIVED"
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


if __name__ == "__main__":
    main()