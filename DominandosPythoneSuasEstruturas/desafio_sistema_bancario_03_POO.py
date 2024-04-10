from abc import ABC 
from abc import abstractmethod
from datetime import datetime

class Cliente:

    def __init__(self, endereco:str) -> None:
        self._endereco = endereco
        self._contas = []

    @property
    def endereco(self):
        return self._endereco
    @endereco.setter
    def endereco(self,endereco:str):
        self._endereco = endereco
    
    @property
    def contas(self):
        return self._contas

    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
        
    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    '''
    Define uma pessoa atraves dos atributos cpf, nome e data
    '''
    def __init__(self, cpf:str,
                 nome:str,
                 data_nascimento:datetime,
                 endereco:str) -> None:
        super().__init__(endereco)
        self._cpf=cpf
        self._nome = nome
        self._data_nascimento = data_nascimento
    
    @property
    def cpf(self):
        return self._cpf
    
    @cpf.setter
    def cpf(self, cpf:str):
        self._cpf=cpf

    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self, nome:str):
        self._nome = nome
        
    @property
    def data_nascimento(self):
        return self._nome
    
    @data_nascimento.setter
    def data_nascimento(self, data_nascimento:datetime):
        self._data_nascimento = data_nascimento

    def __str__(self) -> str:
        return f'''
    Nome: {self._nome}
    CPF: {self._cpf}
    D. Nasci.: {self._data_nascimento}
    End.:{self.endereco}'''


class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

    @property
    @abstractmethod
    def valor(self)->float:
        pass

class Deposito(Transacao):
    def __init__(self, valor:float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self._valor):
            conta.historico.adicionar_transacao(self)
            print(f'(+)Deposito de: R${self._valor}')

                
class Saque(Transacao):
    def __init__(self, valor:float) -> None:
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self._valor):
            conta.historico.adicionar_transacao(self)
            print(f'(-)Saque de: R${self._valor}')

            

class Historico:
    def __init__(self) -> None:
        self._transacoes:list[str] = []
    
    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {#type:ignore
                'tipo':transacao.__class__.__name__,
                'valor':transacao.valor,
                'data':datetime.now().\
                    strftime('%d-%m-%Y %H:%M:%s')

            }
        )
        
    
class Conta:
    def __init__(self, numero:int,
                 cliente:PessoaFisica
                 ) -> None:
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()
    def saldo(self):
        return self._saldo
    @property
    def saldo(self):
        return self._saldo
    @property
    def numero(self):
        return self._numero
    @property
    def agencia(self):
        return self._agencia
    @property
    def cliente(self):
        return self._cliente
    @property
    def historico(self):
        return self._historico
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
        
    def _maior_que_zero(self,valor:float)->bool:
        if valor <= 0:
            print("Operação falhou! Valor menor que 0.")
            return False
        return True

    def _excedeu_saldo(self, valor:float)->bool:
        excedeu_saldo = valor > self._saldo
        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
            return True
        return False

    def sacar(self, valor:float)->bool:
        if not self._excedeu_saldo(valor) and self._maior_que_zero(valor):
            self._saldo -= valor
            return True
        return False

    def depositar(self, valor:float)-> bool:
        if self._maior_que_zero(valor):
            self._saldo += valor
            return True
        return False

    def __str__(self) -> str:
        return f'Ag.:{self._agencia}, N.:{self._numero} - Cl.: {self._cliente.nome}'
class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente: Cliente,
                 limite:float=500,
                 limite_saque:int=3) -> None:
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saque = limite_saque
    
    def _excedeu_limite(self, valor:float)->bool:
        excedeu_limite = valor > self._limite
        if excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")
            return True
        return False
    
    def _excedeu_saques(self,valor:float)-> bool:
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__]
        )
        excedeu_saques = numero_saques >= self._limite_saque
        if excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")
            return True
        return False
    
    def sacar(self, valor: float) -> bool:
        if not self._excedeu_limite(valor) and not self._excedeu_saques(valor):
            return super().sacar(valor)


    def __str__(self):
        return f'''
    Agencia:\t{self.agencia}
    C/C:\t {self.numero}
    Titular:\t{self.cliente} '''

