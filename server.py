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

players={}
last_move={}

def client_thread(conn, player):
    conn.send(str.encode(players[player]))
    reply=""
    
    while True:
        try:
            if player%2==0:
                reply=last_move[player+1]
                print('player1: '+str(reply))
            elif player%2==1:
                reply=last_move[player-1]
                print('player2: '+str(reply))

            conn.sendall(str.encode(reply))
            
            rec_move = conn.recv(4096).decode('utf-8')

            if rec_move!='':
                last_move[player]=rec_move
            else:
                last_move[player]='0'
                
        except Exception as e:
            pass
    
    try:
        if player%2==0:
            del(players[player])
            del(last_move[player])
            del(players[player+1])
            del(last_move[player+1])
        elif player%2==1:
            del(players[player])
            del(last_move[player])
            del(players[player-1])
            del(last_move[player-1])
    except KeyError:
        pass

    print(players)
    print(last_move)
    print("Lost connection")

    conn.close()

current_player=0
while True:
    
    conn, addr=s.accept()

    if len(players)==0:
        current_player=0
    else:
        for _ in range(len(players)):
            for k in players.keys():
                if _ not in players:
                    if _+1 not in players:
                        current_player=_
                else:
                    if _+1 not in players:
                        current_player=_+1

    if current_player%2==0:
        players[current_player]='whites'
        last_move[current_player]='0'
    else:
        players[current_player]='blacks'
        last_move[current_player]='0'


    print("Connected to:", addr, "Current Player: ", current_player, 'players:', players, 'last move: ', last_move)

    new_client=threading.Thread(target=client_thread, args=(conn,current_player))
    new_client.start()