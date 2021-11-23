'''
Author: Michele Alladio
es:
'''

import socket as sck
import string
import threading as thr
import time

operations = [] #lista delle operazioni

class Receive_message(thr.Thread):
    def __init__(self, s):
        thr.Thread.__init__(self)   #costruttore super (java) 
        self.running = True
        self.s = s

    def run(self):
        while self.running:
            data = self.s.recv(4096).decode()

            if data == 'exit':  #chiusura del client
                self.running = False
            else:   #creazione della lista con le operazioni
                print(f"Messaggio ricevuto: {data}")
                operations.append(data)


def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)  #creo un socket TCP / IPv4
    s.connect(('localhost', 7000))

    #Thread per la ricezione dei messaggi
    receiver = Receive_message(s)
    receiver.start()

    time.sleep(2)   #tempo di attesa per evitare errori 

    for operation in operations:    #creazione della prima parte della string di output con un carattere di split
        string = f'{operation} = {eval(operation)}☺'
        s.sendall(string.encode())
    
    time.sleep(5)   #tempo di attesa per evitare errori 

    if not receiver.running:    #chiusura del client una volta finito il suo compito
        s.close()
        receiver.join()
        exit()


if __name__ == "__main__":
    main()