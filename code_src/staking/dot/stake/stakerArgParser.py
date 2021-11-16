from code_src.staking.dot.dotArgparserUtil import actionSeed, actionNumberOfTokens, actionControllerAddress, \
    actionRewardsDestination, \
    actionValidatorAddress, actionHelp
from common import MyHelpFormatter


def stakeDotArgParser(parent_parser):
    # TODO fix example_staker display
    # stake dot
    exampleStaker = """
Description\n
  This script will bond and nominate DOT to a validator.\n

example:\n
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -ca/--controller_address "CONTROLLER_ADDRESS" -nt/--number_of_tokens NUMBER_OF_TOKENS\n
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -ca/--controller_address "CONTROLLER_ADDRESS" -nt/--number_of_tokens NUMBER_OF_TOKENS -rd/--rewards_destination "REWARD_DESTINATION"\n
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -ca/--controller_address "CONTROLLER_ADDRESS" -nt/--number_of_tokens NUMBER_OF_TOKENS -va/--validator_address "VALIDATOR_ADDRESS"\n
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -ca/--controller_address "CONTROLLER_ADDRESS" -nt/--number_of_tokens NUMBER_OF_TOKENS -va/--validator_address "VALIDATOR_ADDRESS_1","VALIDATOR_ADDRESS_2","VALIDATOR_ADDRESS_N"\n
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -ca/--controller_address "CONTROLLER_ADDRESS" -nt/--number_of_tokens NUMBER_OF_TOKENS -rd/--rewards_destination "REWARD_DESTINATION" -va/--validator_address "VALIDATOR_ADDRESS"\n
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -ca/--controller_address "CONTROLLER_ADDRESS" -nt/--number_of_tokens NUMBER_OF_TOKENS -rd/--rewards_destination "REWARD_DESTINATION" -va/--validator_address "VALIDATOR_ADDRESS_1","VALIDATOR_ADDRESS_2","VALIDATOR_ADDRESS_N"\n
    """
    # bounder parent parser
    stakeDotParser = parent_parser.add_parser(name="staker",
                                              help="automatically prepare coins and send them to be staked (bond coin then nominate a validator).",
                                              add_help=False, epilog=exampleStaker,
                                              formatter_class=MyHelpFormatter)
    stakeDotParser.set_defaults(func="staker")
    stakeDotParser._action_groups.pop()

    stakeDotRequiredArguments = stakeDotParser.add_argument_group('required arguments')
    stakeDotOptionalArguments = stakeDotParser.add_argument_group('optional arguments')

    # seed
    actionSeed(stakeDotRequiredArguments)
    # ca
    actionControllerAddress(stakeDotRequiredArguments)
    # nt
    actionNumberOfTokens(stakeDotRequiredArguments)
    # rd
    actionRewardsDestination(stakeDotOptionalArguments)
    # va
    actionValidatorAddress(stakeDotOptionalArguments)
    # help
    actionHelp(stakeDotOptionalArguments)

    return stakeDotParser
