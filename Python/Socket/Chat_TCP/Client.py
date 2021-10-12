'''
costruire una chat TCP che affronta il problema dell'invio di un messaggio da un utente ad un altro
gli utenti devono essere identificati tramite un identificatore univoco (es: nickname) 
ci sarà un server che genera dinamicamente un dizionario nickname:ip 
appena il client conosce il nickname manda un messaggio al server, così conosce anche l'ip tramite la recvfrom,
il server risponde con un OK 
hello = f"NICKNAME:{nickname}"
Se il client manda f"!LIST" il server risponde con la lista di utenti
'''

import socket as sck, string, time
import threading as thr, logging

logging.basicConfig(level=logging.DEBUG)

BUFFER = 4096   #numero massimo di informazioni traslabili
chatmode = False

class Receive_message(thr.Thread):
    def __init__(self, s):
        thr.Thread.__init__(self)   #costruttore super (java) 
        self.running = True
        self.s = s

    def run(self):
        #RICEZIONE MESSAGGI
        while self.running:   
            data = self.s.recv(BUFFER).decode()
            print(data)

def main():
    global chatmode

    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)  #creo un socket TCP / IPv4
    s.connect(('localhost', 7000))

    #invio del nickname
    nickname = input("Inserisci il tuo nickname: ")
    msg = f'NICKNAME:{nickname}'.encode()
    s.sendall(msg)
    logging.info("Connessione avvenuta")

    #attivazione chatmode
    data = s.recv(BUFFER)
    if data.decode()[0:2].upper() == 'OK':
        chatmode = True

    #thread per la ricezione dei messaggi
    receiver = Receive_message(s)
    receiver.start()

    while chatmode:
        choose = input("!LIST per richiedere la lista di utenti connessi: ").upper()

        #RICHIESTA DELLA LISTA DI UTENTI
        if choose == '!LIST':
            s.sendall(f'{nickname}:{choose}'.encode())
        #INVIO DI UN MESSAGGIO
        else:
            nickDest = input("Inserisci il nickname del destinatario: ")
            message = input("Inserisci il messaggio: ")
            msg = f'{nickname}:{nickDest}:{message}'.encode()
            s.sendall(msg)


if __name__ == "__main__":
    main()