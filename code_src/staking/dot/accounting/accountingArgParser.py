import argcomplete
from common import MyHelpFormatter

from code_src.staking.dot.dotArgparserUtil import actionHelp


def createMnemonicArgParser(accountingSubParser):
    exampleCreateMnemonic = """
description : 
  create Mnemonic dot

example:
  python %(prog)s create_mnemonic \n
    """
    createMnemonicParser = accountingSubParser.add_parser("mnemonic", help="""
create a mnemonic phrase , created new wallet.""",
                                                          add_help=False, epilog=exampleCreateMnemonic,
                                                          formatter_class=MyHelpFormatter)
    createMnemonicParser.set_defaults(func="mnemonic")
    createMnemonicParser._action_groups.pop()

    # bound extra group
    createMnemonicOptionalArguments = createMnemonicParser.add_argument_group('optional arguments')
    actionHelp(createMnemonicOptionalArguments)


def createKeypairArgParser(accountingSubParser):
    exampleCreateKeypair = """
description : 
  create Keypair dot

example:
  python %(prog)s keypair -m/--mnemonic "MNEMONIC" \n
    """
    createKeypairParser = accountingSubParser.add_parser("keypair", help="""
get keypair from mnemonic.""",
                                                         add_help=False, epilog=exampleCreateKeypair,
                                                         formatter_class=MyHelpFormatter)
    createKeypairParser.set_defaults(func="keypair")
    createKeypairParser._action_groups.pop()

    # bound extra group
    createKeypairParserRequiredArguments = createKeypairParser.add_argument_group('required arguments')
    createKeypairParserOptionalArguments = createKeypairParser.add_argument_group('optional arguments')

    createKeypairParserRequiredArguments.add_argument("-m", "--mnemonic",
                                                      help="mnemonic phrase is a group words, often 12 or more, created when a new wallet is made",
                                                      type=str, required=True)
    actionHelp(createKeypairParserOptionalArguments)


def accountInfosArgParser(accountingSubParser):
    exampleAccountInfos = """
description : 
  accountInfos dot

example:
  python %(prog)s info \n
    """
    createMnemonicParser = accountingSubParser.add_parser("info", help="""
get account info.""",
                                                          add_help=False, epilog=exampleAccountInfos,
                                                          formatter_class=MyHelpFormatter)
    createMnemonicParser.set_defaults(func="info")
    createMnemonicParser._action_groups.pop()

    # bound extra group
    createMnemonicRequiredArguments = createMnemonicParser.add_argument_group('required arguments')
    createMnemonicOptionalArguments = createMnemonicParser.add_argument_group('optional arguments')

    createMnemonicRequiredArguments.add_argument("-a", "--address",
                                                 help="dot address (ss58_address).",
                                                 type=str, required=True)

    actionHelp(createMnemonicOptionalArguments)


def createAccountArgParser(accountingSubParser):
    exampleAccountInfos = """
description : 
  createAccount dot

example:
  python %(prog)s info \n
        """
    createAccountParser = accountingSubParser.add_parser("create", help="""
create a new wallet.""",
                                                         add_help=False, epilog=exampleAccountInfos,
                                                         formatter_class=MyHelpFormatter)
    createAccountParser.set_defaults(func="create")
    createAccountParser._action_groups.pop()

    # bound extra group
    createMnemonicOptionalArguments = createAccountParser.add_argument_group('optional arguments')
    actionHelp(createMnemonicOptionalArguments)


def accountingArgParser(parent_parser):
    # stake dot
    exampleStaker = """
Description
  Accounting interface to Polkadot..

example:
  python %(prog)s create -h
  python %(prog)s info -h
  python %(prog)s mnemonic -h
  python %(prog)s keypair -h
    """
    # bounder parent parser
    accountingDotParser = parent_parser.add_parser(name="accounting",
                                                   help="accounting interface to DOT.",
                                                   add_help=False, epilog=exampleStaker,
                                                   formatter_class=MyHelpFormatter)

    accountingDotSubParser = accountingDotParser.add_subparsers(help='')

    # create mnemonic
    createMnemonicArgParser(accountingDotSubParser)

    # create_keypair
    createKeypairArgParser(accountingDotSubParser)

    # account_infos
    accountInfosArgParser(accountingDotSubParser)

    # create_account
    createAccountArgParser(accountingDotSubParser)
    argcomplete.autocomplete(accountingDotSubParser)

    return accountingDotParser
