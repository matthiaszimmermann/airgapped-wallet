import argparse
import getpass
import json
import os
import sys

from eth_account import Account
from mnemonic import Mnemonic

Account.enable_unaudited_hdwallet_features()

class EnchantedVault:

    def parse_args(self, args):
        parser = argparse.ArgumentParser(prog="enchanted_vault.py", description='Encrypted wallet manager')
        parser.add_argument('-g', '--generate', help='generate a new mnemonic and print it', action='store_true')
        parser.add_argument('-i', '--initialize', help='initialize a new vault and store in vault file', action='store_true')
        parser.add_argument('-a', '--address', help='print the address of the vault', action='store_true')
        parser.add_argument('-s', '--sign-transaction', help='sign a transaction', action='store_true')

        parser.add_argument('-p', '--password', help='vault password', type=str)
        parser.add_argument('-f', '--file', help='vault file', type=str, default='vault.json')
        parser.add_argument('-if', '--input-file', help='input ', type=str)
        parser.add_argument('-of', '--output-file', help='output ', type=str)

        parser.add_argument('transaction_data', help='transaction data', type=str, nargs='?')


        self.args = parser.parse_args(args)
        
    def run_operations(self):
        if self.args.generate:
            self.generate()
        if self.args.initialize:
            self.initialize()
        if self.args.address:
            self.address()
        if self.args.sign_transaction:
            self.sign_transaction()

    def check_preconditions_write_vault(self):
        if os.path.exists(self.args.file):
            print(f'File exists: {self.args.file}')
            sys.exit(1)
        self.check_password()

    def check_preconditions_read_vault(self):
        if not os.path.exists(self.args.file):
            print(f'File not found: {self.args.file}')
            sys.exit(1)
        self.check_password()

    def check_password(self):
        if not self.args.password:
            self.args.password = getpass.getpass('Password: ')
        if not self.args.password:
            print('Password required')
            sys.exit(2)
    
    # generate a new mnemonic and print it to the console
    def generate(self):
        mnemo = Mnemonic("english")
        mnemonic = mnemo.generate(strength=128)
        print(mnemonic)
    
    # generate a new random mnemonic, encrypt it with the password, and store it in the vault file
    def initialize(self):
        self.check_preconditions_write_vault()
        
        mnemo = Mnemonic("english")
        mnemonic = mnemo.generate(strength=128)
        account = Account.from_mnemonic(mnemonic)
        account_dict = account.encrypt(self.args.password)
        with open(self.args.file, 'w') as f:
            f.write(json.dumps(account_dict))
        
    # read the vault file, decrypt the account, and print the address
    def address(self):
        self.check_preconditions_read_vault()
            
        with open(self.args.file, 'r') as f:
            account_dict = json.loads(f.read())
        account = Account.from_key(Account.decrypt(account_dict, self.args.password))
        print(account.address)

    def sign_transaction(self):
        if not self.args.transaction_data and not os.path.exists(self.args.input_file):
            print('Transaction data required. Use --input-file or provide as argument')
            sys.exit(3)
        if self.args.output_file and os.path.exists(self.args.output_file):
            print(f'Output file exists: {self.args.output_file}')
            sys.exit(4)

        self.check_preconditions_read_vault()

        # read and decrypt wallet
        with open(self.args.file, 'r') as f:
            account_dict = json.loads(f.read())
        account = Account.from_key(Account.decrypt(account_dict, self.args.password))

        # read transaction
        with open(self.args.input_file, 'r') as f:
            transaction = json.loads(f.read())
        
        # sign and write transaction
        signed_tx = account.sign_transaction(transaction)
        if self.args.output_file:
            with open(self.args.output_file, 'w') as f:
                f.write(signed_tx.raw_transaction.hex())
        else:
            print(signed_tx.raw_transaction.hex())
        
        