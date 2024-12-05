import json

from util.html import HtmlUtility
from util.qr_code import QrCodeUtility
from web3.wallet import Wallet


class WalletPageUtility(HtmlUtility):
    VERSION = "0.1.0"
    REPOSITORY = "https://github.com/matthiaszimmermann/py-eth-wallet"

    TITLE = "Ethereum Paper Wallet"
    ETHEREUM_LOGO = "./util/ethereum_logo.png"

    CSS_CLEARFIX = "clearfix"
    CSS_ADDRESS_ROW = "address-row"
    CSS_COLUMN = "column"
    CSS_FILL = "fill-right"
    CSS_NOTES = "notes"
    CSS_CONTENT = "content"
    CSS_CAPTION = "caption"
    CSS_FOOTER = "footer-content"
    CSS_IMG_ADDRESS = "img-address"
    CSS_IMG_WALLET = "img-wallet"

    CSS_STYLES = [
        "html * { font-family:Verdana, sans-serif; }",
        f".{CSS_CLEARFIX}::after {{ content: \"\"; clear:both; display:table; }}",
        f".{CSS_ADDRESS_ROW} {{ background-color:#eef; }}",
        "@media screen {",
        f".{CSS_COLUMN} {{ float:left; padding: 15px; }}",
        f".{CSS_FILL} {{ overflow:auto; padding:15px; }}",
        f".{CSS_NOTES} {{ height:256px; background-color:#fff; }}",
        f".{CSS_CONTENT} {{ padding:15px; background-color:#efefef; font-family:monospace; }}",
        f".{CSS_CAPTION} {{ margin-top:6px; font-size:smaller;}}",
        f".{CSS_FOOTER} {{ font-size:small; }}",
        f".{CSS_IMG_ADDRESS} {{ display:block; height:256px; }}",
        f".{CSS_IMG_WALLET} {{ display:block; height:400px }}",
        "}",
        "@media print {",
        f".{CSS_COLUMN} {{ float:left; padding:8pt; }}",
        f".{CSS_FILL} {{ overflow:auto; padding:8pt; }}",
        f".{CSS_NOTES} {{ height:100pt; border-style:solid; border-width:1pt; }}",
        f".{CSS_CONTENT} {{ background-color:#efefef; font-family:monospace; font-size:6pt }}",
        f".{CSS_CAPTION} {{ margin-top:2pt; font-size:smaller;}}",
        f".{CSS_FOOTER} {{ font-size:6pt; }}",
        f".{CSS_IMG_ADDRESS} {{ display:block; height:100pt; }}",
        f".{CSS_IMG_WALLET} {{ display:block; height:180pt }}",
        "}",
    ]


    @staticmethod
    def create_html(wallet: Wallet) -> str:
        html = []

        # Header
        HtmlUtility.add_open_elements(html, HtmlUtility.HTML, HtmlUtility.HEAD)
        HtmlUtility.add_title(html, WalletPageUtility.TITLE)
        HtmlUtility.add_styles(html, " ".join(WalletPageUtility.CSS_STYLES))
        HtmlUtility.add_close_elements(html, HtmlUtility.HEAD)

        # Body
        HtmlUtility.add_open_elements(html, HtmlUtility.BODY)
        HtmlUtility.add_header2(html, WalletPageUtility.TITLE)

        # Add first row
        HtmlUtility.add_open_div(html, WalletPageUtility.CSS_CLEARFIX, WalletPageUtility.CSS_ADDRESS_ROW)

        # Ethereum logo
        HtmlUtility.add_open_div(html, WalletPageUtility.CSS_COLUMN)
        logo = WalletPageUtility.get_file_bytes(WalletPageUtility.ETHEREUM_LOGO)
        HtmlUtility.add_encoded_image_bytes(html, logo, 256, WalletPageUtility.CSS_IMG_ADDRESS)
        HtmlUtility.add_close_div(html)

        # Account address
        HtmlUtility.add_open_div(html, WalletPageUtility.CSS_COLUMN)
        address_qr_code = QrCodeUtility.content_to_png_bytes(wallet.address, 256)
        HtmlUtility.add_encoded_image_bytes(html, address_qr_code, 256, WalletPageUtility.CSS_IMG_ADDRESS)
        HtmlUtility.add_paragraph(html, "QR Code Address", WalletPageUtility.CSS_CAPTION)
        HtmlUtility.add_close_div(html)

        # Notes
        HtmlUtility.add_open_div(html, WalletPageUtility.CSS_FILL)
        HtmlUtility.add_open_div(html, WalletPageUtility.CSS_NOTES)
        HtmlUtility.add_close_div(html)
        HtmlUtility.add_paragraph(html, "Notes", WalletPageUtility.CSS_CAPTION)
        HtmlUtility.add_close_div(html)

        HtmlUtility.add_close_div(html)

        # Add second row
        HtmlUtility.add_open_div(html, WalletPageUtility.CSS_CLEARFIX)

        # # QR code for wallet file
        vault_file_content = json.dumps(wallet.vault)
        HtmlUtility.add_open_div(html, WalletPageUtility.CSS_COLUMN)
        wallet_qr_code = QrCodeUtility.content_to_png_bytes(vault_file_content, 400)
        HtmlUtility.add_encoded_image_bytes(html, wallet_qr_code, 400, WalletPageUtility.CSS_IMG_WALLET)
        HtmlUtility.add_paragraph(html, "QR Code Wallet File", WalletPageUtility.CSS_CAPTION)
        HtmlUtility.add_close_div(html)

        # Address, passphrase, wallet file, file name
        HtmlUtility.add_open_div(html, WalletPageUtility.CSS_FILL)
        WalletPageUtility.add_wallet_details(html, wallet, vault_file_content)
        # WalletPageUtility.add_wallet_details(html, wallet)
        HtmlUtility.add_close_div(html)

        # Add footer content
        footer = f"Page created with EPW Generator [{WalletPageUtility.REPOSITORY}] V {WalletPageUtility.VERSION}"
        HtmlUtility.add_open_footer(html, WalletPageUtility.CSS_FOOTER)
        HtmlUtility.add_content(html, footer)
        HtmlUtility.add_close_footer(html)

        HtmlUtility.add_close_elements(html, HtmlUtility.BODY, HtmlUtility.HTML)

        return "".join(html)


    @staticmethod
    def add_wallet_details(html, wallet, vault_file_content):
        details = [
            (wallet.address, "Address"),
            (wallet.mnemonic, "Mnemonic"),
            (wallet.path, "BIP 44 Path"),
            (wallet.pass_phrase, "Pass Phrase"),
            (vault_file_content.replace(",\"", ", \""), "Vault File"),
        ]

        for content, caption in details:
            HtmlUtility.add_paragraph(html, caption, WalletPageUtility.CSS_CAPTION)
            HtmlUtility.add_open_div(html, WalletPageUtility.CSS_CONTENT)
            HtmlUtility.add_content(html, content)
            HtmlUtility.add_close_div(html)


    @staticmethod
    def get_file_bytes(file_path):
        try:
            with open(file_path, "rb") as file:
                return file.read()
        except Exception as e:
            raise RuntimeError(f"Failed to read file: {file_path}") from e
