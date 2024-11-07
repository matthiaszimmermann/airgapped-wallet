from mnemonic import Mnemonic

def main():
    mnemo = Mnemonic("english")
    mnemonic = mnemo.generate(strength=128)
    print(mnemonic)



if __name__ == '__main__':
    main()
