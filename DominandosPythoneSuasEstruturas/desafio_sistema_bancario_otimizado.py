from typing import Any
#criar func 
# [c] Cadastrar Usuário
# [b] Criar Conta Corrente

saldo:float = 0
limite:float = 500
extrato:str = ""
numero_saques:int = 0
LIMITE_SAQUES:int = 3

usuarios:list = []
contas:list = []

def cadastro_usuario(usuarios:list)-> list:
    """
    Cadastra um Novo usuario ao sistema

    Args:
        usuarios (list): _description_

    Returns:
        list: lista de usuarios atualizada
    """
    
    novo_usuario:dict[Any] = {
                    'Nome':None,
                    'Data Nascimento':None,
                    'C.P.F.':None,
                    'Endereco':{
                        'Logradouro':None,
                        'Numero':None,
                        'Bairro':None,
                        'Cidade': None,
                        'UF':None
                    }
                     }
    print('Cadastro de Novo Usuário...')
    for prim_key in novo_usuario:

        if prim_key == 'C.P.F.':
            while novo_usuario[prim_key] == None:
                try:
                    novo_usuario[prim_key] = int(input(f'Insira o {prim_key}: '))
                except:
                    print('Valor invalido, favor digitar somente numeros...\nEx.: 1231434')
                    print()

                
                
                #se existe um valor valido de cpf
                if isinstance(novo_usuario[prim_key], int) :
                    #verificar se cpf ja existe
                    for user in usuarios:
                        if user[prim_key] == novo_usuario[prim_key]:
                            print(f'CPF em conflito com o Usuario : ', user.get('Nome') )
                            print('Tente um CPF diferente')
                            novo_usuario[prim_key] = None
                            break #sai do for
                        
        elif prim_key == 'Endereco':
            for key in novo_usuario["Endereco"].keys():
                novo_usuario["Endereco"][key] = input(f'Insira o {key}: ')
            continue

        else:
            novo_usuario[prim_key] = input(f'Digite o {prim_key}: ')
    
    usuarios.append(novo_usuario)

    return usuarios

def listar_usuarios(usuarios:list) -> bool:
    """Lista os Usuarios

    Args:
        usuarios (list): Lista contendo os usuarios

    Returns:
        bool: retorna True se existem usuarios
    """
    if len(usuarios)<1:
        print('Não ha usuarios para ser exibidos...')
        return False
    
    print('Lista de Usuários:')
    for i in range(len(usuarios)):
        print(
            f'{i} - ',
            usuarios[i].get('Nome'),
            ' - ',
            usuarios[i].get('C.P.F.'))
    return True



def cadastro_conta(contas:list, usuarios:list)-> list:
    """Cadastra contas com base nos dados dos usuarios

    Args:
        contas (list): lista contendo as contas
        usuarios (list): lista contendo usuarios

    Returns:
        list: retorna a lista de contas atualizada
    """
    nova_conta = {
        'Agencia': '0001',
        'Número da Conta':None,
        'Usuário':None,
        'Saldo':0,
        'extrato':'',
        'numero_saques':0
    }
    #se nao tem usuarios retorna contas sem modificar
    if not listar_usuarios(usuarios):
        return contas
    
    while True:
        try:
            usuario_cpf = usuarios[int(input('Selecione um Usuario:'))].\
                get('C.P.F.') #type:ignore
            break
        except:
            print('Insira um numero Valido')

        listar_usuarios(usuarios)
    #criando usuario
    nova_conta['Número da Conta'] = len(contas) + 1
    nova_conta['Usuário'] = usuario_cpf
    contas.append(nova_conta)
    return contas

