import json
from typing import Tuple

from util.wallet_page import WalletPageUtility
from web3.wallet import Wallet


class WalletFile:

    EXT_HTML:str = "html"
    EXT_JSON:str = "json"
    INDENT:int = 4

    wallet:Wallet = None
    path:str = None
    file_name_base:str = None
    html:str = None


    def __init__(self, wallet:Wallet):
        self.wallet = wallet
        self.html = WalletPageUtility.create_html(wallet)
        self.file_name_base = self.wallet.address


    def save(self, path:str=None):

        base_name = self.get_base_name(path)

        with open(f"{base_name}.{self.EXT_HTML}", 'w') as file:
            file.write(self.html)

        with open(f"{base_name}.{self.EXT_JSON}", 'w') as file:
            file.write(
                self.get_vault_file())


    def get_base_name(self, path:str) -> str:
        if not path:
            self.path = "."
        else:
            self.path = path

        if self.path.endswith("/"):
            self.path = self.path[:-1]

        return f"{self.path}/{self.file_name_base}"


    def get_wallet_file(self) -> str:
        return self.html


    def get_vault_file(self) -> str:
        return json.dumps(self.wallet.vault, indent=self.INDENT)
