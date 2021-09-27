from platform import system
from os import system as command

so = system()
tempo_espera = 2 #em segundos

def limpar_console():
    #limpa a tela do console de acordo com o sistema
    if so == 'Linux':
        command('clear')
    elif so == 'Windows':
        command('cls')
    else:
        print('\n' * 50)

    return None

def mostrar_menu(titulo:str, opcoes:str, min_:int, max_:int):
    # retorna a escolha do usuario
    while True:
        limpar_console()
        print('\t\t\t{}\n'.format(titulo))
        print(opcoes, end='\n\n')
        escolha = input('Opção: ').strip()
        try:
            escolha = int(escolha)
        except:
            print('Dado inválido (pressione ENTER)')
            input('')
            continue

        if escolha < min_ or escolha > max_:
            print('O valor selecionado não existe (pressione ENTER)')
            input('')
        else:
            return escolha

