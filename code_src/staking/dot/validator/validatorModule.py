from common import active_substrate


class Validator(object):
    def __init__(self):
        self.call_module = "Staking"
        self.substrate = active_substrate

    def set_validator_count(self, new):
        """
        {'call_name': 'set_validator_count', 'call_args': [{'name': 'new', 'type': 107, 'typeName': 'u32', 'docs': []}],
         'documentation': 'Sets the ideal number of validators.
         The dispatch origin must be Root.
         # <weight>\nWeight: O(1)
         Write: Validator Count
         # </weight>',
         'module_prefix': 'Staking', 'module_name': 'Staking', 'spec_version': 9122
        :return:
        """

        call = self.substrate.compose_call(
            call_module=self.call_module,
            call_function='set_validator_count',
            call_params={
                'new': new,
            }
        )

        return call

    def set_invulnerables(self, invulnerables):
        """
        {'call_name': 'set_invulnerables',
        'call_args': [{'name': 'invulnerables', 'type': 55, 'typeName': 'Vec<T::AccountId>', 'docs': []}],
        'documentation': 'Set the validators who cannot be slashed (if any).
        The dispatch origin must be Root.
        # <weight>
        - O(V)\n- Write: Invulnerables
        # </weight>',
        'module_prefix': 'Staking', 'module_name': 'Staking', 'spec_version': 9122}
        :return:
        """

        call = self.substrate.compose_call(
            call_module=self.call_module,
            call_function='set_invulnerables',
            call_params={
                'invulnerables': invulnerables,
            }
        )

        return call

    def set_staking_limits(self, min_nominator_bond, min_validator_bond, max_nominator_count, max_validator_count,
                           threshold):
        """
        {'call_name': 'set_staking_limits',
        'call_args': [
        {'name': 'min_nominator_bond', 'type': 6, 'typeName': 'BalanceOf<T>', 'docs': []},
        {'name': 'min_validator_bond', 'type': 6, 'typeName': 'BalanceOf<T>', 'docs': []},
        {'name': 'max_nominator_count', 'type': 158, 'typeName': 'Option<u32>', 'docs': []},
        {'name': 'max_validator_count', 'type': 158, 'typeName': 'Option<u32>', 'docs': []},
        {'name': 'threshold', 'type': 159, 'typeName': 'Option<Percent>', 'docs': []}],
        'documentation': 'Update the various staking limits this pallet.
        * `min_nominator_bond`: The minimum active bond needed to be a nominator.
        * `min_validator_bond`: The minimum active bond needed to be a validator.
        * `max_nominator_count`: The max number of users who can be a nominator at once.
        When set to `None`, no limit is enforced.
        * `max_validator_count`: The max number of users who can be a validator at once. W
        hen  set to `None`, no limit is enforced.
        Origin must be Root to call this function.
        NOTE: Existing nominators and validators will not be affected by this update.
        to kick people under the new limits, `chill_other` should be called.',
        'module_prefix': 'Staking', 'module_name': 'Staking', 'spec_version': 9122}
        :return:
        """

        call = self.substrate.compose_call(
            call_module=self.call_module,
            call_function='set_staking_limits',
            call_params={
                'min_nominator_bond': min_nominator_bond,
                'min_validator_bond': min_validator_bond,
                'max_nominator_count': max_nominator_count,
                'max_validator_count': max_validator_count,
                'threshold': threshold,
            }
        )

        return call
