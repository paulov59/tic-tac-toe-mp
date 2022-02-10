import socket
from _thread import *

# Iniciando variáveis globais
x = '0'
y = '0'
number_of_connections = 0
VEZ = '1'
jogador = '1'
ready = 0
vitoria = '0'

def threaded(conn):
    global number_of_connections, VEZ, x, y, ready, jogador, vitoria
    conn.send(str.encode('Início'))
    response = ' '

    while True:
        try:
            request = conn.recv(4096).decode('utf-8')
            request = request.split(' ')
            # op = código de operação enviado pelo cliente
            op = request[0]
            if op == "players":
                response = str(number_of_connections)
            # Operação de recebimento de jogadas
            elif op == "jogada":
                jogador = request[1]
                print(f"Jogador {jogador} fez uma jogada")
                x = request[2]
                y = request[3]
                if VEZ == '1':
                    VEZ = '2'
                elif VEZ == '2': 
                    VEZ = '1'
            # Atualizar os clients das jogadas realizadas
            elif op == "updatevez":
                if vitoria != "0":
                    response = f"venceu {vitoria}"
                elif request[1] != VEZ:
                    ready = 1
                    response = f"u {VEZ} {jogador} {x} {y}"
                else:
                    response = "OK"
            elif op == "vitoria":
                print(f"vitória do jogador {request[1]}")
                vitoria = request[1]

            conn.sendall(str.encode(response))
        except Exception as error:
            print('Error on server side!', error)
            break

    print("Connection Closed")
    conn.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_host = 'localhost'
    port = 8080
    server_adress = (server_host, port)

    try:
        server_socket.bind(server_adress) 

    except socket.error as error:
        print(str(error))

    server_socket.listen(2)
    print("Waiting for a connection")
    
    while True:
        conn, address = server_socket.accept()
        print("Connected to: ", address)
        global number_of_connections
        number_of_connections += 1
        start_new_thread(threaded, (conn,))

#--------------------------------------------------
main()
