from eth_account import Account
import sys

# enable unaudited hdwallet features
Account.enable_unaudited_hdwallet_features()

# get mnemonic from command line (quoted or not) or stdin
if len(sys.argv) == 13:
    mnemonic = ' '.join(sys.argv[1:13])
elif len(sys.argv) > 1:
    mnemonic = sys.argv[1]
else:
    mnemonic = sys.stdin.read()

acct = Account.from_mnemonic(mnemonic.strip())
print(acct.address.strip())
