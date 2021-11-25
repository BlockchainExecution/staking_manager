import json
import sys
from bip39 import bip39_validate
from substrateinterface import Keypair
from substrateinterface.exceptions import SubstrateRequestException
from config import activeConfig
from Logger import myLogger


def dotCreateKeyPair(logger, mnemonic):
    invalidCharacters = "[@_!#$%^&*()<>?/|}{~:]0123456789"

    try:
        key = Keypair.create_from_mnemonic(mnemonic=mnemonic, ss58_format=activeConfig.ss58_format)
        logger.info(f"""create key pair

    {key}
""")
        return key
    except ValueError:
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


def checkAccount(ss58_address, tokenNumber, logger):
    # before we bond any coins we need to check account balance for two main things :
    #   1 - minimum dot staking amount witch is by time of writing (21/11/2021) is 120 DOT.
    #   2 - active address (Existential Deposit) witch is 1 DOT :
    #       - NB : If an account drops below the Existential Deposit, the account is reaped (“deactivated”)
    #           and any remaining funds are destroyed.
    # so to protect user that use the script and don't know some basics we need to force check value.

    # query balance info for an account
    accountBalanceInfo = activeConfig.activeSubstrate.query('System', 'Account',
                                                            params=[ss58_address]).value

    # we only need free and reserved information from the balance info
    free, reserved = accountBalanceInfo['data']['free'], accountBalanceInfo['data']['reserved']

    # we need to calculate account balance vs minimum needed
    totalAccountBalance = free / activeConfig.coinDecimalPlaces + reserved / activeConfig.coinDecimalPlaces
    minimumTotalNeeded = activeConfig.stakeMinimumAmount + activeConfig.existentialDeposit

    # check requirements

    # check decimal writing
    lenNumberAfterDecimalPoint = len(str(tokenNumber).split(".")[1])
    if lenNumberAfterDecimalPoint > activeConfig.coinDecimalPlacesLength:
        logger.warning(
            f"wrong token value token take max {activeConfig.coinDecimalPlacesLength} number after decimal point")
        sys.exit(0)

    # we need always to reserve existentialDeposit
    if totalAccountBalance < minimumTotalNeeded or totalAccountBalance < tokenNumber + activeConfig.existentialDeposit:
        logger.warning(
            f"low balance\n"
            f"actual balance is : {totalAccountBalance} {activeConfig.coinName}\n"
            f"requested amount : {tokenNumber} {activeConfig.coinName}\n"
            f"why this happen your account need to have a minimum of {activeConfig.existentialDeposit} "
            f"{activeConfig.coinName} plus the requested amount wish is not the case "
            f"{activeConfig.existentialDeposit} + {tokenNumber} != {totalAccountBalance}")
        sys.exit(0)

    # account has minimum requirements
    # check for token number vs account balance
    if tokenNumber < activeConfig.stakeMinimumAmount:
        logger.warning(f"staking minimum amount is {activeConfig.stakeMinimumAmount} {activeConfig.coinName}")
        sys.exit(0)


class DotSubstrateCall:
    def __init__(self, cli_name, call_module, call_params, seed):
        self.call_module = call_module
        self.call_params = call_params
        self.seed = seed
        self.logger = myLogger(cli_name)
        self.logger.info("Start %s Program." % cli_name)

    def __call__(self, func):
        self.logger.info("execute %s function." % func.__name__)
        print(self.call_module, self.call_params, self.seed)

        if func.__name__ == "bond":
            checkAccount(ss58_address=self.call_params['controller'], tokenNumber=self.call_params['value'],
                         logger=self.logger)

        try:
            self.call_params['value'] = self.call_params['value'] * activeConfig.coinDecimalPlaces
        except KeyError:
            pass

        call = activeConfig.activeSubstrate.compose_call(
            call_module=f"{self.call_module}",
            call_function=f"{func.__name__}",
            call_params=self.call_params
        )

        """
        :param active_substrate: dot substrate to connect to
        :param seed: mnemonic phrase to sign the transaction
        :param call: transition parameters
        :return:
        """

        this_keypair = dotCreateKeyPair(logger=self.logger, mnemonic=self.seed)
        extrinsic = activeConfig.activeSubstrate.create_signed_extrinsic(call=call, keypair=this_keypair)
        """None
        {'substrate': < substrateinterface.base.SubstrateInterfaceobject at 0x000001F7C2F73F70 >, 
        'extrinsic_hash': '0xa9719ca1430e4a9f0305b03e4b6bdd582458525bcc44b01db3caa7fa7d933867', 
        'block_hash': '0xdd088c78eaee25ad99bc7d12c6d5cc5f4d81c6e301951d11501c77254c960505', 
        'block_number': None, 
        'finalized': False, 
        '_ExtrinsicReceipt__extrinsic_idx': None, 
        '_ExtrinsicReceipt__extrinsic': None, 
        '_ExtrinsicReceipt__triggered_events': None, 
        '_ExtrinsicReceipt__is_success': None, 
        '_ExtrinsicReceipt__error_message': None, 
        '_ExtrinsicReceipt__weight': None, 
        '_ExtrinsicReceipt__total_fee_amount': None
        }"""
        try:
            receipt = activeConfig.activeSubstrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)

            print(receipt.finalized)
            self.logger.info(
                "Extrinsic '{}' sent and included in block '{}'".format(receipt.extrinsic_hash, receipt.block_hash))

            self.__exit__()

        except SubstrateRequestException as e:
            arg = e.args[0]
            try:
                self.logger.error("%s : %s" % (arg['message'], arg['data']))
                self.__exit__()
            except KeyError:
                self.logger.error("%s" % (arg['message']))
                self.__exit__()

    def __exit__(self):
        # close connection with remote socket
        activeConfig.activeSubstrate.close()
        # exit system
        sys.exit(0)


# TODO
class DotValidatorCall:
    def __init__(self):
        self.cli_name = "Validator"
        self.logger = myLogger(self.cli_name)
        self.logger.info("Start %s Program." % self.cli_name)

    def __exit__(self):
        pass
