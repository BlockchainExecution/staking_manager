import json
import sys
from bip39 import bip39_validate
# TODO: can you confirm the below github for the substrateinterface library?
from substrateinterface import Keypair # github: https://github.com/polkascan/py-substrate-interface
from substrateinterface.exceptions import SubstrateRequestException
from config import activeConfig
from Logger import myLogger
from code_src.staking.dot.fxn_decorator_implementations.substrateCallManagerUtils import *
# TODO: 
# consider adding dotCreateKeyPair() to DotAccountCall so that this file only has to import
# accountManager and not a utils file for accountManager... importing another utils file isn't very clean
from code_src.staking.dot.fxn_decorator_implementations.accountManagerUtils import *


class DotSubstrateCall:
    """
    Generic class for executing calls to DOT network
    The following calls are made to this class:
    * All calls in bounderArgParser.py (bond, unbond, rebond, bondextra, withdrawunbounded)
    * Some calls in nominatorArgParser.py (nominate, unnominate)
    * 1 call in stakerArgParser (staker)
    """
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
            bondValidator = bondingValidator(logger=self.logger, ss58_address=self.call_params['controller'], tokenNumber=self.call_params['value'])
            bondValidator.validateAccountDataBeforeBonding()

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

        #this_keypair = dotCreateKeyPair(logger=self.logger, mnemonic=self.seed)
        # TODO: should call AccountManager().createAccount() instead to keep everything needed in accountManager.py
        this_keypair = KeyPairManager(logger=self.logger, mnemonic=self.seed).getAddressFromMnemonic()

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


# helper print method for checking the code, can delete function and all references anytime
def printTmp(printMe):
    print("\n\n****************\n %s \n****************\n\n" % printMe)
