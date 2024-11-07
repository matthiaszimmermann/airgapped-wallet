from web3 import Web3
import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv('RPC_URL')
CONTRACT_ADDRESS = os.getenv('ERC20_CONTRACT_ADDRESS')
SENDER_ADDRESS = sys.argv[1]
RECIPIENT_ADDRESS = sys.argv[2] 
AMOUNT_WEI = sys.argv[3]

# print(f'RPC_URL: {RPC_URL}')


w3 = Web3(Web3.HTTPProvider(RPC_URL))
if not w3.is_connected():
    raise ConnectionError("Failed to connect to HTTPProvider")

with open('erc20.abi.json') as abi_file:
    contract_abi = json.load(abi_file)

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)
token_amount = w3.to_wei(AMOUNT_WEI, 'wei')  # Adjust the amount as needed
nonce = w3.eth.get_transaction_count(SENDER_ADDRESS)

transaction = contract.functions.transfer(RECIPIENT_ADDRESS, token_amount).build_transaction({
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

# print(str.encode(transaction))