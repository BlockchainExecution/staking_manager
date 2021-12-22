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
        self.logger = logger
        self.mnemonic = mnemonic
        self.ss58_address = ss58_address

    def createNewAccount(self):
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
        """
        The purpose of this function is to get an account info for a specific address.
        """
        try:
            value = activeConfig.activeSubstrate.query('System', 'Account', params=[self.ss58_address]).value
            fee_frozen = int(value['data']['fee_frozen']) / activeConfig.coinDecimalPlaces
            free = int(value['data']['free']) / activeConfig.coinDecimalPlaces
            reserved = int(value['data']['reserved']) / activeConfig.coinDecimalPlaces
            misc_frozen = int(value['data']['misc_frozen']) / activeConfig.coinDecimalPlaces

            self.logger.info(f"""account {self.ss58_address} infos

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
        The purpose of this function is to get an account address balance.
        """
        if purpose is None:
            # TODO: improve this to return dictionary with account values
            self.getAllAccountInfo()
        elif purpose == "bonding":
            return AccountBalanceForBonding(self.logger, self.ss58_address).getAccountBalanceForBonding()
        else:  # "undefined" scneario - error
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


# helper print method for checking the code, can delete function and all references anytime
def printTmp(printMe):
    print("\n\n****************\n %s \n****************\n\n" % printMe)
