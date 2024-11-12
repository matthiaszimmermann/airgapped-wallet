import sys

from mystic_mint import MysticMint


def main():
    vault = MysticMint()
    vault.parse_args(sys.argv[1:])
    vault.run_operations()


if __name__ == '__main__':
    main()
