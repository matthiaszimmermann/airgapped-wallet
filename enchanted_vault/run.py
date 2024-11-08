import sys
from enchanted_vault import EnchantedVault


def main():
    vault = EnchantedVault()
    vault.parse_args(sys.argv[1:])
    vault.run_operations()


if __name__ == '__main__':
    main()
    