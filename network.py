import socket
import pickle

class Network():
    def __init__(self):
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server="192.168.8.101"
        self.port=5555
        self.addr=(self.server, self.port)
        self.p=self.connect()
    def get_p(self):
        return self.p
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode('utf-8')
        except Exception as e:
            print('connect network')
            print(e)
    def send(self,data):
        try:
            self.client.sendall(str.encode(data))
        except Exception as e:
            print('send network')
            print(e)
    def receive(self):
        try:
            return self.client.recv(2048).decode('utf-8')
        except Exception as e:
            print('receive network')
            print(e)