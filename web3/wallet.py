# from mnemonic import Mnemonic
from eth_account import Account
from eth_account.types import Language

class Wallet:

    WORDS = 12
    LANGUAGE = Language.ENGLISH
    ACCOUNT_PATH = "m/44'/60'/0'/0/0"

    pass_phrase: str = None
    vault: dict = None
    mnemonic: str = None
    address: str = None
    account: Account = None
    language: str = None
    path: str = None
    index: int = None


    def __init__(
        self, 
        pass_phrase:str="",
        mnemonic:str=None,
        num_words:int=WORDS,
        language:Language=LANGUAGE, 
        account_path=ACCOUNT_PATH,
        index:int=None
    ):
        Account.enable_unaudited_hdwallet_features()

        if index is not None and index >= 0:
            account_path = account_path[:-1] + str(index)
        else:
            index = 0

        if mnemonic and len(mnemonic.split()) >= 12:
            self.account = Account.from_mnemonic(
                mnemonic, 
                pass_phrase, 
                account_path)
        else:
            (
                self.account, 
                self.mnemonic
            ) = Account.create_with_mnemonic(
                pass_phrase, 
                num_words, 
                language, 
                account_path)

        self.vault = self.account.encrypt(pass_phrase)
        self.pass_phrase = pass_phrase
        self.address = self.account.address
        self.language = language
        self.path = account_path
        self.index = index
