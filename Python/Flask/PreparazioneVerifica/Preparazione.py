'''Utilizzando Python3, Flask e SQLite, progetta e implementa un server web dotato delle seguenti funzionalità:
Il server espone una pagina web in cui l’utente può inserire un indirizzo IP, un numero di porta minimo, un numero di porta massimo.
Non appena il server riceve tramite POST i dati inseriti dall’utente, effettua uno scan di porte TCP all’indirizzo ip indicato, per tutte le porte comprese tra numero di porta minimo e numero di porta massimo (ricorda il metodo connect_ex della libreria standard socket). Quando lo scan di porte è terminato, visualizza una pagina web con il messaggio “Port scan concluded”.
Il server ha un database sul quale memorizza tutti gli indirizzi IP scansionati e per ciascuno di essi le porte chiuse oppure aperte. Progettare adeguatamente il db e fare in modo che il server salvi in esso i risultati di tutte le scansioni.
'''

from flask import Flask, render_template, redirect, url_for, request
import sqlite3
import random, string
import socket as sck

app = Flask(__name__)
s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)  #creo un socket TCP / IPv4

#one table version
def insert(ip, port, scan):
    conn = sqlite3.connect('./db.db')
    cur = conn.cursor()

    #string=(f"INSERT INTO Memory (Ip, Port, Status) VALUES ('{ip}', {port}, 'OPEN')")

    if scan == 0:
        cur.execute(f"INSERT INTO Memory (Ip, Port, Status) VALUES ('{ip}', {port}, 'OPEN')")
    else:
        cur.execute(f"INSERT INTO Memory (Ip, Port, Status) VALUES ('{ip}', {port}, 'CLOSED')")

    cur.execute('commit')
    conn.close()


#two tables version
'''def check_duplicate(ip):
    conn = sqlite3.connect('./db2.db')
    cur = conn.cursor()

    cur.execute("SELECT Ip FROM IP_Table")
    rows = cur.fetchall()

    for row in rows:
        inserted_ip = row[0]
        if ip = inserted_ip:
            return False

    return

def insert(ip, port, scan, new):
    conn = sqlite3.connect('./db2.db')
    cur = conn.cursor()

    #string=(f"INSERT INTO Memory (Ip, Port, Status) VALUES ('{ip}', {port}, 'OPEN')")

    if new == True
        cur.execute(f"INSERT INTO IP_Table (Ip) VALUES ('{ip}')")
        if scan = 0:
            cur.execute(f"INSERT INTO Port_Table (Port, Status) VALUES ({port}, 'OPEN') WHERE ")
        else:
            cur.execute(f"INSERT INTO Port_Table (Port, Status) VALUES ({port}, 'CLOSED')")

    else:


    cur.execute('commit')
    conn.close()'''

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        ip = request.form['Indirizzo_ip']
        min_value = int(request.form['porta_minima'])
        max_value = int(request.form['porta_massima'])
        
        new = check_duplicate(ip)
        
        if max_value < min_value:
            error = 'Max value port must be higher than the Min one.'
            print('Max value port must be higher than the Min one.')
        else:
            for port in range(min_value, max_value+1):
                scan = s.connect_ex((ip, port))
                print(f'Port {port} of ip {ip}, status: {scan}')
                insert(ip, port, scan, new)

            return redirect(url_for('secret'))

    elif request.method == 'GET':
        return render_template('index.html')
    
    return render_template("index.html")

@app.route(f'/finished')
def secret():
    return "Port scan concluded"

if __name__== "__main__":
    app.run(debug=True)