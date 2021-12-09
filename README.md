# Simulador de Sistema Bancário
Simula um sistema bancário em rede local através de sockets em um sistema do tipo cliente-servidor

Objetivo: Aprender conceitos de back-end tais como, crud, uso de threads, pacotes em python, gerenciamento de conexões, etc... Tudo com o objetivo de melhorar minha noção de server-side no início dos meus estudos sobre a área!

### Como funciona

O arquivo mainServer.py irá iniciar um servidor de onde as aplicações clientes podem se conectar e realizar operações bancárias entre contas cadastradas no sistema.

### Como usar

Com python intalado na sua máquina, inicie a aplicação mainServer.py no terminal com o comando:

```bash
$ python3 mainServer.py
```

Com a aplicação em execução, irá ser mostrada um IP e PORTA que devem ser colocados na aplicação do cliente.

Para executar o cliente use o comando:

```bash
$python3 cliente.py
```

O cliente pode ser usado em qualquer dispositivo da rede local que tenha python instalado.


A fazer no futuro:

- [ ] Mover esta aplicação para um módulo único chamado SSB_V1 e criar um novo módulo com a aplicação refatorada a cada ano. 
  * Objetivo: Reescrever a aplicação de acordo com minhas novas habilidades e ver a diferença em relação a anterior.
- [ ] Criar versao SSB_V3 1 ano após a SSB_V2 haver sido concluída.
