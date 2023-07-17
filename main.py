from itertools import zip_longest
from typing import Any, Literal
import os, sys


class BankingSystem:
    def __init__(self) -> None:
        self.balance = 0
        self.bank_extract = {'withdraw': [], 'deposit': []}
        self.daily_withdraw_count = 3
        
        self.MIN_WITHDRAW = 1
        self.WITHDRAW_VALUE_DAILY_LIMIT = 500
        self.AGENCY_NUMBER = '0001'
        
        self.users = []
        self.accounts = []
        self.num_accounts = 0
        
        self.options = {
            '1': 'Sacar',
            '2': 'Depositar',
            '3': 'Ver extrato',
            '4': 'Criar novo usuário',
            '5': 'Criar conta corrente',
            '6': 'Listar contas',
            '7': 'Sair'
        }
        
    
    def withdraw(self, *, value: float) -> None:
        """Make the bank withdraw operation and register the operation on the
        extract of withdraws
        """ 
        if not isinstance(value, float):
            self.clear_terminal()
            return self.print_msg('Valor inválido, tente novamente.', 'warn')
        
        elif self.balance <= 0 or self.balance < value:
            self.clear_terminal()
            return self.print_msg('Saldo insuficiente!', 'warn')
        
        elif self.daily_withdraw_count <= 0:
            self.clear_terminal()
            return self.print_msg('Limite de retiradas excedido.', 'warn')
        
        elif value > self.WITHDRAW_VALUE_DAILY_LIMIT:
            self.clear_terminal()
            withdraw_day_limit_brl = self.to_brl(self.WITHDRAW_VALUE_DAILY_LIMIT)
            MSG = f'Valor máximo de retirada é de {withdraw_day_limit_brl}'
            return self.print_msg(MSG, 'warn')
        
        self.balance -= value
        self.bank_extract['withdraw'].append(value)
        self.daily_withdraw_count -= 1
        self.clear_terminal()
        self.print_msg('Saque efetuado com sucesso', 'success')
    
    def deposit(self, value: float,/) -> None:
        """Make the bank deposit operation and register in the deposit extract"""
        if not isinstance(value, float):
            self.clear_terminal()
            return self.print_msg('Valor inválido, tente novamente.', 'warn')
        
        if value < self.MIN_WITHDRAW:
            self.clear_terminal()
            msg = f'O deposito mínimo é de R${self.MIN_WITHDRAW:.2f}'
            return self.print_msg(msg, 'warn')
        
        self.balance += value
        self.bank_extract['deposit'].append(value)
        self.clear_terminal()
        self.print_msg('Deposito realizado com sucesso.', 'success')
    
    def show_extract(self, balance, /,*, extract) -> None:
        """show the extract from deposit and withdraws"""
        extracts = zip_longest(
            extract['withdraw'], extract['deposit'], fillvalue=' - '
        )
        self.clear_terminal()
        print(f"\nSALDO: {self.to_brl(balance)}")
        print('\nSAQUE', 'DEPÓSITO', sep='\t'.expandtabs(13))
        for wd, dp in extracts:
            print(f'{self.to_brl(wd)}\t{self.to_brl(dp)}'.expandtabs(20))
        
        
        print(f'\nSAQUES DISPONÍVEIS: {self.daily_withdraw_count}\n')
    
    def create_user(self, name: str, cpf: str, address: str, birth: str) -> None:
        if self.user_cpf_exists(cpf):
            self.clear_terminal()
            return self.print_msg('Usuário já possui conta.', 'error')
        
        self.users.append({'name': name, 'cpf': cpf, 'address': address, 'birth': birth})
        self.clear_terminal()
        self.print_msg('Usuário criado com sucesso.', 'success')
    
    def create_account(self, user_cpf: str, agency: str, number: int) -> dict:
        if not self.user_cpf_exists(user_cpf):
            self.clear_terminal()
            msg = 'cpf não esta atribuído a nenhum usuário do sistema.'
            return self.print_msg(msg, 'error')
        
        account = {'number': number, 'cpf': user_cpf, 'agency': agency}
        self.accounts.append(account)
        self.clear_terminal()
        self.print_msg('Conta criada com sucesso.', 'success')
        return account
    
    def user_cpf_exists(self, user_cpf: str) -> bool:
        """verify if user exists by cpf"""
        user = list(filter(lambda user: user.get('cpf') == user_cpf, self.users))
        if not user:
            return False
        
        return True
    
    def list_accounts(self):
        """list all accounts in the system"""
        if not self.accounts:
            self.clear_terminal()
            return print('Nenhuma conta registrada.')
        
        self.clear_terminal()
        for index, account in enumerate(self.accounts):
            if index > 0 and index < len(self.accounts):
                print()
                print('-' * 10)
                print()
                
            for k, v in account.items():
                print(f'{k}: {v}')
            
            print()
        
    def menu(self) -> str:
        """show the menu and return the user chosen option"""
        
        print('Banco'.center(20, '~'))
        for opt_num, opt_val in self.options.items():
            print(f'[{opt_num}] - {opt_val}')

        option = input('>>> ')
        return option
    
    def user_option_isvalid(self, option: str) -> bool:
        """Validate if the user option is correct.

        Args:
            option (str): the user option chosen

        Returns:
            bool: True if the option is valid.
        """
        if not option.isnumeric():
            return False
        
        if option not in self.options:
            return False
        
        return True
    
    @staticmethod
    def to_brl(value: float) -> str|Any:
        """convert a money value to BRL pattern
        
        Args:
            value (float): any money value
        
        Returns:
            str: the value converted to BRL pattern
            Any: the original value case can't be converted
        """
        try:
            return f'R${float(value):.2f}'
        except ValueError:
            return value
    
    @staticmethod
    def to_float(value) -> float | Any:
        """convert a value to float making treatments
        
        Args:
            value (Any): value to be converted
        
        Return:
            object converted to float if was converted successfully else return 
            the same object received
        """
        try:
            return float(value)
        except (TypeError, ValueError):
            return value
    
    @staticmethod
    def print_msg(msg: str, type: Literal['warn', 'error', 'success']) -> None:
        """print a message coloring by current type

        Args:
            msg (str): the message to be printed
            type (Literal[warn, error, success]): the type of the message
        """
        messages = {
            'warn': f'\033[33m{msg}\033[m',
            'error': f'\033[31m{msg}\033[m',
            'success': f'\033[32m{msg}\033[m'
            }
        print(messages[type])
    
    @staticmethod
    def clear_terminal() -> None:
        cmd = 'cls' if 'win' in sys.platform.lower() else 'clear'
        os.system(cmd)
    
    def run(self):
        while True:
            option = self.menu()
            if not self.user_option_isvalid(option):
                print('Opção invalida.')
                continue

            if self.options[option] == 'Sacar':
                withdraw_value = self.to_float(input('Valor de saque R$: '))
                self.withdraw(value=withdraw_value)
            
            elif self.options[option] == 'Depositar':
                deposit_value = self.to_float(input('Valor de depósito R$: '))
                self.deposit(deposit_value)
            
            elif self.options[option] == 'Ver extrato':
                self.show_extract(self.balance, extract=self.bank_extract)
            
            elif self.options[option] == 'Criar novo usuário':
                self.clear_terminal()
                name = input('Nome: ')
                birth = input('data de nascimento: ')
                address = input('Endereço: ')
                cpf = input('CPF: ')
                
                self.create_user(name, cpf, address, birth)
            
            elif self.options[option] == 'Criar conta corrente':
                cpf = input('CPF: ')
                acct = self.create_account(cpf, self.AGENCY_NUMBER, self.num_accounts + 1)
                if acct is not None:
                    self.num_accounts += 1
            
            elif self.options[option] == 'Listar contas':
                self.list_accounts()
            
            elif self.options[option] == 'Sair':
                break


if __name__ == '__main__':
    bank = BankingSystem()
    bank.run()
