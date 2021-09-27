import socket
import time

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(('10.0.0.117', 8080))

while True:
    req = input('Requisicao: ')
    if req == 'n':
        soc.close()
        break
    soc.send(req.encode())
    for i in range(10,0, -1):
        print(f'Aguardando resposta [ {i} ]')
        time.sleep(1)
        resposta = soc.recv(1024).decode()
        if resposta:
            print(resposta)
            break