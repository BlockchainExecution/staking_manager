import sys
from substrateinterface import Keypair
from substrateinterface.exceptions import SubstrateRequestException
from Logger import myLogger


class Bounder(object):
    def __init__(self):
        self.__name = "Bounder"
        self.logger = myLogger(self.__name)
        self.logger.info("Start Bounder Program.")
        self.call_module = "Staking"

    def getKeyFromSeed(self, seed):
        try:
            return Keypair.create_from_mnemonic(seed)
        except ValueError as e:
            self.logger.error(e)
            sys.exit(0)

    def bond(self, active_substrate, controller_addr, value, reward_address=""):
        self.logger.info("start bond script.")
        """
        {'call_name': 'bond',
        'call_args': [{'name': 'controller', 'type': 147, 'typeName': '<T::Lookup as StaticLookup>::Source', 'docs': []},
        {'name': 'value', 'type': 51, 'typeName': 'BalanceOf<T>', 'docs': []},
        {'name': 'payee', 'type': 152, 'typeName': 'RewardDestination<T::AccountId>', 'docs': []}],
        'documentation': 'Take the origin account as a stash and lock up `value` of its balance. `controller`will
        be the account that controls it.
        `value` must be more than the `minimum_balance` specified by`T::Currency`.
        The dispatch origin for this call must be _Signed_ by the stash account.
        Emits `Bonded`.
        # <weight>
        - Independent of the arguments. Moderate complexity.
        - O(1).\n- Three extra DB entries.
        NOTE:Two of the storage writes (`Self::bonded`, `Self::payee`) are _never_ cleaned
        unless the `origin` falls below _existential deposit_ and gets removed as dust.
        # </weight>',
        'module_prefix': 'Staking','module_name': 'Staking', 'spec_version': 9122}
        :return:
        """
        if not reward_address:
            reward_address = controller_addr
        try:
            call = active_substrate.compose_call(
                call_module=self.call_module,
                call_function='bond',
                call_params={
                    'controller': controller_addr,
                    'value': value,
                    'payee': reward_address
                }
            )

            return call

        except NotImplementedError as e:
            self.logger.error(e)
            sys.exit(0)

    def unBound(self, active_substrate, value):
        self.logger.info("start unBound script.")
        """
        {'call_name': 'unbond', 'call_args':
         [{'name': 'value', 'type': 51, 'typeName': 'BalanceOf<T>', 'docs': []}],
         'documentation': 'Schedule a portion of the stash to be unlocked ready for transfer out after the bond
         period ends. If this leaves an amount actively bonded less than
         T::Currency::minimum_balance(), then it is increased to the full amount.
         The dispatch origin for this call must be _Signed_ by the controller, not the stash.
         Once the unlock period is done, you can call `withdraw_unbonded` to actually move
         the funds out of management ready for transfer.
         No more than a limited number of unlocking chunks (see `MAX_UNLOCKING_CHUNKS`)
         can co-exists at the same time. In that case, [`Call::withdraw_unbonded`]need
         to be called first to remove some of the chunks (if possible).
         If a user encounters the `InsufficientBond` error when calling this extrinsic,
         they should call `chill` first in order to free up their bonded funds.
         Emits `Unbonded`.See also [`Call::withdraw_unbonded`].',
        'module_prefix': 'Staking', 'module_name': 'Staking', 'spec_version': 9122}
        :return:
        """

        call = active_substrate.compose_call(
            call_module=self.call_module,
            call_function='unbond',
            call_params={
                'value': value,
            }
        )

        return call

    def reBound(self, active_substrate, value):
        self.logger.info("start reBound script.")
        """
        {'call_name': 'rebond',
        'call_args': [{'name': 'value', 'type': 51, 'typeName': 'BalanceOf<T>', 'docs': []}],
        'documentation': "Rebond a portion of the stash scheduled to be unlocked.
        The dispatch origin must be signed by the controller.
        # <weight>
        - Time complexity: O(L), where L is unlocking chunks
        - Bounded by `MAX_UNLOCKING_CHUNKS`.
        - Storage changes: Can't increase storage, only decrease it.
        # </weight>",
        'module_prefix': 'Staking', 'module_name': 'Staking', 'spec_version': 9122}
        :return:
        """

        call = active_substrate.compose_call(
            call_module=self.call_module,
            call_function='rebond',
            call_params={
                'value': value,
            }
        )

        return call

    def bondExtra(self, active_substrate, value):
        self.logger.info("start bondExtra script.")
        """
        {'call_name': 'bond_extra', 'call_args':
         [{'name': 'max_additional', 'type': 51, 'typeName': 'BalanceOf<T>',

         'docs': []}], 'documentation': 'Add some extra amount that have appeared in the stash `free_balance` into the
         balance up\nfor staking.\n\nThe dispatch origin for this call must be _Signed_ by the stash, not the controller
         .\n\nUse this if there are additional funds in your stash account that you wish to bond.\nUnlike [`bond`]
         (Self::bond) or [`unbond`](Self::unbond) this function does not impose\nany limitation on the amount that
         can be added.\n\nEmits `Bonded`.\n\n# <weight>\n- Independent of the arguments. Insignificant complexity.\n-
         O(1).\n# </weight>', 'module_prefix': 'Staking', 'module_name': 'Staking', 'spec_version': 9122}
        :return:
        """
        call = active_substrate.compose_call(
            call_module=self.call_module,
            call_function='bond_extra',
            call_params={
                'max_additional': value,
            }
        )

        return call

    def withdrawUnBonded(self, active_substrate, value):
        self.logger.info("start withdrawUnbonded script.")
        """
        {'call_name': 'withdraw_unbonded',
        'call_args': [{'name': 'num_slashing_spans', 'type': 4, 'typeName': 'u32', 'docs': []}],
        'documentation': 'Remove any unlocked chunks from the `unlocking` queue from our management.
        This essentially frees up that balance to be used by the stash account to do
        whatever it wants.
        The dispatch origin for this call must be _Signed_ by the controller.Emits `Withdrawn`.
        See also [`Call::unbond`].
        # <weight>
        Complexity O(S) where S is the number of slashing spans to remove
        NOTE: Weight annotation is the kill scenario, we refund otherwise.
        # </weight>',
        'module_prefix': 'Staking', 'module_name': 'Staking', 'spec_version': 9122}
        :return:
        """

        call = active_substrate.compose_call(
            call_module=self.call_module,
            call_function='withdraw_unbonded',
            call_params={
                'num_slashing_spans': value,
            }
        )

        return call

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
