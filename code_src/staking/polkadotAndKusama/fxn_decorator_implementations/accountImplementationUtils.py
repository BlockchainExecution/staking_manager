from bip39 import bip39_validate
from substrateinterface import Keypair


# DO NOT import accountImplementation, dependencies cannot be circular, must be 1 direction,
# If you feel a "need" to import accountImplementation.py, don't, fix the code instead 

class MnemonicImplementation:
    """
    Class creates a mnemonic and prints in the log, currently has no other purpose
    * For security reasons, do not store the mnemonics
    * This class is intentionally separate from AccountImplementation as there may be times
    when features of mnemonics should be added/changed without concerning AccountImplementation
    """

    def __init__(self, logger):
        self.logger = logger

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


class KeyPairImplementation:
    """
    Class creates a keypair
    """

    def __init__(self, config, logger, mnemonic):
        self.activeConfig = config
        self.logger = logger
        self.mnemonic = mnemonic
        # what to do if no mnemonic is passed? Adapt fxn signature.

    # previously dotCreateKeyPair
    # def createKeyPair(self):
    def getAddressFromMnemonic(self):
        """
        Calculates the dot address given a mnemonic and prints and returns it (or exits the system if it fails).
        It's currently kept outside the DotAccountCall as an auxilary function in order to keep the pre-defined
        function set in DotAccountCall (i.e. createMnemonic, getAccountInfos, etc.)
        Function is called from DotAccountCall and DotSubstrateCall
        """
        invalidCharacters = "[@_!#$%^&*()<>?/|}{~:]0123456789"

        # If a mnemonic is not passed in, the default in the above library will be used
        # however, we will enforce that "something" is passed in to avoid the default (len 10 is arbitrary)
        if (len(self.mnemonic.split(' ')) < 10):
            self.logger.critical("A bad mnemonic as been passed to create the keypair")
            return False

        try:
            # Keypair ~ https://github.com/polkascan/py-substrate-interface#keypair-creation-and-signing
            key = Keypair.create_from_mnemonic(mnemonic=self.mnemonic, ss58_format=self.activeConfig.ss58_format)
            self.logger.info(f"""Here is the address associated with the above mnemonic:\n
        {key}
         \n\n""")

            # do a quick verification that the key signs normally
            if key.verify("This is a test message", key.sign("This is a test message")):
                return key
            else:
                # if the key verification fails, exit immediatly
                self.logger.critical("\nDO NOT USE KEY. KEY INCORRECTLY GENERATED.\n")
                return False

        except ValueError:
            # more thorough check for the mnemonic below

            # split mnemonic by space into words
            splitMnemonic = self.mnemonic.split(" ")

            lengthMnemonic = len(splitMnemonic)
            # check word length and special character
            lengthWordInMnemonic = any(word for word in splitMnemonic if len(word) < 3 or len(word) > 8)
            lengthOfDigitInMnemonicIfAny = any(s for s in self.mnemonic if s in invalidCharacters)

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
                elif lengthWordInMnemonic or not bip39_validate(self.mnemonic):
                    self.logger.critical("Please check for messing strings.")
                    return False


class AccountBalanceForBonding:
    """
    Class is to return balance of bonding - verifications
    TODO: Better explanation
    # TODO:
    # * Ideally keep in Utils file instead of here, but need to refactor
    # to prevent importing accountImplementation.py in Utils
    """

    def __init__(self, config, logger, ss58_address):
        self.activeConfig = config
        self.logger = logger
        self.ss58_address = ss58_address

    def __call__(self):
        return self.getAccountBalanceForBonding()

    def getAccountBalanceForBonding(self):
        # query balance info for an account
        accountBalanceInfo = self.activeConfig.activeSubstrate.query('System', 'Account',
                                                                     params=[self.ss58_address]).value

        # In general, the usable balance of the account is the amount that is free minus any funds that are considered
        # frozen (either misc_frozen or fee_frozen) and depend on the reason for which the funds are to be used.
        # If the funds are to be used for transfers, then the usable amount is the free amount minus
        # any misc_frozen funds. However, if the funds are to be used to pay transaction fees,
        # the usable amount would be the free funds minus fee_frozen.
        # explained: https://wiki.polkadot.network/docs/learn-accounts#balance-types

        """
        In this situation we are using send funds balance witch is free minus misc_frozen
        """
        free = accountBalanceInfo['data']['free']

        # transferable balance
        miscFrozen = accountBalanceInfo['data']['misc_frozen']
        totalAccountBalance = (free - miscFrozen) / self.activeConfig.coinDecimalPlaces

        return totalAccountBalance
