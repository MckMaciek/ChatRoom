import socket
import threading

IP_ADDR = '127.0.0.1'
PORT = 1236
BYTE_SIZE = 1024
CODING = 'UTF-8'


portAndIpTuple = (IP_ADDR,PORT)

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(portAndIpTuple)

copiedMessage = ""

def receive():
    
    while True:
        try:
            message = client.recv(BYTE_SIZE).decode(CODING)
            if message == 'NICK':
                
                nickname = input()
                client.send(nickname.encode(CODING))
            else:
                print(message)
        except:
            client.close()
            break

def write():
    while True:
        
        print("[You]-> ",end="")
        inputMessage = input('')
        copiedMessage = inputMessage 
        
        message = '{}'.format(inputMessage)
        client.send(message.encode(CODING))
        print("")
        
        if copiedMessage == "/q":
            client.close()
            break
        
        
receive_thread = threading.Thread(target=receive)
receive_thread.start()

writing_thread = threading.Thread(target=write)
writing_thread.start()
