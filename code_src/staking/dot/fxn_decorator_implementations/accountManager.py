import json
import sys
from bip39 import bip39_validate
# TODO: can you confirm the below github for the substrateinterface library?
from substrateinterface import Keypair # github: https://github.com/polkascan/py-substrate-interface
from substrateinterface.exceptions import SubstrateRequestException
from config import activeConfig
from Logger import myLogger


"""
Generic class for executing account related calls for DOT
The following calls are made to this class:
* All calls in accountingArgParser.py (mnemonic, keypair, info, create)
"""
class DotAccountCall:
    def __init__(self, mnemonic="", ss58_address=""):
        self.cli_name = "Accounting"
        self.mnemonic = mnemonic
        self.ss58_address = ss58_address
        self.logger = myLogger(self.cli_name)
        self.logger.info("Start %s Program." % self.cli_name)

    def createMnemonic(self):
        mnemonic = Keypair.generate_mnemonic()
        createMnemonicLogMessage = f"""create mnemonic phrase

    mnemonic : {mnemonic}

    note : please write down this mnemonic in paper and stored in a save place.
    learn more about mnemonic : https://coinmarketcap.com/alexandria/glossary/mnemonic-phrase
            """
        try:
            self.logger.info(createMnemonicLogMessage)
            return mnemonic
        except Exception as e:
            self.logger.critical(f"error : {e}")
            return False

    def getAccountInfos(self, ss58_address):
        try:
            value = activeConfig.activeSubstrate.query('System', 'Account', params=[ss58_address]).value
            fee_frozen = int(value['data']['fee_frozen']) / activeConfig.coinDecimalPlaces
            free = int(value['data']['free']) / activeConfig.coinDecimalPlaces
            reserved = int(value['data']['reserved']) / activeConfig.coinDecimalPlaces
            misc_frozen = int(value['data']['misc_frozen']) / activeConfig.coinDecimalPlaces

            self.logger.info(f"""account {ss58_address} infos

    nonce : {value['nonce']}
    consumers : {value['consumers']}
    providers : {value['providers']}
    sufficients : {value['sufficients']}
    free : {free} {activeConfig.coinName}
    reserved : {reserved} {activeConfig.coinName}
    misc_frozen : {misc_frozen} {activeConfig.coinName}
    fee_frozen : {fee_frozen} {activeConfig.coinName}
    """)
        except Exception as e:
            self.logger.error(f"{e}")

    def createAccount(self) -> json:
        createAccountMnemonic = self.createMnemonic()
        createAccountKeyPair = dotCreateKeyPair(self.logger, createAccountMnemonic)
        # check if mnemonic is created if this pass keypair will pass without errors
        if not createAccountKeyPair:
            return False
        return True

    def __call__(self, func):
        name = func.__name__
        if name == "mnemonic":
            self.createMnemonic()
        elif name == "create":
            self.createAccount()
        elif name == "info":
            self.getAccountInfos(self.ss58_address)
        elif name == "keypair":
            dotCreateKeyPair(self.logger, mnemonic=self.mnemonic)
        else:
            pass

def dotCreateKeyPair(logger, mnemonic):
    invalidCharacters = "[@_!#$%^&*()<>?/|}{~:]0123456789"

    # If a mnemonic is not passed in, the default in the above library will be used
    # however, we will enforce that "something" is passed in to avoid the default (len 10 is arbitrary)
    if (len(mnemonic) < 10):
            logger.critical("A bad mnemonic as been passed to create the keypair")
            return False

    try:
        # Keypair ~ https://github.com/polkascan/py-substrate-interface#keypair-creation-and-signing
        key = Keypair.create_from_mnemonic(mnemonic=mnemonic, ss58_format=activeConfig.ss58_format)
        logger.info(f"""create key pair\n\n
    {key}
     \n\n""")

        # do a quick verification that the key signs normally
        if key.verify("This is a test message", key.sign("This is a test message")):
            return key
        else:
            # if the key verification fails, exit immediatly
            logger.critical("\nDO NOT USE KEY. KEY INCORRECTLY GENERATED.\n")
            return False

    except ValueError:
        # more thorough check for the mnemonic below

        # split mnemonic by space into words
        splitMnemonic = mnemonic.split(" ")

        lengthMnemonic = len(splitMnemonic)
        # check word length and special character
        lengthWordInMnemonic = any(word for word in splitMnemonic if len(word) < 3 or len(word) > 8)
        lengthOfDigitInMnemonicIfAny = any(s for s in mnemonic if s in invalidCharacters)

        # Checking mnemonic length
        # length doesn't meet the standard
        if lengthMnemonic not in [12, 15, 18, 21, 24]:
            logger.critical(
                "Number of words must be one of the following: [12, 15, 18, 21, 24], but it is not (%d)."
                % lengthMnemonic)
            return False

        # length meet the standard
        else:
            # Checking mnemonic for invalid characters (non alphabet)
            if lengthOfDigitInMnemonicIfAny:
                logger.critical("Mnemonic words must be alphabet words.")
                return False

            # check word len in mnemonic min = 2 max = 8 or the mnemonic doesn't have valid word
            elif lengthWordInMnemonic or not bip39_validate(mnemonic):
                logger.critical("Please check for messing strings.")
                return False


