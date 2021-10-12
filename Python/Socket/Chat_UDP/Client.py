'''
costruire una chat UDP che affronta il problema dell'invio di un messaggio da un utente ad un altro
gli utenti devono essere identificati tramite un identificatore univoco (es: nickname) 
ci sarà un server che genera dinamicamente un dizionario nickname:ip 
appena il client conosce il nickname manda un messaggio al server, così conosce anche l'ip tramite la recvfrom,
il server risponde con un OK 
hello = f"NICKNAME:{nickname}"
'''

import socket as sck, string, time
import threading as thr

BUFFER = 4096   #numero massimo di informazioni traslabili

class Receive_message(thr.Thread):
    def __init__(self, s):
        thr.Thread.__init__(self)   #costruttore super (java) 
        self.running = True
        self.s = s

    def run(self):
        while self.running:    
            data, addr = self.s.recvfrom(BUFFER)
            print(data.decode())

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)  #creo un socket UDP / IPv4

    #invio del nickname
    nickname = input("Inserisci il tuo nickname: ")
    msg = f'NICKNAME:{nickname}'.encode()
    s.sendto(msg, ('192.168.0.126', 5000))

    #attivazione chatmode
    data, addr = s.recvfrom(BUFFER)
    if data.decode()[0:2].upper() == 'OK':
        chatmode = True

    #thread per la ricezione dei messaggi
    receiver = Receive_message(s)
    receiver.start()

    while chatmode:
        nickDest = input("Inserisci il nickname del destinatario: ")
        message = input("Inserisci il messaggio: ")
        msg = f'{nickname}:{nickDest}:{message}'.encode()
        s.sendto(msg, ('192.168.0.126', 5000))


if __name__ == "__main__":
    main()