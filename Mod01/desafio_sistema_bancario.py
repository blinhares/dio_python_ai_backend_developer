menu = '''
[1]Depositar
[2]Sacar
[3]Extrato
[4]Sair
'''
extrato:list[float] = []
n_saques = 0
N_MAX_SAQUE = 3
V_MAX_SAQUE = 500

while True:
    print(menu)
    opcao = input('Digite uma opcao:')
    if opcao == '1':
        try:
            valor_deposito = float(input('Digite um valor a ser depositado: '))
        except:
            print('Valor invalido!\nRetornando ao Menu...')
            continue

        if valor_deposito > 0:
            extrato.append(valor_deposito)
            print(f'Valor de {valor_deposito} depositado com sucesso!')
        else:
            print('Valor invalido!')

        

    elif opcao == '2':
        try:
            valor_sacado = float(input('Digite um valor a ser sacado: '))
        except:
            print('Valor invalido!')
            continue
            
        #verifica se o valor é valido  
        if valor_sacado > 0:
        
            # verifica se ha saldo
            if sum(extrato) >= valor_sacado :

                # verifica se ha saques disponiveis
                if n_saques < N_MAX_SAQUE:
                    extrato.append(valor_sacado * -1)
                    print(f'Valor de {valor_sacado} sacado com sucesso!')
                    n_saques += 1

                else:
                    print('Número de Saques diários excedido!')

            else:
                print('Saldo indisponivel!')
        
        else:
            print('Valor invalido!')

        

    elif opcao == '3':
        print(' Seu Extrato '.center(25,'#'))
        print()
        for i in range(len(extrato)):
            print(f'{i} ----------- R${extrato[i]}')
        print(f'Saldo total : R${sum(extrato):.2f}')
   
    else:
        break

