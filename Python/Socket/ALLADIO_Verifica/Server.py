import socket as sck
import threading as thr
import sqlite3
from sqlite3 import Error
import time

clientList = [] #lista dei client

class Client_Manager(thr.Thread):
    def __init__(self, address, connection):
        thr.Thread.__init__(self)   #costruttore super (java)
        self.connection = connection
        self.address = address
        self.running = True
    
    def run(self):
        connDb = create_connection("./file.db")  
        while self.running:
            data = self.connection.recv(4096).decode().split('☺')  #ricezione, decodifica e split dell'interrogazione
            if data[0] == 'EXIT':   #chiusura del thread
                self.running = False
                if connDb != None:  #se esiste il database viene chiuso
                    connDb.close()

            elif len(data) == 2:    #interrogazioni in cui l'unico parametro è il nome del file

                fileName = data[0]
                queryNumber = int(data[1])

                if queryNumber == 1:
                    existentFile = execute_query_id(connDb, queryNumber, fileName, -1)  #esecuzione query, -1 per convenzione in termine di distinzione dalla query numero 3
                    if existentFile == None:    #se il file non esiste
                        self.connection.sendall('\nIl file non esiste!\n'.encode())
                    else:
                        self.connection.sendall(f'\nFile {fileName}: file esistente\n'.encode())

                elif queryNumber == 2:
                    fragmentsNumber = execute_query_id(connDb, queryNumber, fileName, -1)   #esecuzione query
                    if fragmentsNumber == None: #se il file non esiste
                        self.connection.sendall('\nNon è possibile stabilire il numero di frammenti: il file non esiste!\n'.encode())
                    else:
                        self.connection.sendall(f'\nNumero di frammenti del file {fileName}: {fragmentsNumber}\n'.encode())
                
                elif queryNumber == 4:
                    ipList = execute_query_id(connDb, queryNumber, fileName, -1)    #esecuzione query 
                    if ipList == None:  #se il file non esiste
                        self.connection.sendall("\nNon è possibile stabilire l'ip degli hosts: il file non esiste!\n".encode())
                    else:
                        self.connection.sendall(f'\nLista degli ip degli hosts del file {fileName}: {ipList}\n'.encode())

            elif len(data) > 2: #interogazione in cui i parametri sono nome del file e id del frammento
                fileName = data[0]
                fragmentId = int(data[1])
                queryNumber = int(data[2])

                host = execute_query_id(connDb, queryNumber, fileName, fragmentId)

                if host == None:
                    self.connection.sendall("\nNon è possibile stabilire l'ip dell'host: il file non esiste oppere non esiste quel frammento nel file!\n".encode())
                else:
                    self.connection.sendall(f'\nHost del frammento {fragmentId} del file {fileName}: {host}\n'.encode())

#CONNESSIONE AL DB
def create_connection(db_file): #funzione per connettere il database allo script
    conn = None
    try:
        conn = sqlite3.connect(db_file) #attiva la connessione al db
    except Error as e: #gestione dell'errore
        print(e)

    return conn

#ESTRAZIONE DELLE OPERAZIONI DAL DB
def execute_query_id(conn, queryNumber, fileName, fragmentId):

    cur = conn.cursor()
    fileName = f"'{fileName}'"  #aggiungo gli apici a fileName per un confronto nella query

    if fragmentId == -1:    #interrogazioni numero 1, 2 e 4
        if queryNumber == 1:
            cur.execute(f"SELECT nome FROM files Where nome = {fileName}")
            rows = cur.fetchall()

            for row in rows:
                return row[0]
        
        elif queryNumber == 2:
            cur.execute(f"SELECT tot_frammenti FROM files Where nome = {fileName}")
            rows = cur.fetchall()

            for row in rows:
                return row[0]
                
        elif queryNumber == 4:
            hostsList = []

            cur.execute(f"SELECT host FROM frammenti, files Where frammenti.id_file = files.id_file AND nome = {fileName}")
            rows = cur.fetchall()
            
            if rows == []:
                return None #non siste il file
            else:
                for row in rows:
                    hostsList.append(row[0])
                return hostsList
    
    else:   #interrogazione numero 3
        cur.execute(f"SELECT host FROM frammenti, files Where frammenti.id_file = files.id_file AND n_frammento = {fragmentId} AND nome = {fileName}")
        rows = cur.fetchall()

        for row in rows:
            return row[0]

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.bind(("127.0.0.1", 7000))
    s.listen()

    global clientList

    while True:
        connection, address = s.accept()

        #creazione del thread --> uno per ogni client
        client = Client_Manager(address, connection)
        clientList.append(client)
        print(f'{client}: Connessione avvenuta\n')
        client.start()

        for client in clientList:   #controllo per le chiusure dei client
            if not client.running:
                print(f'{client}: Disconnessione in corso...\n')
                client.join()  
                clientList.remove(client)

if __name__ == "__main__":
    main()