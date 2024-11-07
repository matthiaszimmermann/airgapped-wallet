from web3 import Web3
import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv('RPC_URL')
# CONTRACT_ADDRESS = os.getenv('ERC20_CONTRACT_ADDRESS')
# SENDER_ADDRESS = sys.argv[1]
# RECIPIENT_ADDRESS = sys.argv[2] 
# AMOUNT_WEI = sys.argv[3]
RAW_TRANSACTION = sys.argv[1]

# print(f'RPC_URL: {RPC_URL}')


w3 = Web3(Web3.HTTPProvider(RPC_URL))
if not w3.is_connected():
    raise ConnectionError("Failed to connect to HTTPProvider")


tx_hash = w3.eth.send_raw_transaction(RAW_TRANSACTION)
print(tx_hash.hex())
