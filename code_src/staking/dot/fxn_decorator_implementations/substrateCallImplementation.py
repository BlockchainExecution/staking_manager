from code_src.staking.dot.fxn_decorator_implementations.substrateCallImplementationUtils import *
from code_src.staking.dot.fxn_decorator_implementations.accountImplementation import *


# https://docs.rs/pallet-staking/latest/pallet_staking/enum.Call.html#variant.chill
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

    def call(self, call):
        """
        :param active_substrate: dot substrate to connect to
        :param seed: mnemonic phrase to sign the transaction
        :param call: transition parameters
        :return:
        """

        # this_keypair = dotCreateKeyPair(logger=self.logger, mnemonic=self.seed)
        # TODO: should call AccountImplementation().createAccount() instead to keep everything needed in accountImplementation.py
        # this_keypair = KeyPairImplementation().getAddressFromMnemonic()
        this_address = AccountImplementation(logger=self.logger, mnemonic=self.seed).getAddressFromMnemonic()
        extrinsic = activeConfig.activeSubstrate.create_signed_extrinsic(call=call, keypair=this_address)
        try:
            receipt = activeConfig.activeSubstrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)

            print(receipt.finalized)
            self.logger.info(
                "Extrinsic '{}' sent and included in block '{}'".format(receipt.extrinsic_hash, receipt.block_hash))

        except SubstrateRequestException as e:
            arg = e.args[0]
            try:
                self.logger.error("%s : %s" % (arg['message'], arg['data']))
                self.__exit__()
            except KeyError:
                if arg['message'] == "Transaction is temporarily banned":
                    self.logger.error(
                        "The tx is already in pool. Either try on a different node, or wait to see if the initial transaction goes through.")
                    self.__exit__()
                else:
                    self.logger.error("%s" % (arg['message']))
                    self.__exit__()

    def __call__(self, func):
        self.logger.info("execute %s function." % func.__name__)
        print(self.call_module, self.call_params, self.seed)

        if func.__name__ == "bond":
            bondValidator = BondingValidator(logger=self.logger, ss58_address=self.call_params['controller'],
                                             tokenNumber=self.call_params['value'])
            bondValidator.validateAccountDataBeforeBonding()

        if func.__name__ == "bond_extra":
            self.call_params['max_additional'] = self.call_params['value'] * activeConfig.coinDecimalPlaces

        try:
            self.call_params['value'] = self.call_params['value'] * activeConfig.coinDecimalPlaces
        except KeyError:
            pass

        call_chill = activeConfig.activeSubstrate.compose_call(
            call_module=f"{self.call_module}",
            call_function="chill",
            call_params={}
        )

        if func.__name__ == "bond":
            call_bond = activeConfig.activeSubstrate.compose_call(
                call_module=f"{self.call_module}",
                call_function=f"{func.__name__}",
                call_params=self.call_params
            )
            self.call(call_chill)
            self.call(call_bond)

            self.__exit__()

        elif func.__name__ == "stop_nominate_all":

            call_unbond = activeConfig.activeSubstrate.compose_call(
                call_module=f"{self.call_module}",
                call_function="unbond",
                call_params=self.call_params
            )

            self.call(call_chill)
            self.call(call_unbond)

            self.__exit__()

        elif func.__name__ == "stake":
            print(f"function {func.__name__}")
            print(self.call_params)
            call_params_bond = {'controller': self.call_params['controller'],
                                'value': self.call_params['value'],
                                'payee': self.call_params['payee']}

            call_bond = activeConfig.activeSubstrate.compose_call(
                call_module=f"{self.call_module}",
                call_function="bond",
                call_params=call_params_bond
            )
            call_params_nominate = {'targets': self.call_params['targets']}

            call_nominate = activeConfig.activeSubstrate.compose_call(
                call_module=f"{self.call_module}",
                call_function="nominate",
                call_params=call_params_nominate
            )

            self.call(call_bond)
            self.call(call_nominate)

            self.__exit__()
        else:
            call = activeConfig.activeSubstrate.compose_call(
                call_module=f"{self.call_module}",
                call_function=f"{func.__name__}",
                call_params=self.call_params
            )
            self.call(call)
            self.__exit__()

    def __exit__(self):
        # close connection with remote socket
        activeConfig.activeSubstrate.close()
        # exit system
        sys.exit(0)


# helper print method for checking the code, can delete function and all references anytime
def printTmp(printMe):
    print("\n\n****************\n %s \n****************\n\n" % printMe)
