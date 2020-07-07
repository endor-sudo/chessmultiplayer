import socket
import threading
import sys

server="192.168.8.101"
port=5555

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)

print("Waiting for a connection, Server Started")

players={0:'whites', 1:'blacks'}
last_move={0:'0', 1:'0'}

def client_thread(conn, player):
    conn.send(str.encode(players[player]))
    print(str(players[player])+'sent')
    reply=""
    
    while True:
        try:
            if player==0:
                reply=last_move[1]
            if player==1:
                reply=last_move[0]
            print('reply:')
            print(reply)
            conn.sendall(str.encode(reply))

            move= conn.recv(4096).decode('utf-8')
            print('move:')
            print(move)
            if move=='move':
                last_move[player] = conn.recv(4096).decode('utf-8')
                print('last_move[player]:')
                print(last_move[player])
        except Exception as e :
            print('client_thread')
            print(e)
            break
    
    print("Lost connection")
    conn.close()

current_player=0
while True:
    conn, addr=s.accept()
    print("Connected to:", addr)

    new_client=threading.Thread(target=client_thread, args=(conn,current_player))
    new_client.start()
    current_player+=1