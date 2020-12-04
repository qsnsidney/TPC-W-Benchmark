import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
SERVER_PORT = 3400        # Port to listen on (non-privileged ports are > 1023)
CLIENT_PORT = 3306

# conn - with client
# soc - with mysql
# encodings: "ISO-8859-9", "utf-8"
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, SERVER_PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        '''
        #data = conn.recv(1024)
        #print("from client:", data)
        print("connect to mysql")
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        soc.connect((HOST, CLIENT_PORT))
        #soc.sendall(data)
        data = soc.recv(1024) # data from mysql server
        print(data.hex())
        print(data)
        print("length:", len(data))
        #l = data.replace(b"\xff", b"\x00").split(b"\x00")
        #for i in l:
        #    print(i.decode("utf-8"))
        #print("data from mysql:", data[4:].decode("utf-8"))
        '''
        # fake handshake - always return OK
        handshake = bytes.fromhex("4a0000000a382e302e323200420000007501106664640b3000ffffff0200ffc715000000000000000000001f56193f3064355a0b21135e006d7973716c5f6e61746976655f70617373776f726400")
        conn.sendall(handshake)
        handshakeresponse = conn.recv(1024)
        ok = bytes.fromhex("0700000200000002000000")
        conn.sendall(ok)
        print("handshake done")
        while True:
            data = conn.recv(1024) # receive new request from client 
            print(data)
            if not data:
                print("connection ends by client")
                break
            print(data.hex())
            print("length:", len(data))
            #print("data from client:", data[4:].decode("utf-8"))
            '''
            soc.sendall(data) # forward new request to mysql server
            data = soc.recv(1024) # data from mysql
            if not data:
                print("connection ends by mysql")
                break
            print(data.hex())
            print("length:", len(data))
            #print("data from mysql:", data[4:].decode("utf-8"))
            '''


            