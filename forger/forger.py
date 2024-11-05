from mnemonic import Mnemonic

def main():
    mnemo = Mnemonic("english")
    random_seed = mnemo.generate(strength=128)
    print(random_seed)
    print(mnemo.to_seed(random_seed))


if __name__ == '__main__':
    main()
