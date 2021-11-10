from common import active_substrate


class Bond(object):
    def __init__(self, controller_addr, value, reward_address, keypair):
        self.call_module = "Staking"
        self.substrate = active_substrate
        self.controller_addr = controller_addr
        self.value = value
        self.reward_address = reward_address
        self.keypair = keypair

    def bond(self):
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
        call = self.substrate.compose_call(
            call_module=self.call_module,
            call_function='bond',
            call_params={
                'controller': self.controller_addr,
                'value': self.value,
                'payee': self.reward_address
            }
        )

        return call

    def bond_extra(self):
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
        call = self.substrate.compose_call(
            call_module=self.call_module,
            call_function='bond_extra',
            call_params={
                'max_additional': self.value,
            }
        )

        return call

    def unbond(self):
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

        call = self.substrate.compose_call(
            call_module=self.call_module,
            call_function='unbond',
            call_params={
                'value': self.value,
            }
        )

        return call

    def withdraw_unbonded(self):
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

        call = self.substrate.compose_call(
            call_module=self.call_module,
            call_function='withdraw_unbonded',
            call_params={
                'num_slashing_spans': self.value,
            }
        )

        return call

    def rebond(self):
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

        call = self.substrate.compose_call(
            call_module=self.call_module,
            call_function='rebond',
            call_params={
                'value': self.value,
            }
        )

        return call
