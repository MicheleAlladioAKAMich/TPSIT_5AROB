#libreries
from flask import Flask, render_template, redirect, url_for, request, make_response
import sqlite3
from sympy import *
from datetime import datetime
import semaforo

app = Flask(__name__)
sem = semaforo.semaforo()

#global state for the stoplight
STATO = "ATTIVO" #"SPENTO"

GREEN = 0
YELLOW = 0
RED = 0

'''
PROFILE RECOVERY AND COMPARISON
Using a specific query, the validity of the user's credentials is checked.
If not so, the programme will raise an error
'''
def validate(username, password):
    conn = sqlite3.connect("./db.db")
    completion = False  
    cur = conn.cursor()
    cur.execute("SELECT * FROM AUTHORIZED_USERS")
    rows = cur.fetchall()

    #extraction of credentials from the database
    for row in rows:
        dbUser = row[0]
        #print(dbUser)
        dbPass = row[1]
        #print(dbPass)
        if dbUser == username:
            completion = check_password(dbPass, password)   #completion always set to True
    return completion 
    conn.close()

def check_password(hashed_password, user_password): #not yet implemented...
    return hashed_password == user_password

'''
INSERT VALUES
Using a specific query each login is always saved in the database with the time when this occurred.
'''
def login_log(user):
    conn = sqlite3.connect("./db.db")
    cur = conn.cursor()
    #query for saving informations
    cur.execute(f"INSERT INTO LOGIN (USER, DATE) VALUES ('{user}', '{datetime.today()}')")
    cur.execute("commit")
    conn.close()

'''
INSERT VALUES
Using a specific query each stoplight's change of state is always saved in 
the database with the user who made it and the time when this occurred.
'''
def insert(username, state):
    conn = sqlite3.connect("./db.db")
    cur = conn.cursor()

    cur.execute(f"INSERT INTO OPERATIONS_HISTORY (User, Operation, Date) VALUES ('{username}', '{state}', '{datetime.today()}')")

    cur.execute('commit')
    conn.close()

'''
LOGIN
Each user must log in before change settings. Not all users can log in.
Using coockies the programme will save into a database users who change the state of the stoplight.
'''
@app.route('/', methods=['GET', 'POST'])
def Login():
    error = None
    if request.method == 'POST':
        #taking user's credentials
        username = request.form['username']
        #print(username)
        password = request.form['password']
        #print(password)
        completion = validate(username, password)   #validating user's credentials
        #raise of an error if the user isn't allowed to log in
        if completion == False: 
            error = 'Invalid Credentials. Please try again.'
            print(error)
        else:
            login_log(username)
            print(f'{username} logged successfully!')
            #redirect to the settings page
            resp = make_response(redirect(url_for('Settings')))
            #cookie setting
            resp.set_cookie('username', username)
            return resp
    return render_template('Login.html', error=error)   #raise of an error

'''
REINDIRIZZAMENTO
Users who are allowed to log in can also change stoplight's settings.
The fields allow users to change the duration of each light and the status of the traffic light.
'''
@app.route(f'/Settings', methods=['GET', 'POST'])
def Settings():
    global STATO, GREEN, YELLOW, RED
    error = None
    if request.method == 'POST':
        #taking settings
        verde = request.form['verde']
        giallo = request.form['giallo']
        rosso = request.form['rosso']
        state = request.form['state']
        #print(STATO)
        username = request.cookies.get('username')  #cookie

        if(state != ""):
            if(state=="ATTIVO" or state=="SPENTO"):
                insert(username, state) #insertion of the change of state in the appropriate database
                STATO = state   #change of state
            else:   #raise of an error if state is not allowed
                error = "State MUST be ATTIVO or SPENTO!, state will be setted in reference to the previous state"
                print(error)

        #changing lights duration
        if(verde!=""):
            GREEN = verde
        if(giallo!=""):
            YELLOW = giallo
        if(rosso!=""):
            RED = rosso
            
        resp = make_response(redirect(url_for('test'))) #redirect to the test page
        return resp

    return render_template('Settings.html', error=error)

#ESEMPIO di pagina di test
@app.route('/test')
def test():
    if STATO == "ATTIVO":
        #Esempio di sequenza con semaforo attivo. I tempi devono essere
        #modificabili dalla pagina di configurazione!
        sem.rosso(int(RED))
        sem.verde(int(GREEN))
        sem.giallo(int(YELLOW))
    else:
        #Esempio di sequenza con semaforo spento. I tempi devono essere
        #modificabili dalla pagina di configurazione!
        for _ in range(3):
            sem.giallo(1)
            sem.luci_spente(1)
    return 'TEST ESEGUITO!'

if __name__== "__main__":
    app.run(debug=True) #auto-debug