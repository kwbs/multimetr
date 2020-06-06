import socket
import threading

class Channel:
    pass

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket,):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.channel=None
        self.log("New connection added: ", clientAddress)

    def run(self):
        self.log("Connection from : ", clientAddress)
        self.greeting_text = '''\n
            ___________________________________
           | Hi, This is from Server..         |
           | type 1 for start_measure command  |
           | type 2 for set_range command      |
           | type 3 for stop_measure command   |
           | type 4 for get_status command     |
           | type h for help                   |
           | type q for quit                   |
           |___________________________________| '''
        self.csocket.sendall(bytes(self.greeting_text, 'utf-8'))
        msg = ''
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode()
            parsed_command=self.parse_command(msg)
            result=self.handler_command(self.csocket,parsed_command)
            if result == 'end_loop':
                break
            self.log("from client", parsed_command)
            # self.csocket.sendall(bytes(parsed_command, 'UTF-8'))
        self.log("Client at ", clientAddress, " disconnected...")

    def log(self, *message):
        print("Client: ", *message)

    def parse_command(self,command):
        dict_commands={"1":"start_measure","2":"set_range","3":"stop_measure","4":"get_status","h":"help","q":"quit"}
        if command in dict_commands.keys():
            return dict_commands[command]
        else:
            return "type the correct command"
    
    def handler_command(self,csocket,command):
        if command == 'quit':
            self.csocket.close() 
            return "end_loop"
        elif command=="help":
            self.csocket.sendall(bytes(self.greeting_text, 'UTF-8'))
            return self.greeting_text
        else:
            self.csocket.sendall(bytes(command, 'UTF-8'))



LOCALHOST = "192.168.88.250"
PORT = 9090
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()
