import json
import sys
from bip39 import bip39_validate
# TODO: can you confirm the below github for the substrateinterface library?
from substrateinterface import Keypair # github: https://github.com/polkascan/py-substrate-interface
from substrateinterface.exceptions import SubstrateRequestException
from config import activeConfig
from Logger import myLogger
from code_src.staking.dot.fxn_decorator_implementations.accountImplementationUtils import *

class AccountImplementation:
    """
    * TODO: rename to AccountImplementation (big refactor)

    AccountImplementation is a class for containing functions related to accounts.
    An "account" is defined as keypair with associated data.

    AccountImplementation also serves as a kind of interface for all functions outside accountImplementation.py and
    accountImplementationUtils.py to have 1 reference point for 'account' related functions. 
    Any classes/functions outside accountImplementation.py and accountImplementationUtils.py should not need to 
    directly refer to any code in accountImplementationUtils.py

    Therefore, some of the functions in AccountImplementation are "redundant", e.g. 
    createMnemonic just calls MnemonicImplementation in accountImplementationUtils.py
    """
    def __init__(self, logger, mnemonic="", ss58_address=""):
        self.mnemonic = mnemonic
        self.ss58_address = ss58_address
        self.logger = logger

    def createNewAccount(self) -> json:
        # TODO: createAccount is not returning a json, is that a problem?
        # MnemonicImplementation is called here instead of self.createMnemonic() because it's better
        # for functions in the AccountImplementation class to directly call the implementation classes
        newMnemonic = MnemonicImplementation(self.logger).createMnemonic()
        createAccountKeyPair = KeyPairImplementation(self.logger, newMnemonic).getAddressFromMnemonic()
        # check if mnemonic is created if this pass keypair will pass without errors
        if not createAccountKeyPair:
            return False
        return True

    def createMnemonic(self):
        """
        The purpose of this function is to provide a function in AccountImplementation class
        to create a mnemonic without requiring a function outside accountImplementation.py to
        call a function in accountImplementationUtils.py
        """
        newMnemonic = MnemonicImplementation(self.logger).createMnemonic()
        return newMnemonic

    def getAddressFromMnemonic(self):
        """
        The purpose of this function is to provide a function in AccountImplementation class
        to get an address from a mnemonic without requiring a function outside accountImplementation.py
        to call a function in accountImplementationUtils.py
        """
        address = KeyPairImplementation(self.logger, self.mnemonic).getAddressFromMnemonic()
        return address

    def getAllAccountInfo(self):
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

#    def getAccountBalanceForBonding(self):
#    def getAccountBalance():

class DotAccountCall:
    """
    Class for executing account related calls for DOT
    The following calls are made to this class:
    * All calls in accountingArgParser.py (mnemonic, keypair, info, create)
    """
    def __init__(self, mnemonic="", ss58_address=""):
        self.cli_name = "Accounting"
        self.mnemonic = mnemonic
        self.ss58_address = ss58_address
        self.logger = myLogger(self.cli_name)
        self.logger.info("Start %s Program." % self.cli_name)

    def __call__(self, func):
        name = func.__name__
        if name == "mnemonic":
            AccountImplementation(self.logger, self.mnemonic, self.ss58_address).createMnemonic()
        elif name == "create":
            AccountImplementation(self.logger, self.mnemonic, self.ss58_address).createNewAccount()
        elif name == "info":
            AccountImplementation(self.logger, self.mnemonic, self.ss58_address).getAllAccountInfo()
        elif name == "keypair":
            AccountImplementation(self.logger, self.mnemonic, self.ss58_address).getAddressFromMnemonic()
        else:
            pass

### ----- Move to Utils file after finished factoring/debugging ----- ###

class AccountBalanceForBonding:
    """
    Class is to return balance of bonding - verifications
    TODO: Better explanation
    # TODO:
    # * rename AccountBalance class; better inheretence/abstraction
    # * use accountImplementation
    # * called in substrateCallImplementationUtils.py
    # Why doens't this go in DotAccountCall?
    """
    def __init__(self, logger, ss58_address, account: AccountImplementation):
        self.logger = logger
        self.ss58_address = ss58_address

        # takes AccountImplementation as initialization arguement
        if(isinstance(account, AccountImplementation()) == False):
            logger.warning("AccountImplementation type *not* passed to initialize AccountBalanceForBonding. Failing.")
            return False

    def getAccountBalanceForBonding(self):
        # query balance info for an account
        accountBalanceInfo = activeConfig.activeSubstrate.query('System', 'Account',
                                                                params=[self.s58_address]).value

        # we only need free and reserved information from the balance info
        # free and reserved explained: https://wiki.polkadot.network/docs/learn-accounts#balance-types
        # TODO: decide what the account balance calculation "should" be, i.e. free + reserved or only free?
        free,reserved = accountBalanceInfo['data']['free'], accountBalanceInfo['data']['reserved']

        # free and reserved are given as uint quantity; convert to float
        totalAccountBalance = free / activeConfig.coinDecimalPlaces + reserved / activeConfig.coinDecimalPlaces

        return totalAccountBalance

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
    def __init__(self, logger, mnemonic):
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
        if (len(self.mnemonic) < 10):
                logger.critical("A bad mnemonic as been passed to create the keypair")
                return False

        try:
            # Keypair ~ https://github.com/polkascan/py-substrate-interface#keypair-creation-and-signing
            key = Keypair.create_from_mnemonic(mnemonic=self.mnemonic, ss58_format=activeConfig.ss58_format)
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



            ### TEST THIS CLASS BEFORE DELETING BELOW ###

    # def createMnemonic(self):
    #     m = MnemonicImplementation()
    #     return m.createMnemonic()

    # def getAccountInfos(self, ss58_address):
    #     a = AccountImplementation(self.logger, self.mnemonic, self.ss58_address)
    #     a.getAllAccountInfo()
    #     try:
    #         value = activeConfig.activeSubstrate.query('System', 'Account', params=[ss58_address]).value
    #         fee_frozen = int(value['data']['fee_frozen']) / activeConfig.coinDecimalPlaces
    #         free = int(value['data']['free']) / activeConfig.coinDecimalPlaces
    #         reserved = int(value['data']['reserved']) / activeConfig.coinDecimalPlaces
    #         misc_frozen = int(value['data']['misc_frozen']) / activeConfig.coinDecimalPlaces

    #         self.logger.info(f"""account {ss58_address} infos

    # nonce : {value['nonce']}
    # consumers : {value['consumers']}
    # providers : {value['providers']}
    # sufficients : {value['sufficients']}
    # free : {free} {activeConfig.coinName}
    # reserved : {reserved} {activeConfig.coinName}
    # misc_frozen : {misc_frozen} {activeConfig.coinName}
    # fee_frozen : {fee_frozen} {activeConfig.coinName}
    # """)
    #     except Exception as e:
    #         self.logger.error(f"{e}")

    # def createAccount(self) -> json:
    #     return AccountImplementation().createAccount()
        # createAccountMnemonic = self.createMnemonic()
        # createAccountKeyPair = dotCreateKeyPair(self.logger, createAccountMnemonic)
        # # check if mnemonic is created if this pass keypair will pass without errors
        # if not createAccountKeyPair:
        #     return False
        # return True

# helper print method for checking the code, can delete function and all references anytime
def printTmp(printMe):
    print("\n\n****************\n %s \n****************\n\n" % printMe)
