import socket

a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

a.connect(('10.0.0.117', 8080))

a.send(b'O SERVIDOR NAO PRECISA ESTAR EXECUTANDO UM RECV NO EXATO MOMENTO PARA RECEBER A MENSAGEM')

a.close()