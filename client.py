from socket import *
import _thread
from datetime import datetime

#L'unica differenza con  gli altri client è che questo possiede la capacità
#di creare una thread che consente di stampare le risposte del server
#in maniera indipendente dall'input dell'utente

def receiver(clientSocket):
    while 1:
        reply = clientSocket.recv(2048)
        print("S: ", reply.decode("utf-8"))

SERVER_PORT = 35655
CLIENT_PORT = 65535
SERVER_ADDR = '37.100.252.168'

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.bind(("", CLIENT_PORT))
clientSocket.connect((SERVER_ADDR, SERVER_PORT))
clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
print("Connessione riuscita")

_thread.start_new_thread(receiver, (clientSocket,))
msg = ''
while msg != '.':
    msg = input("Io:")
    clientSocket.send(msg.encode('utf-8'))

clientSocket.close()