from socket import *
import register as re
import _thread
from datetime import datetime
import cacheHandler as han

##############################################################################################
#Al momento le funzioni arrivano fino al momento in cui devo comunicare con il secondo utente#
#A differenza del UDP non è possibile specificare l'indizzio del ricevente                   #
##############################################################################################

def SendMessage(clientSocket, msg):
    #Invia un stringa da stampare al client
    clientSocket.send(msg.encode("utf-8"))

def handler(clientSocket, clientAddress):
    #L'handler gestisce la singola connessione
    #E' necessario che l'utente si loggi prima di procedere alla fase di comunicazione
    #Questo fa si che il file register_df.csv possa aggiornare il suo indirizzo ip 
    #rendendolo raggiungibile dagli altri utenti
    SendMessage(clientSocket, "Premere 1 per registrasi o 2 per loggarsi")
    reply = clientSocket.recv(2048).decode("utf-8")
    if reply == "1":
        #Sistema di registrazione
        SendMessage(clientSocket, "Inserire username")
        username = clientSocket.recv(2048).decode("utf-8")
        SendMessage(clientSocket, "Inserire password")
        password = clientSocket.recv(2048).decode("utf-8")
        if re.Register(username, password) == 0:
            SendMessage(clientSocket, "Errore, utente già registrato")
        print("Registrazione effettuata")
        #Il caso di registrazione attualmente non è in grado di aggiorare l'ip dell'utente
        #necessitando quindi di un login successivo per farlo
        handler(clientSocket, clientAddress)
    elif reply == "2":
        SendMessage(clientSocket, "Inserire username")
        username = clientSocket.recv(2048).decode("utf-8")
        SendMessage(clientSocket, "Inserire password")
        password = clientSocket.recv(2048).decode("utf-8")
        address = clientAddress[0]
        if re.Login(username, password, address) == 0:
            handler(clientSocket, clientAddress)
            SendMessage(clientSocket, "Password errata o username inesistente")
        print("Login effettuato")
    #A login effettuato si procede con la fase di recupero dell'indirizzo ip dell'utente
    #con cui comunicare
    MsgCache(clientSocket)
    clientSocket.close()

def MsgCache(clientSocket):
    #La funzione è abbastanza semplice:
    #In base allo username inserito dall'utente, si cerca il suo corrispettivo indirizzo ip
    #E lo si restituisce in una variabile che potrà essere successivamente usata
    #per instaurare una connessione
    SendMessage(clientSocket, "Con chi vuoi aprire la connessione? (Digitare il suo username)")
    peerUsername = clientSocket.recv(2048)
    peerAddress = re.FindUserAddress(peerUsername)
    if peerAddress == 0:
        SendMessage(clientSocket, "Errore, l'utente non è stato trovato") 
        MsgCache(clientSocket)
    while msg != '.':
        SendMessage(clientSocket, "Inserire contenuto del messaggio")
        msg = client.recv(2048)
        han.RegisterMsg(datetime.now,peerUsername,msg)

    
SERVER_PORT = 35655
CLIENT_PORT = 65535
SERVER_ADDR = '37.100.252.168'

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', SERVER_PORT))
serverSocket.listen(20)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

print("Up and running..")

while 1:
    currentSocket, clientAddress = serverSocket.accept()
    print("Connesso con: ", clientAddress)
    _thread.start_new_thread(handler, (currentSocket, clientAddress,))