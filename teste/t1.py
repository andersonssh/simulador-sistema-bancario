import socket
import time
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

c.bind(('0.0.0.0', 8080))


def mostrar(n, oq):
    print(oq)
    print(n)
    return n
for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)][0][1]:
    print(s)

print([mostrar(l, 'l') for l in ([mostrar(ip, 'ip') for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
c.listen()
conn, addr = c.accept()
print('Conexao aceita! {}:{}'.format(addr[0], addr[1]))
for i in range(10,0,-1):
    print(f'Aguarde! [ {i} ]')
    time.sleep(1)

print('recebendo dados')
print('-----dados-------')
print(conn.recv(1024).decode())
print('-----------------')

