# actions
# parser arguments

# TODO find a way to pass action as string to add_argument command

def actionSeed(parser_in):
    parser_in.add_argument('-s', '--seed',
                           help='mnemonic phrase is a group words, often 12 or more, created when a new wallet is made.'
                                'to store your cryptocurrency.', required=True
                           )


def actionControllerAddress(parser_in):
    parser_in.add_argument('-ca', '--controller_address',
                           help="""
An address you would like to bond to the stash account. Stash and Controller can be the same address but it is not recommended since it defeats the security of the two-account staking model.!""",
                           required=True, type=str
                           )


def actionNumberOfTokens(parser_in):
    parser_in.add_argument('-nt', '--number_of_tokens',
                           help='The number of DOT you would like to stake to the network.',
                           required=True,
                           type=int
                           )


def actionRewardsDestination(parser_in):
    parser_in.add_argument('-rd', '--rewards_destination',
                           help="""
Choices supports the following:
  staked    - Pay into the stash account, increasing the amount at stake accordingly.
  stash       - Pay into the stash account, not increasing the amount at stake.
  account     - Pay into a custom account, like so: Account DMTHrNcmA8QbqRS4rBq8LXn8ipyczFoNMb1X4cY2WD9tdBX.
  controller  - Pay into the controller account.
""",
                           default="staked",
                           choices=["staked", "stash", "account", "controller"],
                           required=False,
                           type=str.lower
                           )


def actionValidatorAddress(parser_in):
    parser_in.add_argument('-va', '--validator_address',
                           help="""
Address of a Polkadot validators (where to stake coins).It can be one or more address. By default binance validator address will be chosen.
                                    """,
                           default=["114SUbKCXjmb9czpWTtS3JANSmNRwVa4mmsMrWYpRG1kDH5"],
                           nargs="*",
                           required=False,
                           )


def actionHelp(parser_in):
    parser_in.add_argument("-h", "--help", action="help", help="show this help message and exit")

# TODO add a decorator for ArgParser functions and remove repeated code
#   hint: code is already 50% done and is commented as decoratorFuncArgParser function


"""def decoratorFuncArgParser(bounderSubParser, example, name, help_in, actions={}):
    parserFunc = bounderSubParser.add_parser(name, help=help_in,
                                             add_help=False, epilog=example,
                                             formatter_class=argparse.RawDescriptionHelpFormatter)

    parserFunc.set_defaults(func=name)
    parserFunc._action_groups.pop()

    parserFuncRequiredArguments = parserFunc.add_argument_group('required arguments')
    parserFuncOptionalArguments = parserFunc.add_argument_group('optional arguments')"""
