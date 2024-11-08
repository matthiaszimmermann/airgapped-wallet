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
        parser = argparse.ArgumentParser(prog="enchanted_vault", description='Encrypted wallet manager')
        parser.add_argument('-p', '--password', help='password for the vault', type=str)
        parser.add_argument('-f', '--file', help='file to store the vault', type=str, default='vault.json')

        parser.add_argument('-g', '--generate', help='generate a new mnemonic and print it', action='store_true')
        parser.add_argument('-i', '--initialize', help='initialize a new vault and store in vault file', action='store_true')
        parser.add_argument('-a', '--address', help='print the address of the vault', action='store_true')

        self.args = parser.parse_args(args)
        
    def run_operations(self):
        if self.args.generate:
            self.generate()
        if self.args.initialize:
            self.check_preconditions_write()
            self.initialize()
        if self.args.address:
            self.check_preconditions_read()
            self.address()

    def check_preconditions_write(self):
        if os.path.exists(self.args.file):
            print(f'File exists: {self.args.file}')
            sys.exit(1)
        self.check_password()

    def check_preconditions_read(self):
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
        if os.path.exists(self.args.file):
            print(f'File exists: {self.args.file}')
            sys.exit(1)
            
        mnemo = Mnemonic("english")
        mnemonic = mnemo.generate(strength=128)
        account = Account.from_mnemonic(mnemonic)
        account_dict = account.encrypt(self.args.password)
        with open(self.args.file, 'w') as f:
            f.write(json.dumps(account_dict))
        
    # read the vault file, decrypt the account, and print the address
    def address(self):
        if not os.path.exists(self.args.file):
            print(f'File not found: {self.args.file}')
            sys.exit(1)
        
        with open(self.args.file, 'r') as f:
            account_dict = json.loads(f.read())
        account = Account.from_key(Account.decrypt(account_dict, self.args.password))
        print(account.address)
