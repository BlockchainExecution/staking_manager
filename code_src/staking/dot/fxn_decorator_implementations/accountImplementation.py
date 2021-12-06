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
    AccountImplementation is a class for containing functions related to accounts.
    An "account" is defined as keypair with associated data.

    AccountImplementation also serves as a kind of interface for all functions outside accountImplementation.py and
    accountImplementationUtils.py to have 1 reference point for 'account' related functions. 
    Any classes/functions outside accountImplementation.py and accountImplementationUtils.py should not need to 
    directly refer to any code in accountImplementationUtils.py

    Therefore, some of the functions in AccountImplementation are "redundant", e.g. 
    createMnemonic just calls MnemonicImplementation in accountImplementationUtils.py
    """
    def __init__(self, logger, mnemonic=None, ss58_address=None):
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

    def getAccountBalance(self, purpose=None):
        """
        TODO: Document
        """
        if(purpose == None):
            # TODO: improve this to return dictionary with account values
            self.getAllAccountInfo()
        elif (purpose == "bonding"):
            return AccountBalanceForBonding(self).getAccountBalanceForBonding()
        else: # "undefined" scneario - error
            self.logger.warning(f"Unknown object passed into getAccountBalance. Failing.")
            sys.exit(0)


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
    # * Ideally keep in Utils file instead of here, but need to refactor 
    # to prevent importing accountImplementation.py in Utils
    """
    def __init__(self, account: AccountImplementation):
        self.logger = account.logger
        self.ss58_address = account.ss58_address

        # takes AccountImplementation as initialization arguement
        if(isinstance(account, AccountImplementation) == False):
            print("""AccountImplementation type *not* passed to initialize AccountBalanceForBonding.\n
                Therefore, the logger is not set and this erorr is printed instead of logger.
                Program Exiting...""")
            # TODO: If wrong object passed, logger will not be set and not print the error. Fix.
            logger.warning("AccountImplementation type *not* passed to initialize AccountBalanceForBonding. Failing.")
            sys.exit(0)
            return False

    def __call__(self):
        return self.getAccountBalanceForBonding()

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
