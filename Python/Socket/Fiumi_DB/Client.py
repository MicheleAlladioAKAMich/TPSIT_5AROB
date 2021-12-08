'''
Author: Michele Alladio
es:
'''

import socket as sck
import string
import time
from datetime import datetime

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)  #creo un socket TCP / IPv4
    s.connect(('localhost', 7000))

    trasmissionDelay = float(input("Inserisci un delay di trasmissione dei dati: "))

    while True:
        stationId = input("Inserisci l'ID identificativo della stazione / exit per uscire: ")
        if stationId.upper() == 'EXIT':
            s.sendall('EXIT'.encode())
            break
        else:
            riverLevel = input("Inserisci il livello del fiume: ")

            message = f'{stationId}☺{riverLevel}☺{datetime.now()}'
            s.sendall(message.encode())

            data = s.recv(4096).decode()
            print(data)

            time.sleep(trasmissionDelay)
    
    s.close()
    exit()

if __name__ == "__main__":
    main()