def main():


    def imprimir_lista(lista):
        for index,item in enumerate(lista):
                print()
                print(f'N.: {index}')
                print(item)

    def escolher_da_lista(lista):
        while True:
            imprimir_lista(lista)
            try:
                valor = int(input('Escolha uma opcao =>> '))
            except:
                print('Valor invalido, tente novamente...')
                continue
            if valor < len(lista) and valor > -1: 
                break
            print('Valor invalido, tente novamente...')

        return valor
    def receber_valor():
        while True:
            try:
                valor = float(input('Digite um valor =>> '))
            except:
                print('Valor invalido!')
            if valor < 0:
                print('Valor invalido!')
                continue
            else:
                break

        return valor


    menu = '''
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Criar Conta Corrente
    [5] Cadastrar Usuário
    [6] Listar Contas
    [7] Listar Usuário
    [8] Sair
    '''
    contas_correntes:list[ContaCorrente] = []
    pessoas:list[PessoaFisica] = []
   
   #cadastrando usuarios para testes
    # pessoas.append(PessoaFisica('444.555.666-11',
    #                            'Carlos','22-07-1980',
    #                            'rua de baixo, 12'))
    # pessoas.append(PessoaFisica('123.432.123-11',
    #                            'bruno','24-01-1990',
    #                            'rua de cima, 123'))
    # contas_correntes.append(ContaCorrente(1,pessoas[0]))
    # contas_correntes.append(ContaCorrente(2,pessoas[0]))
    # contas_correntes.append(ContaCorrente(3,pessoas[1]))
    # transacao = Deposito(1000)
    # transacao.registrar(contas_correntes[0])
    # transacao = Deposito(140)
    # transacao.registrar(contas_correntes[0])
    # transacao = Deposito(500)
    # transacao.registrar(contas_correntes[1])
    # transacao = Deposito(10)
    # transacao.registrar(contas_correntes[1])
    # transacao = Deposito(300)
    # transacao.registrar(contas_correntes[2])



    while True:
        print(menu)
        opcao = input('Digite uma opcao=>> ')
        if opcao == '1':
            if len(contas_correntes)<1:
                print('Nao ha contas cadastradas')
                continue
            print('Selecione a Conta para qual deseja realizar a operacao')
            conta_index = escolher_da_lista(contas_correntes)
            valor = receber_valor()
            transacao = Deposito(valor)
            transacao.registrar(contas_correntes[conta_index])
            
        elif opcao == '2':
            if len(contas_correntes)<1:
                print('Nao ha contas cadastradas')
                continue
            print('Selecione a Conta para qual deseja realizar a operacao')
            conta_index = escolher_da_lista(contas_correntes)
            valor = receber_valor()
            transacao = Saque(valor)
            transacao.registrar(contas_correntes[conta_index])
            
        elif opcao == '3':
            if len(contas_correntes)<1:
                print('Nao ha contas cadastradas')
            else:
                conta_index = escolher_da_lista(contas_correntes)
                transacoes = contas_correntes[conta_index].historico.transacoes
                print('-'*80)
                print('TIPO'.center(20),'VALOR'.center(20),'Data'.center(20))
                for transacao in transacoes:
                    # print(transacao['tipo'])
                    print(str(transacao['tipo']).center(20),str(transacao['valor']).center(20),
                          str(transacao['data']).center(20))
                print('-'*80)
                print('Saldo : R$'.center(20),contas_correntes[conta_index].saldo)
                    
        elif opcao == '4':
            print('Cadastrando Conta corrente...')
            cliente_numero = escolher_da_lista(pessoas)
            numero_conta = len(contas_correntes) + 1
            nova_conta = ContaCorrente( #type:ignore
                numero_conta,
                pessoas[cliente_numero])
            contas_correntes.append(nova_conta)
            print('Cadastro realizado com sucesso!')

            
        elif opcao == '5':
            nome = input('Digite o nome: ')
            cpf = input('Digite o cpf: ')
            data_nascimento = input('Digite a Data de Nascimento: ')
            endereco = input('Digite o end: ')
            nova_pessoa = PessoaFisica(cpf,nome, data_nascimento, endereco)
            print(nova_pessoa)
            pessoas.append(nova_pessoa)
        elif opcao == '6':
            print(f'O banco de dados possue {len(contas_correntes)} registros')
            imprimir_lista(contas_correntes)
        elif opcao == '7':
            print(f'O banco de dados possue {len(pessoas)} registros')
            imprimir_lista(pessoas)

        elif opcao == '0':
            print('Saindo do sistema...')
            break
        else:
            print('Opcao invalida... Tente Novamente ou digite 0 para sair!')
         

if __name__ == '__main__':
    main()