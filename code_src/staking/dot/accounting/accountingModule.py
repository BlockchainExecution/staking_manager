import json

from bip39 import bip39_validate

from Logger import myLogger
from substrateinterface import Keypair


class Accounting(object):
    def __init__(self):
        self.name = "Accounting"
        self.logger = myLogger(self.name)
        self.logger.info("Starting accounting Program.")
        self.invalidCharacters = "[@_!#$%^&*()<>?/|}{~:]0123456789"

    def createMnemonic(self):
        mnemonic = Keypair.generate_mnemonic()
        createMnemonicLogMessage = f"""\n
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

    def createKeypair(self, mnemonic):
        try:
            key = Keypair.create_from_mnemonic(mnemonic)
            self.logger.info(key)
            return key
        except ValueError:
            # split mnemonic by space into words
            splitMnemonic = mnemonic.split(" ")

            lengthMnemonic = len(splitMnemonic)
            # check word length and special character
            lengthWordInMnemonic = any(word for word in splitMnemonic if len(word) < 3 or len(word) > 8)
            lengthOfDigitInMnemonicIfAny = any(s for s in mnemonic if s in self.invalidCharacters)

            # Checking mnemonic length
            # length doesn't meet the standard
            if lengthMnemonic not in [12, 15, 18, 21, 24]:
                self.logger.critical(
                    "Number of words must be one of the following: [12, 15, 18, 21, 24], but it is not (%d)."
                    % lengthMnemonic)
                return False

            # length meet the standard
            else:
                # Checking mnemonic for invalid characters (non alphabet)
                if lengthOfDigitInMnemonicIfAny:
                    self.logger.critical("Mnemonic words must be alphabet words.")
                    return False

                # check word len in mnemonic min = 2 max = 8 or the mnemonic doesn't have valid word
                elif lengthWordInMnemonic or not bip39_validate(mnemonic):
                    self.logger.critical("Please check for messing strings.")
                    return False

    def getAccountInfos(self, active_substrate, ss58_address):
        return self.logger.info(active_substrate.query('System', 'Account', params=[ss58_address]).value)

    def createAccount(self) -> json:
        createAccountMnemonic = self.createMnemonic()
        createAccountKeyPair = self.createKeypair(createAccountMnemonic)
        # check if mnemonic is created if this pass keypair will pass without errors
        if not createAccountMnemonic:
            return False

        return True
