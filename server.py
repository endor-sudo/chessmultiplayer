import socket
import threading

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
    global players
    global last_move
    conn.send(str.encode(players[player]))
    reply=""
    
    while True:
        try:
            if player==0:
                reply=last_move[1]
            if player==1:
                reply=last_move[0]

            conn.sendall(str.encode(reply))
            
            rec_move = conn.recv(4096).decode('utf-8')

            if rec_move!='':
                last_move[player]=rec_move
            else:
                last_move[player]='0'
                
        except Exception as e:
            break
    print("Lost connection")
    conn.close()

current_player=0
while True:
    if current_player>1:
        current_player=0
        players={0:'whites', 1:'blacks'}
        last_move={0:'0', 1:'0'}
    conn, addr=s.accept()
    print("Connected to:", addr)

    new_client=threading.Thread(target=client_thread, args=(conn,current_player))
    new_client.start()
    current_player+=1