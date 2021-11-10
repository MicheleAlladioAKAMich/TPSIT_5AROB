'''
Author: Michele Alladio, Filippo Ferrando
es:
'''

import socket as sck, string, time

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)  #creo un socket TCP / IPv4
    s.connect(('192.168.0.122', 7002))
    #s.connect(('localhost', 7002))

    print("COMANDI:\n-1 --> avanti\n-2 --> indietro\n-3 --> sinistra\n-4 --> destra\n-5 --> stop\n-6 --> zig-zag")

    while True:
        command = input().upper().encode()

        s.sendall(command)

    '''try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()'''

if __name__ == '__main__':
    main()