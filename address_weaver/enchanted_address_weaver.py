from eth_account import Account
import sys
import json

# enable unaudited hdwallet features
Account.enable_unaudited_hdwallet_features()

# get mnemonic from command line (quoted or not) or stdin
if len(sys.argv) == 3:
    encrypted_pk = sys.argv[1]
    password = sys.argv[2]
else:
    encrypted_pk = sys.stdin.read()
    password = sys.stdin.read()

pk = Account.decrypt(encrypted_pk.replace("'", "\""), password)
acct = Account.from_key(pk)
print(acct.address.strip())
