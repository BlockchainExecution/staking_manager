from common import active_substrate


class Nominate(object):

    def __init__(self, targets):
        self.call_module = "Staking"
        self.substrate = active_substrate
        self.targets = targets

    def nominate(self):
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

        call = self.substrate.compose_call(
            call_module=self.call_module,
            call_function='nominate',
            call_params={
                'targets': self.targets,
            }
        )

        return call
