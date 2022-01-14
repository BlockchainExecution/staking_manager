from common import MyHelpFormatter


def argument(*name_or_flags, **kwargs):
    """Convenience function to properly format arguments to pass to the
    subcommand decorator.
    """
    return [*name_or_flags], kwargs


def subcommand(parent, subHelp="", epilog="", reqArgs=None, optArgs=None):
    if reqArgs is None:
        reqArgs = []

    def decorator(func):
        parser = parent.add_parser(func.__name__, description=func.__doc__, add_help=False, help=subHelp,
                                   formatter_class=MyHelpFormatter, epilog=epilog)
        # myLogger("decorator").info(parser)
        requiredArguments = parser.add_argument_group('required arguments')
        optionalArguments = parser.add_argument_group('optional arguments')
        # myLogger("decorator").info(func.__name__)
        # parser._action_groups.pop()
        for rArg in reqArgs:
            # myLogger("decorator").info(rArg)
            requiredArguments.add_argument(*rArg[0], **rArg[1])
        for oArg in optArgs:
            # myLogger("decorator").info(oArg)
            optionalArguments.add_argument(*oArg[0], **oArg[1])
        parser.set_defaults(func=func)

    return decorator


def actionNumSlashingSpans():
    return argument('-nss', '--num_slashing_spans', help="?", default=0,
                    required=False, type=int)


def actionMnemonic():
    return argument('-m', '--mnemonic',
                    help='mnemonic phrase is a group words, often 12 or more,\ncreated when a new wallet is made.\n''to store your cryptocurrency.\n\n',
                    required=True)


def actionControllerAddress():
    return argument('-ca', '--controller_address',
                    help="""An address you would like to bond to the stash account.\nStash and Controller can be the same address but it is not recommended\nsince it defeats the security of the two-account staking model.!\n\n""",
                    required=True, type=str
                    )


def actionDerivationPath():
    return argument('-dp', '--derivation_path',
                    help="""the key type and sequence number refer to the segment of the BIP44 derivation path (for example, 0, 1, 2, ...) that is used to derive a private and a public key from the mnemonic!\n\n""",
                    required=True, type=str
                    )



def actionNumberOfTokens():
    return argument('-nt', '--number_of_tokens',
                    help='The number of DOT you would like to stake to the network.\n',
                    required=True,
                    type=float
                    )


def actionRewardsDestination():
    return argument('-rd', '--rewards_destination',
                    help="""
Choices supports the following:
  staked    - Pay into the stash account, increasing the amount at stake accordingly.
  stash       - Pay into the stash account, not increasing the amount at stake.
  account     - Pay into a custom account, for example: Account DMTHrNcmA8QbqRS4rBq8LXn8ipyczFoNMb1X4cY2WD9tdBX.
  controller  - Pay into the controller account.\n
""",
                    default="Staked",
                    choices=["Staked", "Stash", "Account", "Controller"],
                    required=False,
                    type=str
                    )


def actionValidatorAddress(activeConfig):
    return argument('-va', '--validator_address',
                    help="""
Address of a Polkadot validators (where to stake coins). It can be one or more address.\nBy default binance validator address will be chosen.\n
                                    """,
                    default=activeConfig.activeValidator,
                    nargs="*",
                    required=False,
                    )


def actionHelp():
    return argument("-h", "--help", action="help", help="show this help message and exit")


def actionTest():
    return argument("-h", "--help", action="help", help="show this help message and exit")
