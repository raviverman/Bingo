import socket

class Network(object):
    def __init__(self, serverIP=None, serverPort=9000):
        self.serverSocket = None
        self.serverPort = serverPort 
        self.serverIP = serverIP
        self.clientSocket = None

    def startServer(self):
        """
        starts server locally and listens at port in serverPort
        """
        # open a IPv4 TCP socket 
        self.serverSocket = socket.socket(socket.AF_INET,
                                          socket.SOCK_STREAM)
        try:
            # bind socket to a port
            self.serverSocket.bind(("", self.serverPort))

            # server queue length 3
            self.serverSocket.listen(3)
        except:
            print(f"Port {self.serverPort} busy")
            return
        
        self.clientSocket, _ = self.serverSocket.accept()
        return self.clientSocket

    def connectServer(self):
        """
        connect to server via IP set in self.serverIP
        """
        assert self.serverIP is not None
        self.clientSocket = socket.socket()
        try:
            self.clientSocket.connect((self.serverIP, self.serverPort))
            print(f"Connected to Server: {self.serverIP} at {self.serverPort}")
        except:
            print("Unable to connect to server")
            return
    
    def send(self, data:str):
        """
        sends string data by converting it to bytes
        """
        byteData = data.encode("UTF-8")
        self.clientSocket.send(byteData)

    def receive(self):
        """
        receives data in bytes and converts it to string & return
        """
        byteData = self.clientSocket.recv(1024)
        data = byteData.decode("UTF-8")
        return data

    def cleanup(self):
        if isinstance(self.serverSocket, socket.socket):
            self.serverSocket.close()
        if isinstance(self.clientSocket, socket.socket):
            self.clientSocket.close()
        

if __name__ == "__main__":
    # test network api
    net = Network()
    client = net.startServer()
    print ("Connected to %s" % (client))
    net.cleanup()
        
