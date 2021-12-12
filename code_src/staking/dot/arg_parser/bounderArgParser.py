from code_src.staking.dot.fxn_decorator_implementations.substrateCallImplementation import DotSubstrateCall
from common import MyHelpFormatter
from code_src.staking.dot.dotArgparserUtil import actionMnemonic, actionNumberOfTokens, actionControllerAddress, \
    actionRewardsDestination, \
    actionValidatorAddress, actionHelp, subcommand, actionNumSlashingSpans
from examples import exampleBond, exampleBounder, exampleBoundExtra, exampleReBound, exampleWithdrawUnBonded


def bounderArgParser(parent_parser):
    # bounder
    # bounder parent parser
    bounderParser = parent_parser.add_parser("bounder", help="bond interface to DOT.", epilog=exampleBounder,
                                             formatter_class=MyHelpFormatter)
    bounderSubParser = bounderParser.add_subparsers(help='')

    # bond
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
    - O(1).
    - Three extra DB entries.
    NOTE:Two of the storage writes (`Self::bonded`, `Self::payee`) are _never_ cleaned
    unless the `origin` falls below _existential deposit_ and gets removed as dust.
    # </weight>',
    'module_prefix': 'Staking','module_name': 'Staking', 'spec_version': 9122}
    :return:
    """

    @subcommand(parent=bounderSubParser,
                subHelp="Take the origin account as a stash and lock up `value` of its balance. `controller` will be the account that controls it.",
                epilog=exampleBond, reqArgs=[actionMnemonic(), actionControllerAddress(), actionNumberOfTokens()],
                optArgs=[actionRewardsDestination(), actionValidatorAddress(), actionHelp()])
    def bond(args):
        @DotSubstrateCall(cli_name="Bounder", call_module="Staking",
                          call_params={'controller': args.controller_address, 'value': args.number_of_tokens,
                                       'payee': args.rewards_destination}, seed=args.mnemonic)
        def bond():
            pass

    # unbound
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

    @subcommand(parent=bounderSubParser,
                subHelp="Schedule a portion of the stash to be unlocked ready for transfer out after the bond period ends.",
                epilog=exampleBond, reqArgs=[actionMnemonic(), actionNumberOfTokens()],
                optArgs=[actionHelp()])
    def unbond(args):
        @DotSubstrateCall(cli_name="Bounder", call_module="Staking",
                          call_params={'value': args.number_of_tokens}, seed=args.mnemonic)
        def unbond():
            """
            - Invalid subscription id
            - Transaction is temporarily banned
            """

            pass

    # rebond
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

    @subcommand(parent=bounderSubParser,
                subHelp="Rebond a portion of the stash scheduled to be unlocked.",
                epilog=exampleReBound, reqArgs=[actionMnemonic(), actionNumberOfTokens()],
                optArgs=[actionRewardsDestination(), actionValidatorAddress(), actionHelp()])
    def rebond(args):
        @DotSubstrateCall(cli_name="Bounder", call_module="Staking",
                          call_params={'value': args.number_of_tokens}, seed=args.mnemonic)
        def rebond():
            pass

    # bond extra
    """
    {'call_name': 'bond_extra', 'call_args':
     [{'name': 'max_additional', 'type': 51, 'typeName': 'BalanceOf<T>',
     'docs': []}], 'documentation': 'Add some extra amount that have appeared in the stash `free_balance` into the
     balance up for staking.
     The dispatch origin for this call must be _Signed_ by the stash, not the controller.
     Use this if there are additional funds in your stash account that you wish to bond.
     Unlike [`bond`] (Self::bond) or [`unbond`](Self::unbond) this function does not imposeany limitation 
     on the amount that can be added.
     Emits `Bonded`.# <weight>- Independent of the arguments. Insignificant complexity.-O(1).
     # </weight>', 'module_prefix': 'Staking', 'module_name': 'Staking', 'spec_version': 9122}
    :return:
    """

    @subcommand(parent=bounderSubParser,
                subHelp="Add some extra amount that have appeared in the stash `free_balance` into the balance up for staking.",
                epilog=exampleBoundExtra, reqArgs=[actionMnemonic(), actionNumberOfTokens()],
                optArgs=[actionRewardsDestination(), actionValidatorAddress(), actionHelp()])
    def bondextra(args):
        @DotSubstrateCall(cli_name="Bounder", call_module="Staking",
                          call_params={'value': args.number_of_tokens}, seed=args.mnemonic)
        def bond_extra():
            pass

    # TODO understand better num_slashing_spans
    # withdraw unbounded
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

    @subcommand(parent=bounderSubParser,
                subHelp="Remove any unlocked chunks from the `unlocking` queue. This essentially frees up that balance "
                        "to be used by the stash account to do whatever it wants.",
                epilog=exampleWithdrawUnBonded, reqArgs=[actionMnemonic(), actionNumSlashingSpans()],
                optArgs=[actionHelp()])
    def withdrawunbonded(args):
        @DotSubstrateCall(cli_name="Bounder", call_module="Staking",
                          call_params={'num_slashing_spans': args.num_slashing_spans}, seed=args.mnemonic)
        def withdraw_unbonded():
            pass

    return bounderParser
