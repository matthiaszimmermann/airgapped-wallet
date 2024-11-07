from eth_account import Account
import sys
import json

# enable unaudited hdwallet features
Account.enable_unaudited_hdwallet_features()

# get mnemonic from command line (quoted or not) or stdin
if len(sys.argv) != 4:
    print("Usage: python3 transmuter.py <encrypted_pk> <password> <raw_transaction>")
    print(len(sys.argv))
    sys.exit(1)

encrypted_pk = sys.argv[1]
password = sys.argv[2]
raw_transaction = sys.argv[3]

pk = Account.decrypt(encrypted_pk, password)
acct = Account.from_key(pk)

signed_tx = acct.sign_transaction(json.loads(raw_transaction))
print(signed_tx.raw_transaction.hex())
