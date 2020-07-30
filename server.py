import threading
import socket

class Client:
    def __init__(self,nickname,address):
        self.nickname = nickname
        self.socketAddress = address
        
    def returnNick(self):
        return self.nickname
    
    def returnSocket(self):
        return self.socketAddress


class ServerLogic:
    def __init__(self):
        
        self.IP_ADDR = '127.0.0.1'
        self.PORT = 1236
        self.hostAndPort = (self.IP_ADDR,self.PORT)
        self.byteSize = 1024
        
        self.CODING = 'UTF-8'
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.server.bind(self.hostAndPort)
        self.clientList = []
        
        self.server.listen()
        print("[Server is running...]")
    
    
    def handlingServer(self,client):
        while True:
            try:
                
                message = client.socketAddress.recv(self.byteSize)
                
                if message.decode(self.CODING) == '/q':
                    raise("[disconnected]")
                
                message = bytes('[{}]-> '.format(client.nickname),encoding=self.CODING) + message
                self.broadcastMessage2(message,client)
            except:
                
                userLeft = ("[Server: User: {} has left]".format(client.nickname)).encode(self.CODING)
                
                self.broadcastMessage(userLeft)
                client.socketAddress.close()
                
                i = self.clientList.index(client)
                self.clientList.remove(client)
                del client
                
                break
    def broadcastMessage(self,message):  #  ZAKODUJ PRZED WYSLANIEM!
        
        try:
            for client in self.clientList:
                client.socketAddress.send(message)        
        except:
            print('')
            
    def broadcastMessage2(self,message,clientX):  #  ZAKODUJ PRZED WYSLANIEM!
        
        try:
            for client in self.clientList:
                if client == clientX:
                    continue
                
                client.socketAddress.send(message)        
        except:
            print('')
            
            
        
    def receiveMessage(self):
        while True:
            client, address = self.server.accept()
            print('[Connected user with address {}]'.format(str(address)))
            
            client.send(bytes(('[Server: Type your nick below]'),encoding=self.CODING))
            nickname = str(client.recv(self.byteSize).decode(self.CODING))
            c1 = Client(nickname,client)
            self.clientList.append(c1)
            
            arriveMsg = (bytes('[Server: {} has arrived!]'.format(c1.returnNick()),encoding=self.CODING))
            self.broadcastMessage(arriveMsg)
            c1.socketAddress.send(bytes('[Server: {} You are connected! press enter to proceed]'.format(c1.returnNick()),encoding=self.CODING))
            
            thread = threading.Thread(target=self.handlingServer, args=(c1,))
            thread.start()
            
            
            
            
s1 = ServerLogic()
s1.receiveMessage()
