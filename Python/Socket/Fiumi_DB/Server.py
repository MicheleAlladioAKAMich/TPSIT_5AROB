import socket as sck
import threading as thr
import sqlite3
from sqlite3 import Error
import time

clientList = [] #lista dei client
dizStations = {}  #dizionario delle stazioni

class Client_Manager(thr.Thread):
    def __init__(self, address, connection):
        thr.Thread.__init__(self)   #costruttore super (java)
        self.connection = connection
        self.address = address
        self.running = True
    
    def run(self):
        connDb = create_connection("./fiumi.db")  
        while self.running:
            data = self.connection.recv(4096).decode().split('☺')  #ricezione della stringa dei risultati dopo 3 secondi

            if data[0] == 'EXIT':
                self.running = False
                if connDb != None:  #se esiste il database viene chiuso
                    connDb.close()

            else:
                stationId = int(data[0])
                level = int(data[1])
                date = data[2]

                fiume, localita, livello = select_station_id(connDb, stationId)

                if fiume == '-':
                    self.connection.sendall('\nSpiacenti, non esiste questa stazione di misurazione.\n'.encode())
                elif level < (int(livello)*30)/100:
                    self.connection.sendall('\nRicezione avvenuta, grazie per la segnalazione!\n'.encode())
                elif level >= (int(livello)*30)/100 and level < (livello*70)/100:
                    self.connection.sendall('\nRicezione avvenuta, grazie per la segnalazione!\n'.encode())
                    print(f'AVVISO IMMINENTE, LIVELLO DEL {fiume} SITUATO A {localita}\nlivello:{level}, data e ora: {date}\n')
                else:
                    self.connection.sendall('\nRICHIESTA DI ATTIVAZIONE DELLA SIRENA LUMINOSA!\n'.encode())
                    print(f'PERICOLO IN CORSO, LIVELLO DEL {fiume} SITUATO A {localita}\nLivello:{level}, data e ora: {date}\n')

#CONNESSIONE AL DB
def create_connection(db_file): #funzione per connettere il database allo script
    conn = None
    try:
        conn = sqlite3.connect(db_file) #attiva la connessione al db
    except Error as e: #gestione dell'errore
        print(e)

    return conn

#ESTRAZIONE DELLE OPERAZIONI DAL DB
def select_station_id(conn, id):
    operationsList = [] #lista di operazioni associata a ciascun client
    
    cur = conn.cursor()      
    cur.execute(f"SELECT fiume, localita, livello FROM livelli Where id_stazione = {id}") #ogni operazione che ha come client il client identificato tramite l'id univoco

    rows = cur.fetchall()
    if rows == []:
        return '-', '-', '-'
    else:
        for row in rows:
            return row[0], row[1], row[2]


def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.bind(("127.0.0.1", 7000))
    s.listen()

    global clientList, dizOperations
    identification = 0  #numero identificativo (uno per ogni client)

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