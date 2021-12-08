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

    while True:

        interrogation = int(input("LISTA DELLE OPZIONI:\n-1: chiedere al server se un certo nome file è presente\n-2: chiedere al server il numero di frammenti di un file a partire dal suo nome file\n-3: chiedere al server l’IP dell’host che ospita un frammento a partire nome file e dal numero del frammento\n-4: chiedere al server tutti gli IP degli host sui quali sono salvati i frammenti di un file a partire dal nome file\n-5: terminare la connessione\n"))
            
        #SCELTA DEL FORMATO DEL MESSAGGIO DA MANDARE IN BASE ALL'INTERROGAZIONE SCELTA
        if interrogation == 1 or interrogation == 2 or interrogation == 4:
            fileName = input("Inserisci il nome del file: ")
            message = f'{fileName}☺{str(interrogation)}'
            s.sendall(message.encode())
        
        elif interrogation == 3:
            fileName = input("Inserisci il nome del file: ")
            fragmentNumber = input("Inserisci il numero del frammento: ")
            message = f'{fileName}☺{fragmentNumber}☺{str(interrogation)}'
            s.sendall(message.encode())
        
        elif interrogation == 5:    #chiusura del client
            s.sendall('EXIT'.encode())
            break

        #RICEZIONE DATI
        data = s.recv(4096).decode()
        print(data)

        time.sleep(2)   #tempo di attesa tra le interrogazioni
    
    s.close()
    exit()

if __name__ == "__main__":
    main()