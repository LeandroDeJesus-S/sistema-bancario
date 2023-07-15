from itertools import zip_longest
from sys import platform
import os
import time


class BankingSystem:
    def __init__(self) -> None:
        self.balance = 0
        self.bank_withdraw_statement = []
        self.bank_deposit_statement = []
        self.daily_withdraw_count = 3
        
        self.MIN_WITHDRAW = 1
        self.WITHDRAW_VALUE_DAILY_LIMIT = 500
    
    def run(self):
        """the main function of the program"""
        print(
f""" 
SALDO: {self.to_brl(self.balance)}
SAQUES DISPONÍVEIS: {self.daily_withdraw_count}

[1] Sacar
[2] Depositar
[3] Ver extrato
[4] Sair
"""
        )
        option = input('>>> ')
        options = {
            '1': self.withdraw,
            '2': self.deposit,
            '3': self.show_extract,
            '4': quit
        }
        
        try:
            return options[option]()
        
        except KeyError:
            print('Opção invalida, tente novamente!')
        
        except ValueError:
            print('Por favor, insira um valor válido.')
    
    def withdraw(self) -> None:
        """Make the bank withdraw operation and register the operation on the
        extract of withdraws
        """
        value = float(input('Valor: R$'))
        
        if self.balance <= 0 or self.balance < value:
            return print('Saldo insuficiente!')
        
        elif self.daily_withdraw_count <= 0:
            return print('Limite de retiradas excedido.')
        
        elif value > self.WITHDRAW_VALUE_DAILY_LIMIT:
            MSG = f'Valor máximo de retirada é de R${self.WITHDRAW_VALUE_DAILY_LIMIT:.2f}'
            return print(MSG)
        
        self.balance -= value
        self.bank_withdraw_statement.append(value)
        self.daily_withdraw_count -= 1
    
    def deposit(self) -> None:
        """Make the bank deposit operation and register in the deposit extract"""
        value = float(input('Valor: R$'))
        
        if value < self.MIN_WITHDRAW:
            return print(f'O deposito mínimo é de R${self.MIN_WITHDRAW:.2f}')
        
        self.balance += value
        self.bank_deposit_statement.append(value)
    
    def show_extract(self):
        """show the extract from deposit and withdraws"""
        extracts = zip_longest(self.bank_withdraw_statement, 
                               self.bank_deposit_statement,
                               fillvalue=' - ')
        
        
        print('\nSAQUE', 'DEPÓSITO', sep='\t'.expandtabs(13))
        for wd, dp in extracts:
            print(f'{self.to_brl(wd)}\t{self.to_brl(dp)}'.expandtabs(20))
        
        input('\nPressione Enter para continuar...')
    
    def to_brl(self, value: float) -> float:
        """convert a money value to BRL pattern"""
        try:
            return f'R${float(value):.2f}'
        except ValueError:
            return value


if __name__ == '__main__':
    banking_system = BankingSystem()
    
    clean_cmd = 'cls' if 'win' in platform else 'clear'
    
    while True:
        time.sleep(1.5)
        os.system(clean_cmd)
        
        banking_system.run()
