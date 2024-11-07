from mnemonic import Mnemonic
from eth_account import Account
import sys

# enable unaudited hdwallet features
Account.enable_unaudited_hdwallet_features()

def main():
    if (len(sys.argv) >= 2):
        password = sys.argv[1]
    if (len(sys.argv) < 2):
        password = sys.stdin.read().strip()
    mnemo = Mnemonic("english")
    mnemonic = mnemo.generate(strength=128)
    # seed = mnemo.to_seed(mnemonic)
    # print(seed.hex())
    account = Account.from_mnemonic(mnemonic)
    # print(account._private_key.hex())
    print(account.encrypt(password))



if __name__ == '__main__':
    main()
