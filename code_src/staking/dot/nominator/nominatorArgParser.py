import argcomplete
from common import MyHelpFormatter

from code_src.staking.dot.dotArgparserUtil import actionSeed, actionValidatorAddress, actionHelp


def nominateArgParser(nominatorSubParser):
    example_bondextra = """
description : 
  nominate dot coin

example:
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -va/--validator_address VALIDATOR_ADDRESS \n
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -va/--validator_address VALIDATOR_ADDRESS_1,VALIDATOR_ADDRESS_2,VALIDATOR_ADDRESS_N \n
    """
    nominateParser = nominatorSubParser.add_parser("nominate", help="""
Declare the desire to nominate `targets` for the origin controller. Effects will be felt at the beginning of the next era.""",
                                                   add_help=False, epilog=example_bondextra,
                                                   formatter_class=MyHelpFormatter)
    nominateParser.set_defaults(func="nominate")
    nominateParser._action_groups.pop()

    # bound extra group
    nominateRequiredArguments = nominateParser.add_argument_group('required arguments')
    nominateOptionalArguments = nominateParser.add_argument_group('optional arguments')

    actionSeed(nominateRequiredArguments)
    actionValidatorAddress(nominateOptionalArguments)
    actionHelp(nominateOptionalArguments)


# TODO check the right wat to unnominate
def unNominateArgParser(nominatorSubParser):
    example_bondextra = """
description : 
  unnominate dot coin

example:
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -va/--validator_address VALIDATOR_ADDRESS \n
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -va/--validator_address VALIDATOR_ADDRESS_1,VALIDATOR_ADDRESS_2,VALIDATOR_ADDRESS_N \n
    """
    unNominateParser = nominatorSubParser.add_parser("unnominate", help="""
not ready yet""",
                                                     add_help=False, epilog=example_bondextra,
                                                     formatter_class=MyHelpFormatter)
    unNominateParser.set_defaults(func="unnominate")
    unNominateParser._action_groups.pop()

    # bound extra group
    unNominateRequiredArguments = unNominateParser.add_argument_group('required arguments')
    unNominateOptionalArguments = unNominateParser.add_argument_group('optional arguments')

    actionSeed(unNominateRequiredArguments)
    actionValidatorAddress(unNominateRequiredArguments)
    actionHelp(unNominateOptionalArguments)


def nominatorArgParser(parser_parent):
    # dotSubParser
    # nominator
    exampleNominate = """
Note: 
You need to bond you dot coin before you can use nominate option.
python stake dot bounder -h for more information

example:
    python %(prog)s -s/--seed "MNEMONIC_PHRASE"
    python %(prog)s -s/--seed "MNEMONIC_PHRASE" -va/--validator_address "VALIDATOR_ADDRESS"
    python %(prog)s -s/--seed "MNEMONIC_PHRASE" -va/--validator_address "VALIDATOR_ADDRESS_1","VALIDATOR_ADDRESS_2","VALIDATOR_ADDRESS_N"

    """
    # nominator parent parser
    nominatorParser = parser_parent.add_parser(name="nominator", help="""nomination interface to DOT.""",
                                               add_help=False, epilog=exampleNominate,
                                               formatter_class=MyHelpFormatter)

    nominatorSubParser = nominatorParser.add_subparsers(help='')
    # nominate
    nominateArgParser(nominatorSubParser)
    # un nominate
    unNominateArgParser(nominatorSubParser)

    # auto complete
    argcomplete.autocomplete(nominatorSubParser)

    return nominatorParser
