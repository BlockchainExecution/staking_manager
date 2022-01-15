from code_src.staking.cosmos.fxn_decorator_implementations.accountImplementation import AtomAccountCall
from code_src.staking.polkadotAndKusama.argparserUtil import actionControllerAddress, actionHelp, actionDerivationPath
from common import MyHelpFormatter
from examples import exampleAccount, exampleAccountInfos, exampleCreateAccount
from code_src.staking.polkadotAndKusama.argparserUtil import actionHelp, subcommand, actionMnemonic, \
    actionControllerAddress


def atomAccountArgParser(parent_parser):
    # bounder parent parser
    accountAtomParser = parent_parser.add_parser(name="account",
                                                 help=f"account interface to Cosmos.",
                                                 add_help=False, epilog=exampleAccount,
                                                 formatter_class=MyHelpFormatter)

    accountAtomSubParser = accountAtomParser.add_subparsers(help='')

    # account_infos
    @subcommand(parent=accountAtomSubParser, subHelp="get an account info.", epilog=exampleAccountInfos,
                reqArgs=[actionControllerAddress()],
                optArgs=[actionHelp()])
    def info(args):
        @AtomAccountCall(address=args.controller_address)
        def info():
            pass

    # create_account
    @subcommand(parent=accountAtomSubParser, subHelp="create an account.", epilog=exampleCreateAccount,
                optArgs=[actionHelp()])
    def create(args):
        @AtomAccountCall()
        def create():
            pass

    @subcommand(parent=accountAtomSubParser, subHelp="create an account.", epilog=exampleCreateAccount,
                reqArgs=[actionMnemonic(), actionDerivationPath()],
                optArgs=[actionHelp()])
    def keypair(args):
        @AtomAccountCall(mnemonic=args.mnemonic, derivation_path=args.derivation_path)
        def keypair():
            pass

    return accountAtomParser
