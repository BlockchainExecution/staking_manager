import json
import sys
from bip39 import bip39_validate
# TODO: can you confirm the below github for the substrateinterface library?
from substrateinterface import Keypair # github: https://github.com/polkascan/py-substrate-interface
from substrateinterface.exceptions import SubstrateRequestException
from config import activeConfig
from Logger import myLogger
from code_src.staking.dot.fxn_decorator_implementations.accountManager import AccountBalanceForBonding


"""
Class which contains validation logic for bonding DOT.
validateAccountDataBeforeBonding() is the primary use function for this class,
it should perform all necessary validations.
The other functions are primarily used to execute validateAccountDataBeforeBonding()

TODO:
* Create class to hold the validation functions
* Better integration with accountManager

"""

# TODO: basic validations in init
class bondingValidator:
    def __init__(self, logger, ss58_address, tokenNumber):
        self.logger = logger
        self.logger.info("Validating account data for bonding")
        self.ss58_address = ss58_address
        self.tokenNumber = tokenNumber

    #def __call__(self, logger, ss58_address, tokenNumber): 

    def validateAccountDataBeforeBonding(self):
        # before we bond any coins we need to check account balance for two main things :
        #   1 - minimum dot staking amount witch is by time of writing (21/11/2021) is 120 DOT.
        #   2 - active address (Existential Deposit) witch is 1 DOT :
        #       - NB : !! If an account drops below the Existential Deposit, the account is reaped (“deactivated”)
        #           and any remaining funds are destroyed. !!
        # https://support.polkadot.network/support/solutions/articles/65000168651-what-is-the-existential-deposit-
        # so to protect user that use the script and don't know some basics we need to force check value.

        # check the number of tokens to bond is above protocol min
        self.validateBondSize()
        
        # if the bonding qty is above the protocol min,
        # check that the account balance is sufficient to bond the tokenNumber
        # will sys.exit if balance is insufficient
        self.validateAcctBalanceForBonding()

        # TODO: check that controller address matches mnc

        # check decimal writing
        lenNumberAfterDecimalPoint = len(str(tokenNumber).split(".")[1])
        if lenNumberAfterDecimalPoint > activeConfig.coinDecimalPlacesLength:
            logger.warning(
                f"wrong token value token take max {activeConfig.coinDecimalPlacesLength} number after decimal point")
            sys.exit(0)

    def validateBondSize(self):
        # TODO: the minimum to stake and the minimum to bond are not the same I assume, which should we be using?
        # TODO: confirm that the decimals of tokenNumber and stakeMin are directly comparable?
        if(self.tokenNumber < activeConfig.stakeMinimumAmount):
            self.logger.warning(f"You are trying to bond {self.tokenNumber}, but the minimum required for bonding is {activeConfig.stakeMinimumAmount} {activeConfig.coinName}\n")
            sys.exit(0)

    def validateAcctBalanceForBonding(self):

        # we need to calculate account balance vs minimum needed

        # check requirements
        totalAccountBalance = AccountBalanceForBonding.getAccountBalance(self.ss58_address)

        # we need always to reserve existentialDeposit

        if totalAccountBalance < (self.tokenNumber + activeConfig.existentialDeposit):    
            logger.warning(
                f"Low balance\n"
                f"Actual balance is : {totalAccountBalance} {activeConfig.coinName}\n"
                f"Requested amount : {tokenNumber} {activeConfig.coinName}\n"
                f"Your account needs to have a minimum of {activeConfig.existentialDeposit} "
                f"{activeConfig.coinName} plus the requested amount and it does not.\nYou need at least: "
                f"{activeConfig.existentialDeposit} + {tokenNumber} = {activeConfig.existentialDeposit + tokenNumber}, "
                f"but the account balance is only {totalAccountBalance}")
            sys.exit(0)


# helper print method for checking the code, can delete function and all references anytime
def printTmp(printMe):
    print("\n\n****************\n %s \n****************\n\n" % printMe)
