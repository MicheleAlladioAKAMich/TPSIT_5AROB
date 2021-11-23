import socket as sck
import threading as thr
import sqlite3
from sqlite3 import Error
import time

clientList = [] #lista dei client
dizOperations = {}  #dizionario delle operazioni --> chiave = id univoco del client ||| valore = lista delle operazioni

class Client_Manager(thr.Thread):
    def __init__(self, address, connection, identification):
        thr.Thread.__init__(self)   #costruttore super (java)
        self.connection = connection
        self.identification = identification
        self.address = address
        self.running = True
    
    def run(self):
        
        for operation in dizOperations[self.identification]:    #lista di operazioni che riguardano questo thread
            self.connection.sendall(operation.encode()) #invio delle operazioni con un delay di 0.5 secondi
            time.sleep(0.5)
        
        time.sleep(3)   
        results = self.connection.recv(4096).decode()[:-1].split('☺')  #ricezione della stringa dei risultati dopo 3 secondi

        for result in results:  #stampa dei risultati dopo l'esecuzione della split sul carattere speciale
            print(f'{result} from {self.address[0]} - {self.address[1]}')   #prima parte della stringa creata nel client + seconda parte creata localmente
        
        self.connection.sendall('exit'.encode())    #il thread ha concluso il suo compito --> viene chiuso
        self.running = False


#CONNESSIONE AL DB
def create_connection(db_file): #funzione per connettere il database allo script
    conn = None
    try:
        conn = sqlite3.connect(db_file) #attiva la connessione al db
    except Error as e: #gestione dell'errore
        print(e)

    return conn


#RICERCA DEL NUMERO DI CLIENT UTILIZZANDO UNA QUERY SUL DB
def maxClient(conn):
    cur = conn.cursor()        
    cur.execute(f"SELECT MAX(client) FROM operations") #query per ricercare il numero di client
    nClient = cur.fetchall()

    for client in nClient:
        return client[0]    #numero di client

#ESTRAZIONE DELLE OPERAZIONI DAL DB
def select_task_id(conn, id):
    operationsList = [] #lista di operazioni associata a ciascun client
    
    cur = conn.cursor()      
    cur.execute(f"SELECT operation FROM operations Where client = {id}") #ogni operazione che ha come client il client identificato tramite l'id univoco

    rows = cur.fetchall()

    for row in rows:
        operationsList.append(row[0])   #creazione della lista di operazioni per quel client
    return operationsList


def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.bind(("127.0.0.1", 7000))
    s.listen()

    global clientList, dizOperations
    identification = 0  #numero identificativo (uno per ogni client)

    connDb = create_connection("./operations.db")
    clientNumber = maxClient(connDb)    #numero massimo di client

    for id in range (1, clientNumber+1):    #per ogni client vengono estrapolate le sue operazioni dal DB
        operationsList = select_task_id(connDb, id)
        dizOperations[id] = operationsList  #aggiornamento dizionario delle operazioni

    while True:
        connection, address = s.accept()

        identification+=1   #incremento del numero identificativo del client
        if identification > clientNumber:   #se il numero dei client supera quello massimo riinizia da 1
            identification = 1

        print(f'Thread number: {identification}')   #DEBUG

        #creazione del thread -> uno per ogni client
        client = Client_Manager(address, connection, identification)
        clientList.append(client)
        client.start()

        for client in clientList:   #controllo per le chiusure dei client
            if not client.running:
                if connDb != None:  #se esiste il database viene chiuso
                    connDb.close()
                client.join()  
                clientList.remove(client)

if __name__ == "__main__":
    main()