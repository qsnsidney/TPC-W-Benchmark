import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
SERVER_PORT = 3400        # Port to listen on (non-privileged ports are > 1023)
CLIENT_PORT = 3306

# conn - with client
# soc - with mysql
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, SERVER_PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        #data = conn.recv(1024)
        #print("from client:", data)
        print("connect to mysql")
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        soc.connect((HOST, CLIENT_PORT))
        #soc.sendall(data)
        data = soc.recv(1024) # data from mysql server
        print("data from mysql:", data)
        while True:
            conn.sendall(data) # forward data to client
            data = conn.recv(1024) # receive new request from client 
            if not data:
                print("connection ends by client")
                break
            print("data from client:", data)
            soc.sendall(data) # forward new request to mysql server
            data = soc.recv(1024) # data from mysql
            if not data:
                print("connection ends by mysql")
                break
            print("data from mysql:", data)


            