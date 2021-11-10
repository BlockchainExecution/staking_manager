from common import active_substrate


class Setter(object):
    def __init__(self):
        self.call_module = "Staking"
        self.substrate = active_substrate

    def set_payee(self, payee_addr):
        """
        {'call_name': 'set_payee',
        'call_args': [{'name': 'payee', 'type': 152, 'typeName': 'RewardDestination<T::AccountId>', 'docs': []}],
        'documentation': '(Re-)set the payment target for a controller.
        Effects will be felt at the beginning of the next era.
        The dispatch origin for this call must be _Signed_ by the controller, not the stash.
        # <weight>
        - Independent of the arguments. Insignificant complexity.
        - Contains a limited number of reads.
        - Writes are limited to the `origin` account key.
        - Weight: O(1)\n- DB Weight:
        - Read: Ledger
        - Write: Payee
        # </weight>',
        'module_prefix': 'Staking', 'module_name': 'Staking', 'spec_version': 9122}
        :param payee_addr:
        :return:
        """

        call = self.substrate.compose_call(
            call_module=self.call_module,
            call_function='set_payee',
            call_params={
                'payee': payee_addr,
            }
        )

        return call


    def set_controller(self,controller_addr):
        """
        {'call_name': 'set_controller',
        'call_args': [{'name': 'controller', 'type': 147, 'typeName': '<T::Lookup as StaticLookup>::Source', 'docs': []}],
         'documentation': '(Re-)set the controller of a stash.
         Effects will be felt at the beginning of the next era.
         The dispatch origin for this call must be _Signed_ by the stash, not the controller.
         # <weight>
         - Independent of the arguments. Insignificant complexity.
         - Contains a limited number of reads.
         - Writes are limited to the `origin` account key.
         Weight: O(1)\nDB Weight:
         - Read: Bonded, Ledger New Controller, Ledger Old Controller
         - Write: Bonded, Ledger New Controller, Ledger Old Controller
         # </weight>',
         'module_prefix': 'Staking', 'module_name': 'Staking', 'spec_version': 9122}
        :param controller_addr:
        :return:
        """

        call = self.substrate.compose_call(
            call_module=self.call_module,
            call_function='set_payee',
            call_params={
                'payee': controller_addr,
            }
        )

        return call