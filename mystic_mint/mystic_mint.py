import argparse
from web3 import Web3
import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()


class MysticMint:

    def parse_args(self, args):
        parser = argparse.ArgumentParser(prog="mystic_mint.py", description='Create and transmit ERC20 transactions')
        parser.add_argument('-e', '--erc20-contract', help='the address of the erc20 contract', type=str)
        parser.add_argument('-s', '--sender', help='the sender address', type=str)
        parser.add_argument('-r', '--recipient', help='the recipient address', type=str)
        parser.add_argument('-aw', '--amount-wei', help='the amount to transfer (in wei)', type=int)
        # parser.add_argument('-a', '--amount', help='the amount to transfer', type=float)
        parser.add_argument('-tx', '--transaction', help='the signed transaction to submit', type=str)

        parser.add_argument('-c', '--create', help='create a transaction', action='store_true')
        parser.add_argument('-t', '--submit', help='submit the transaction', action='store_true')

        self.args = parser.parse_args(args)
        
        self.RPC_URL = os.getenv('RPC_URL')
        if not self.args.erc20_contract:
            self.args.erc20_contract = os.getenv('ERC20_CONTRACT_ADDRESS')

    def run_operations(self):
        if self.args.create:
            self.create()
        if self.args.submit:
            self.submit()
        
    def create(self):
        w3 = Web3(Web3.HTTPProvider(self.RPC_URL))
        if not w3.is_connected():
            raise ConnectionError("Failed to connect to HTTPProvider")

        if os.path.exists('erc20.abi.json'):
            with open('erc20.abi.json') as abi_file:
                contract_abi = json.load(abi_file)
        else:
            if os.path.exists('mystic_mint/erc20.abi.json'):
                with open('mystic_mint/erc20.abi.json') as abi_file:
                    contract_abi = json.load(abi_file)

        if not contract_abi:
            raise FileNotFoundError("Failed to load contract ABI from file erc20.abi.json")


        contract = w3.eth.contract(address=self.args.erc20_contract, abi=contract_abi)
        token_amount = w3.to_wei(self.args.amount_wei, 'wei')  # Adjust the amount as needed
        nonce = w3.eth.get_transaction_count(self.args.sender)

        transaction = contract.functions.transfer(self.args.recipient, token_amount).build_transaction({
            'chainId': w3.eth.chain_id,
            'gas': 77000,  # Adjust the gas limit as needed
            # 'gasPrice': w3.eth.gas_price,  # Adjust the gas price as needed or use w3.eth.generate_gas_price()
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })

        # print(transaction)
        # print(Web3.to_bytes(Web3.to_json(transaction)))
        tx_json = json.dumps(transaction)
        print(tx_json)

    def submit(self):
        w3 = Web3(Web3.HTTPProvider(self.RPC_URL))
        if not w3.is_connected():
            raise ConnectionError("Failed to connect to HTTPProvider")

        if not self.args.transaction:
            raise ValueError("No transaction provided")

        signed_transaction = self.args.transaction
        tx_hash = w3.eth.send_raw_transaction(signed_transaction)
        print(f"Transaction hash: {tx_hash.hex()}")
