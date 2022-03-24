'''
Una web app per calcolare gli integrali

Realizzate una web app così costituita:
pagina di login che permetta all’utente di accedere alla pagina di calcolo;
pagina di calcolo nella quale l’utente possa indicare
una funzione f(x) (stringa) e i due estremi di integrazione: la pagina deve calcolare l’integrale definito
una funzione f(x) (stringa): la pagina deve calcolare l’integrale indefinito
DB sqlite3 nel quale memorizzare gli utenti e i calcoli di integrali effettuati con le loro soluzioni.
NOTA: utilizzare https://docs.sympy.org/latest/tutorial/calculus.html#integrals per il calcolo degli integrali

BONUS:
Implementate i cookies, in modo da poter salvare sul DB un registro degli integrali calcolati da ogni utente.
'''

from flask import Flask, render_template, redirect, url_for, request, make_response
import sqlite3
import random, string
import socket as sck
from sympy import *
from datetime import datetime

app = Flask(__name__)
s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)  #creo un socket TCP / IPv4

'''
RECUPERO DELLA DESCRIZIONE
utilizzando un'apposita query viene controllata la validità delle credenziali dell'utente
'''
def validate(username, password):
    conn = sqlite3.connect("./db.db")
    completion = False
    cur = conn.cursor()
    cur.execute("SELECT * FROM AUTHORIZED_USERS")
    rows = cur.fetchall()
    for row in rows:
        dbUser = row[0]
        #print(dbUser)
        dbPass = row[1]
        #print(dbPass)
        if dbUser == username:
            completion = check_password(dbPass, password)
    return completion
    conn.close()

def check_password(hashed_password, user_password):
    return hashed_password == user_password

def login_log(user):
    conn = sqlite3.connect("./db.db")
    cur = conn.cursor()
    cur.execute(f"INSERT INTO LOGIN (USER, DATE) VALUES ('{user}', '{datetime.today()}')")
    cur.execute("commit")
    conn.close()

#one table version
'''
INSERIMENTO DEI VALORI NEL DATABASE
Attraverso un apposita query si vanno ad inserire i dati nel database.
Tra i dati troviamo lo username, l'integrale, i possibili estremi ed il risultato
'''
def insert(username, integral, estMin, estMax, result):
    conn = sqlite3.connect("./db.db")
    cur = conn.cursor()

    cur.execute(f"INSERT INTO OPERATIONS_HISTORY (User, Integral, EstMin, EstMax, Result) VALUES ('{username}', '{integral}', '{estMin}', '{estMax}', '{result}')")

    cur.execute('commit')
    conn.close()

'''
LOGIN
Inserimento dati dell'utente, creazione cookies e reindirizzamento alla pagina di calcolo
'''
@app.route('/', methods=['GET', 'POST'])
def Login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        #print(username)
        password = request.form['password']
        #print(password)
        completion = validate(username, password)
        if completion == False:
            error = 'Invalid Credentials. Please try again.'
            print(error)
        else:
            login_log(username)
            print(f'{username} logged successfully!')
            resp = make_response(redirect(url_for('Calculator')))
            resp.set_cookie('username', username)
            return resp
    return render_template('Login.html', error=error)

'''
REINDIRIZZAMENTO
Se l'utente è valido viene reindirizzato su un apposito 
sito per il calcolo degli integrali, il quale scinde gli integrali definiti da quelli indefiniti
'''
@app.route(f'/Calculator', methods=['GET', 'POST'])
def Calculator():
    error = None
    x = symbols('x')
    if request.method == 'POST':
        integral = request.form['integral']
        estMax = request.form['estMax']
        estMin = request.form['estMin']
        username = request.cookies.get('username')

        #controllo del tipo di integrale
        if estMax == '' or estMin == '':
            result = integrate(integral, x)
        else:
            result = integrate(integral, (x, estMax, estMin))

        insert(username, integral, estMin, estMax, result)

    return render_template('Calculator.html', error=error)
    


if __name__== "__main__":
    app.run(debug=True) #auto-debug