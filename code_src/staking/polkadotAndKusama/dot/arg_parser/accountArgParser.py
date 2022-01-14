from code_src.staking.polkadotAndKusama.fxn_decorator_implementations.accountImplementation import DotAccountCall
from common import MyHelpFormatter
from examples import exampleCreateMnemonic, exampleCreateAccount, exampleAccountInfos, exampleCreateKeypair, \
    exampleAccount
from code_src.staking.polkadotAndKusama.argparserUtil import actionHelp, subcommand, actionMnemonic, actionControllerAddress


def accountArgParser(parent_parser, coin):
    # bounder parent parser
    accountDotParser = parent_parser.add_parser(name="account",
                                                help=f"account interface to {coin}.",
                                                add_help=False, epilog=exampleAccount,
                                                formatter_class=MyHelpFormatter)

    accountDotSubParser = accountDotParser.add_subparsers(help='')

    # create mnemonic
    @subcommand(parent=accountDotSubParser, subHelp="create a mnemonic phrase.", epilog=exampleCreateMnemonic,
                optArgs=[actionHelp()])
    def mnemonic(args):
        @DotAccountCall()
        def mnemonic():
            pass

    # create_keypair
    @subcommand(parent=accountDotSubParser, subHelp="create a key pair from seed", epilog=exampleCreateKeypair,
                reqArgs=[actionMnemonic()],
                optArgs=[actionHelp()])
    def keypair(args):
        @DotAccountCall(mnemonic=args.mnemonic)
        def keypair():
            pass

    # account_infos
    @subcommand(parent=accountDotSubParser, subHelp="get an account info.", epilog=exampleAccountInfos,
                reqArgs=[actionControllerAddress()],
                optArgs=[actionHelp()])
    def info(args):
        @DotAccountCall(ss58_address=args.controller_address)
        def info():
            pass

    # create_account
    @subcommand(parent=accountDotSubParser, subHelp="create an account.", epilog=exampleCreateAccount,
                optArgs=[actionHelp()])
    def create(args):
        @DotAccountCall()
        def create():
            pass

    return accountDotParser
