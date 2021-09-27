
conta = {'email': ops}
if conta:
    print(conta['email'])
    msg = conta['email'] + '|' + conta['nome'] + '|' + conta['saldo'] + '|' +'_'.join([i for i in conta['transacoes'])
    sessoes_ativas[ip]['con'].send(gtc.encode())