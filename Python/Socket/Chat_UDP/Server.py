'''
costruire una chat UDP che affronta il problema dell'invio di un messaggio da un utente ad un altro
gli utenti devono essere identificati tramite un identificatore univoco (es: nickname) 
ci sarà un server che genera dinamicamente un dizionario nickname:ip 
appena il client conosce il nickname manda un messaggio al server, così conosce anche l'ip tramite la recvfrom,
il server risponde con un OK 
hello = f"NICKNAME:{nickname}"
'''

import socket as sck

BUFFER = 4096

def main():

    dictClient = {}
    tableNickname = []

    s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM) #creo un socket UDP / IPv4
    s.bind(('127.0.0.1', 7000)) 

    cnt = 0

    while True:
        data, addr = s.recvfrom(BUFFER)   #data = stringa ricevuta    addr -> tupla (IP client, porta client)

        if data.decode().startswith('NICKNAME'):
            nickname = data.decode().split(':')[-1] #split del nickname, prende la parte dopo i : 

            if nickname == '':  #se l'utente non mette un nickname --> guest0, guest1, guest2, ....
                nickname = f'guest{cnt}'    #guest1, guest2, guest3,....
                cnt+=1

            dictClient[nickname] = addr
            print(f'New user: {nickname}')

            #invio messagio per la chatmode
            msg = 'OK'.encode()
            s.sendto(msg, addr)

        
        else:
            #decodifica e split parti del messaggio
            mittente = data.decode().split(':')[0]
            destinatario = data.decode().split(':')[1]
            message = data.decode().split(':')[2]

            print(f'{mittente} send to {destinatario}: {message}')

            for nick, userAddr in dictClient.items():
                if destinatario == nick:
                    address = userAddr

            msg = f'Message from {mittente}: {message}'.encode()

            s.sendto(msg, address)

if __name__ == "__main__":
    main()

