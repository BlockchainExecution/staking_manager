from code_src.staking.dot.fxn_decorator_implementations.accountImplementation import DotAccountCall
from common import MyHelpFormatter
from examples import exampleCreateMnemonic, exampleCreateAccount, exampleAccountInfos, exampleCreateKeypair, \
    exampleStaker
from code_src.staking.dot.dotArgparserUtil import actionHelp, subcommand, actionSeed, actionControllerAddress

"""
TODO:
* This file and all references (i.e. cli cmds) need to be renamed accountingArgParser -> accountArgParser
* "accounting" is kind of incorrect english and is therefore confusing to the user, "account" is correct

"""

def accountingArgParser(parent_parser):
    # bounder parent parser
    accountingDotParser = parent_parser.add_parser(name="accounting",
                                                   help="accounting interface to DOT.",
                                                   add_help=False, epilog=exampleStaker,
                                                   formatter_class=MyHelpFormatter)

    accountingDotSubParser = accountingDotParser.add_subparsers(help='')

    # create mnemonic
    @subcommand(parent=accountingDotSubParser, subHelp="create a mnemonic phrase.", epilog=exampleCreateMnemonic,
                optArgs=[actionHelp()])
    def mnemonic(args):
        @DotAccountCall()
        def mnemonic():
            pass

    # create_keypair
    @subcommand(parent=accountingDotSubParser, subHelp="get an address from a mnemonic", epilog=exampleCreateKeypair,
                reqArgs=[actionSeed()],
                optArgs=[actionHelp()])
    def keypair(args):
        @DotAccountCall(mnemonic=args.seed)
        def keypair():
            pass

    # account_infos
    @subcommand(parent=accountingDotSubParser, subHelp="get the info of an account (i.e. an address)", epilog=exampleAccountInfos,
                reqArgs=[actionControllerAddress()],
                optArgs=[actionHelp()])
    def info(args):
        @DotAccountCall(ss58_address=args.controller_address)
        def info():
            pass

    # create_account
    @subcommand(parent=accountingDotSubParser, subHelp="create an account.", epilog=exampleCreateAccount,
                optArgs=[actionHelp()])
    def create(args):
        @DotAccountCall()
        def create():
            pass

    return accountingDotParser
