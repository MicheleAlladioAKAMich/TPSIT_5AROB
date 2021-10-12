'''
costruire una chat TCP che affronta il problema dell'invio di un messaggio da un utente ad un altro
gli utenti devono essere identificati tramite un identificatore univoco (es: nickname) 
ci sarà un server che genera dinamicamente un dizionario nickname:ip 
appena il client conosce il nickname manda un messaggio al server, così conosce anche l'ip tramite la recvfrom,
il server risponde con un OK 
hello = f"NICKNAME:{nickname}"
'''

import socket as sck, threading as thr, logging

BUFFER = 4096

clientList = []
dizUsers = {}

logging.basicConfig(level=logging.DEBUG)

class Client_Manager(thr.Thread):
    def __init__(self, connection, nickname):
        thr.Thread.__init__(self)   #costruttore super (java)
        self.connection = connection
        self.nickname = nickname
        self.running = True
    
    def run(self):
        while self.running:

            #DIVISIONE DEL MESSAGGIO
            message = self.connection.recv(BUFFER).decode()
            splittedMessage = message.split(':')

            #INVIO DELLA LISTA DI UTENTI
            if splittedMessage[1] == '!LIST':
                logging.info(f'{splittedMessage[0]} ha richiesto la lista di utenti connessi')
                for client in clientList:   #ricerca del destinatario
                    if client.nickname == splittedMessage[0]:
                        client.connection.sendall(f'{dizUsers}'.encode())
            
            else:
                #INVIO DI UN MESSAGGIO DA UN UNTENTE ALL'ALTRO
                logging.info(f'Messaggio spedito da {splittedMessage[0]} a {splittedMessage[1]}: {splittedMessage[2]}')

                for client in clientList:   #ricerca del destinatario
                    if client.nickname == splittedMessage[1]:   
                        client.connection.sendall(f'Messaggio da {splittedMessage[0]}: {splittedMessage[2]}'.encode())

def main():
    global clientList, dizUsers

    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM) #creo un socket TCP / IPv4
    s.bind(('127.0.0.1', 7000)) 
    s.listen()

    cnt = 0

    while True:
        connection, addr = s.accept()   #data = stringa ricevuta    addr -> tupla (IP client, porta client)

        nickname = connection.recv(BUFFER).decode().split(':')[-1] #split del nickname, prende la parte dopo i : 

        if nickname == '':  #se l'utente non mette un nickname --> guest0, guest1, guest2, ....
            nickname = f'guest{cnt}'    #guest1, guest2, guest3,....
            cnt+=1

        logging.info(f'New user: {nickname}')

        #aggiunta del nickname al dizionario del server
        dizUsers[nickname] = addr
        print(dizUsers)

        #creazione del thread (uno per ogni client connesso)
        client = Client_Manager(connection, nickname)
        clientList.append(client)
        client.start()

        #invio messagio per la chatmode
        msg = 'OK'.encode()
        connection.sendall(msg)


if __name__ == "__main__":
    main()

