from code_src.staking.dot.dotArgparserUtil import actionSeed, actionNumberOfTokens, actionControllerAddress, \
    actionRewardsDestination, \
    actionValidatorAddress, actionHelp, subcommand
from code_src.staking.dot.fxn_decorator_implementations.substrateCallImplementation import DotSubstrateCall

from examples import exampleStaker


def stakeDotArgParser(parent_parser):
    # bounder parent parser
    @subcommand(parent=parent_parser,
                subHelp="automatically prepare coins and send them to be staked (bond coin then nominate a validator).",
                epilog=exampleStaker, reqArgs=[actionSeed(), actionControllerAddress(), actionNumberOfTokens()],
                optArgs=[actionRewardsDestination(), actionValidatorAddress(), actionHelp()])
    def staker(args):
        @DotSubstrateCall(cli_name="Bounder", call_module="Staking",
                          call_params={'controller': args.controller_address, 'value': args.number_of_tokens,
                                       'payee': args.rewards_destination}, seed=args.seed)
        def bond():
            pass

        @DotSubstrateCall(cli_name="Nominator", call_module="Staking", call_params={'targets': args.validator_address},
                          seed=args.seed)
        def nominate():
            pass
