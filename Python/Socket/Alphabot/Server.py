'''
Author: Michele Alladio
es:'''

import socket as sck

def main():

    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM) 
    s.bind(('localhost', 7000)) 

    s.listen()
    conn, addr = s.accept()
    print(f"Connessione avvenuta con: {addr}")

    while True:
       
        data = conn.recv(4096).decode()  
        print(data)   

    s.close()    
    
if __name__ == "__main__":
    main()