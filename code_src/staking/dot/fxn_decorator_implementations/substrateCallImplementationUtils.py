import sys
from config import activeConfig
from substrateinterface import Keypair
from code_src.staking.dot.fxn_decorator_implementations.accountImplementation import AccountImplementation


class BondingValidator:
    """
    Class which contains validation logic for bonding DOT.
    validateAccountDataBeforeBonding() is the primary use function for this class,
    it should perform all necessary validations.
    The other functions are primarily used to execute validateAccountDataBeforeBonding()
    """

    def __init__(self, logger, ss58_address, tokenNumber):
        # TODO: basic validations in init
        self.logger = logger
        self.logger.info("Validating account data for bonding")
        self.ss58_address = ss58_address
        self.tokenNumber = tokenNumber

    def __call__(self):
        self.validateAccountDataBeforeBonding()

    def validateAccountDataBeforeBonding(self):
        """
        Before we bond any coins we need to check account balance for two main things :
          1 - minimum dot staking amount witch is by time of writing (21/11/2021) is 120 DOT.
          2 - active address (Existential Deposit) witch is 1 DOT :
              - NB : !! If an account drops below the Existential Deposit, the account is reaped (“deactivated”)
                  and any remaining funds are destroyed. !!
            https://support.polkadot.network/support/solutions/articles/65000168651-what-is-the-existential-deposit-
        """

        self.validateDecimalPoint()

        # check the number of tokens to bond is above protocol min
        self.validateBondSize()

        # if the bonding qty is above the protocol min,
        # check that the account balance is sufficient to bond the tokenNumber
        # will sys.exit if balance is insufficient
        self.validateAcctBalanceForBonding()

        # TODO: check that controller address matches mnc

    def validateDecimalPoint(self):
        # check decimal writing
        lenNumberAfterDecimalPoint = len(str(self.tokenNumber).split(".")[1])
        if lenNumberAfterDecimalPoint > activeConfig.coinDecimalPlacesLength:
            self.logger.warning(
                f"wrong token value token take max {activeConfig.coinDecimalPlacesLength} number after decimal point")
            sys.exit(0)

    def validateBondSize(self):
        """
        Function checks that the size of the bond is above the minimum defined by the network
        Minimum dot staking amount witch is by time of writing (21/11/2021) is 120 DOT.
        TODO: the minimum to stake and the minimum to bond are not the same I assume, which should we be using?
        TODO: confirm that the decimals of tokenNumber and stakeMin are directly comparable?
        """
        if self.tokenNumber < activeConfig.stakeMinimumAmount:
            self.logger.warning(
                f"You are trying to bond {self.tokenNumber}, but the minimum required for bonding is {activeConfig.stakeMinimumAmount} {activeConfig.coinName}\n")
            sys.exit(0)

    def validateAcctBalanceForBonding(self):
        """
        Function calculates and compares account balance vs minimum balance needed to stake
        """
        # check requirements
        accountToVerify = AccountImplementation(self.logger, ss58_address=self.ss58_address)
        totalAccountBalance = accountToVerify.getAccountBalance("bonding")
        transactionFees = TransactionFees(ss58_address=self.ss58_address, dest=activeConfig.activeValidator[0],
                                          value=self.tokenNumber).estimateTxFees()

        # we need always to reserve existentialDeposit
        if totalAccountBalance < (self.tokenNumber + transactionFees + activeConfig.existentialDeposit):
            tokenNumber = self.tokenNumber / activeConfig.coinDecimalPlaces
            self.logger.warning(
                f"Low balance\n"
                f"Actual balance is : {totalAccountBalance} {activeConfig.coinName}\n"
                f"Requested amount : {tokenNumber} {activeConfig.coinName}\n"
                f"Your account needs to have a minimum of {activeConfig.existentialDeposit} "
                f"{activeConfig.coinName} plus the requested amount plus the transaction fees and it does not.\nYou need at least: "
                f"{activeConfig.existentialDeposit} + {tokenNumber} + {transactionFees} = {activeConfig.existentialDeposit + tokenNumber + transactionFees}, "
                f"but the account balance is only {totalAccountBalance}")
            sys.exit(0)


class TransactionFees:
    def __init__(self, ss58_address, dest, value):
        self.ss58_address = ss58_address
        self.dest = dest
        self.value = value

    def estimateTxFees(self):
        keypair = Keypair(ss58_address=self.ss58_address)

        call = activeConfig.activeSubstrate.compose_call(
            call_module='Balances',
            call_function='transfer',
            call_params={
                'dest': self.dest,
                'value': self.value * activeConfig.coinDecimalPlaces
            }
        )
        payment_info = activeConfig.activeSubstrate.get_payment_info(call=call, keypair=keypair)[
                           'partialFee'] / activeConfig.coinDecimalPlaces
        return payment_info


# helper print method for checking the code, can delete function and all references anytime
def printTmp(printMe):
    print("\n\n****************\n %s \n****************\n\n" % printMe)
