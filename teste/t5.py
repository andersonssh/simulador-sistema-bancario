import ipaddress

ip = '10.0.0.1'

endereco = ipaddress.ip_address(ip)

#a biblioteca permite fazer eperacoes com o endereco gerado
print(endereco + 100)
print(endereco + 1000)


#trabalhando com redes


ip1 = '192.0.0.0/24'


rede = ipaddress.ip_network(ip1)

print(rede)


#como o ip2 nao é o endereco de uma rede, com o strict = False, ele diz a qual rede o ip pertence

ip2 = '192.168.0.1/24'

print(ipaddress.ip_network(ip2, strict=False))

#lista todos os ips de uma mesma rede
for ip in rede:
    print(ip)

#nesta linha, o stric=False pode ajudar pois ele ira identificar a que rede
#determinado ip inserido pertence, e ira fazer o processo
#lembrando que a mascra de rede /24 diz que,
#um endereco tera 24 bits (8 digitos), para
#identificar a rede e 8 para servir como identificador de um host
# for ip in ipaddress.ip_network(ip2):
#     print(ip)