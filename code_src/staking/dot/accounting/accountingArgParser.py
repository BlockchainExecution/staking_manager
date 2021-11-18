import argcomplete

from code_src.staking.dot.accounting.accountingModule import Accounting
from common import MyHelpFormatter, active_substrate
from examples import exampleCreateMnemonic, exampleCreateAccount, exampleAccountInfos, exampleCreateKeypair, \
    exampleStaker
from code_src.staking.dot.dotArgparserUtil import actionHelp, subcommand, actionSeed, actionControllerAddress


def accountingArgParser(parent_parser):
    account = Accounting()
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
        return account.createMnemonic()

    # create_keypair
    @subcommand(parent=accountingDotSubParser, subHelp="create a key pair from seed", epilog=exampleCreateKeypair,
                reqArgs=[actionSeed()],
                optArgs=[actionHelp()])
    def keypair(args):
        seed = args.seed
        return account.createKeypair(seed)

    # account_infos
    @subcommand(parent=accountingDotSubParser, subHelp="get an account info.", epilog=exampleAccountInfos,
                reqArgs=[actionControllerAddress()],
                optArgs=[actionHelp()])
    def info(args):
        ss58_address = args.controller_address
        return account.getAccountInfos(active_substrate=active_substrate, ss58_address=ss58_address)

    # create_account
    @subcommand(parent=accountingDotSubParser, subHelp="create an account.", epilog=exampleCreateAccount,
                optArgs=[actionHelp()])
    def create(args):
        return account.createAccount()

    argcomplete.autocomplete(accountingDotSubParser)

    return accountingDotParser
