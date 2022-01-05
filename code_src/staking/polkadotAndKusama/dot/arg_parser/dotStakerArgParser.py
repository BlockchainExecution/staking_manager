from code_src.staking.polkadotAndKusama.argparserUtil import actionMnemonic, actionNumberOfTokens, \
    actionControllerAddress, \
    actionRewardsDestination, \
    actionValidatorAddress, actionHelp, subcommand
from code_src.staking.polkadotAndKusama.fxn_decorator_implementations.substrateCallImplementation import \
    SubstrateCall
from config import DotActiveConfig
from examples import exampleStaker


def dotStakeDotArgParser(parent_parser):
    # bounder parent parser
    @subcommand(parent=parent_parser,
                subHelp="automatically prepare coins and send them to be staked (bond coin then nominate a validator).",
                epilog=exampleStaker, reqArgs=[actionMnemonic(), actionControllerAddress(), actionNumberOfTokens()],
                optArgs=[actionRewardsDestination(), actionValidatorAddress(DotActiveConfig), actionHelp()])
    def stake(args):
        @SubstrateCall(config=DotActiveConfig, cli_name="Bounder", call_module="Staking",
                       call_params={'controller': args.controller_address, 'value': args.number_of_tokens,
                                    'payee': args.rewards_destination, 'targets': args.validator_address},
                       seed=args.mnemonic)
        def stake():
            pass
