from common import active_substrate


class Chill(object):
    def __init__(self, controller_addr):
        self.substrate = active_substrate
        self.controller_addr = controller_addr

    def chill(self):
        """
        {'call_name': 'chill',
        'call_args': [],
        'documentation': 'Declare no desire to either validate or nominate.
        Effects will be felt at the beginning of the next era.
        The dispatch origin for this call must be _Signed_ by the controller, not the stash.
        # <weight>
        - Independent of the arguments. Insignificant complexity.
        - Contains one read.\n- Writes are limited to the `origin` account key.
        # </weight>',
        'module_prefix': 'Staking', 'module_name': 'Staking', 'spec_version': 9122}
        :return:
        """
        call = self.substrate.compose_call(
            call_module='Staking',
            call_function='chill',
        )

        return call

    def chill_other(self):
        """
        {'call_name': 'chill_other',
        'call_args': [{'name': 'controller', 'type': 0, 'typeName': 'T::AccountId', 'docs': []}],
        'documentation': 'Declare a `controller` to stop participating as either a validator or nominator.
        Effects will be felt at the beginning of the next era.
        The dispatch origin for this call must be _Signed_, but can be called by anyone.
        If the caller is the same as the controller being targeted, then no further checks are
        enforced, and this function behaves just like `chill`.
        If the caller is different than the controller being targeted, the following conditions
        must be met:\n* A `ChillThreshold` must be set and checked which defines how close to the max
          nominators or validators we must reach before users can start chilling one-another.
          * A `MaxNominatorCount` and `MaxValidatorCount` must be set which is used to determine
            how close we are to the threshold.
          * A `MinNominatorBond` and `MinValidatorBond` must be set and checked, which determines
        if this is a person that should be chilled because they have not met the threshold
        bond required.
        This can be helpful if bond requirements are updated, and we need to remove old users
        who do not satisfy these requirements.',
        'module_prefix': 'Staking', 'module_name': 'Staking', 'spec_version': 9122}
        :return:
        """

        call = self.substrate.compose_call(
            call_module='Staking',
            call_function='chill',
            call_params={
                'controller': self.controller_addr,
            }
        )

        return call