def listar_contas(contas:list)->bool:
    """Lista os Usuarios

    Args:
        contas (list): Lista contendo as contas

    Returns:
        bool: retorna True se existem contas
    """
    if len(contas)<1:
        print('Não ha contas para ser exibidos...')
        return False
    
    print('Lista de Contas:')
    for i in range(len(contas)):
        print('Ordem'.center(6),'Número da Conta'.center(20),'Usuário'.center(15),'Saldo'.center(20) )
        print(
            f'{i+1}'.center(6),
            str(contas[i].get('Número da Conta')).center(20),
            str(contas[i].get('Usuário')).center(15),
            str(contas[i].get('Saldo')).center(20),
            )
    return True
    
def coletar_conta(contas = contas)->int:
    """Coletar conta

    Args:
        contas (list): lista de contas. Defaults to contas.

    Returns:
        int: retorna a posicao da lista de contas. 
        Conta 01 - retorno -> 0
        Conta 02 - retorno -> 1
    """
    while True:
        listar_contas(contas)
        print('Selecione uma conta => ')
        try:
            n_conta = int(input())
            if n_conta > 0:
                contas[n_conta-1]
                return n_conta - 1
            
        except:
            print('Número da Conta invalida, tente novamente...')
            

def saque(*, valor:float, saldo:float, limite:float, numero_saques:int, extrato:str)->tuple[float,int,str]:
    """Funcao Saque

    Args:
        valor (float): Valor solicitado para saque.
        saldo (float): Saldo atual do cliente
        limite (float): Limite de saque do cliente
        numero_saques (int): Numero de saques realizados
        extrato (str): Extrato do cliente

    Returns:
        saldo, numero_saques, extrato
    """

    excedeu_saldo = valor > saldo

    excedeu_limite = valor > limite

    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1

    else:
        print("Operação falhou! O valor informado é inválido.")

    return (saldo, numero_saques, extrato)

def saque_from(n_conta:int, valor:float):
    saldo = contas[n_conta]['Saldo']
    numero_saques = contas[n_conta]['numero_saques']
    extrato = contas[n_conta]['extrato']

    saldo, numero_saques, extrato = saque(valor=valor,
                                     saldo=saldo,
                                     limite=limite,
                                     numero_saques= numero_saques,
                                     extrato=extrato)
    

def deposito(valor:float, saldo:float, extrato:str,/):
    if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"

    else:
        print("Operação falhou! O valor informado é inválido.")

    return (saldo, extrato)

def mostrar_extrato(saldo:float,/, *, extrato:str):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[u] Cadastrar Usuário / [ul] Listar Usuarios
[c] Criar Conta Corrente / [cl] Listar Contas
[q] Sair

=> """


while True:

    opcao = input(menu)

    if opcao == "d":
        n_conta = coletar_conta()
        
        valor = float(input("Informe o valor do depósito: "))

        contas[n_conta]['Saldo'],contas[n_conta]['extrato'] = deposito(
                                            valor,
                                            contas[n_conta]['Saldo'],
                                            contas[n_conta]['extrato'])

    elif opcao == "s":
        n_conta = coletar_conta()

        valor = float(input("Informe o valor do saque: "))

        saldo = contas[n_conta]['Saldo']
        numero_saques = contas[n_conta]['numero_saques']
        extrato = contas[n_conta]['extrato']

        saldo, numero_saques, extrato = saque(valor=valor,
                                     saldo=saldo,
                                     limite=limite,
                                     numero_saques= numero_saques,
                                     extrato=extrato)
        
        contas[n_conta]['Saldo'] = saldo
        contas[n_conta]['numero_saques'] = numero_saques
        contas[n_conta]['extrato'] = extrato
        


    elif opcao == "e":
        n_conta = coletar_conta()

        mostrar_extrato(contas[n_conta]['Saldo'],
                        extrato=contas[n_conta]['extrato'])
    
    elif opcao == "u":
        usuarios = cadastro_usuario(usuarios)

    elif opcao == "ul":
        listar_usuarios(usuarios)

    elif opcao == "c":
        contas = cadastro_conta(contas, usuarios)

    elif opcao == "cl":
        listar_contas(contas)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
