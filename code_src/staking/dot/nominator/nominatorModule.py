import sys
from substrateinterface import Keypair
from substrateinterface.exceptions import SubstrateRequestException
from Logger import myLogger


class Nominator(object):

    def __init__(self):
        self.__name = "Nominator"
        self.logger = myLogger(self.__name)
        self.logger.info("Start Nominator Program.")
        self.call_module = "Staking"

    def getKeyFromSeed(self, seed):
        try:
            return Keypair.create_from_mnemonic(seed)
        except ValueError as e:
            self.logger.error(e)
            sys.exit(0)

    def nominate(self, active_substrate, targets):
        self.logger.info("start nominate script.")
        """
        {'call_name': 'nominate',
        'call_args': [{'name': 'targets', 'type': 155, 'typeName': 'Vec<<T::Lookup as StaticLookup>::Source>', 'docs': []}],
         'documentation': "Declare the desire to nominate `targets` for the origin controller.
         Effects will be felt at the beginning of the next era.
         The dispatch origin for this call must be _Signed_ by the controller, not the stash.
         # <weight>
         - The transaction's complexity is proportional to the size of `targets` (N)
         which is capped at CompactAssignments::LIMIT (MAX_NOMINATIONS).
         - Both the reads and writes follow a similar pattern.
         # </weight>",
         'module_prefix': 'Staking', 'module_name': 'Staking', 'spec_version': 9122}
        :return:
        """

        call = active_substrate.compose_call(
            call_module=self.call_module,
            call_function='nominate',
            call_params={
                'targets': targets,
            }
        )

        return call

    # TODO add unnominate function

    def run(self, active_substrate, seed, call):
        this_substrate = active_substrate
        this_keypair = self.getKeyFromSeed(seed=seed)
        extrinsic = this_substrate.create_signed_extrinsic(call=call, keypair=this_keypair)
        try:
            receipt = this_substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
            return self.logger.info(
                "Extrinsic '{}' sent and included in block '{}'".format(receipt.extrinsic_hash, receipt.block_hash))

        except SubstrateRequestException as e:
            arg = e.args[0]
            return self.logger.error("%s : %s" % (arg['message'], arg['data']))
