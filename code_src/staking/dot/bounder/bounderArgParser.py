import argcomplete
from common import MyHelpFormatter
from code_src.staking.dot.dotArgparserUtil import actionSeed, actionNumberOfTokens, actionControllerAddress, \
    actionRewardsDestination, \
    actionValidatorAddress, actionHelp


def bondArgParser(bounderSubParser):
    # example
    exampleBond = """
description : 
  bond dot coin before nomination

example:
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -ca/--controller_address CONTROLLER_ADDRESS -nt/--number_of_tokens NUMBER_OF_TOKENS \n
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -ca/--controller_address CONTROLLER_ADDRESS -nt NUMBER_OF_TOKENS -va/--validator_address VALIDATOR_ADDRESS \n
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -ca/--controller_address CONTROLLER_ADDRESS -nt NUMBER_OF_TOKENS -va/--validator_address VALIDATOR_ADDRESS_1,VALIDATOR_ADDRESS_2,VALIDATOR_ADDRESS_N \n

"""
    # func parser
    bondParser = bounderSubParser.add_parser("bond",
                                             help="""
Take the origin account as a stash and lock up `value` of its balance. `controller` will be the account that controls it.""",
                                             add_help=False, epilog=exampleBond,
                                             formatter_class=MyHelpFormatter)
    bondParser.set_defaults(func="bond")
    bondParser._action_groups.pop()

    # options
    # groups
    bondRequiredArguments = bondParser.add_argument_group('required arguments')
    bondOptionalArguments = bondParser.add_argument_group('optional arguments')

    # seed
    actionSeed(bondRequiredArguments)
    # ca
    actionControllerAddress(bondRequiredArguments)
    # nt
    actionNumberOfTokens(bondRequiredArguments)
    # rd
    actionRewardsDestination(bondOptionalArguments)
    # va
    actionValidatorAddress(bondOptionalArguments)
    # help
    actionHelp(bondOptionalArguments)


def unBoundArgParser(bounderSubParser):
    exampleUnBound = """
description : 
  unbound dot coin

example:
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -nt NUMBER_OF_TOKENS \n
"""
    # unbound func parser
    unboundParser = bounderSubParser.add_parser("unbound", help="""
Schedule a portion of the stash to be unlocked ready for transfer out after the bond period ends.""",
                                                add_help=False, epilog=exampleUnBound,
                                                formatter_class=MyHelpFormatter)
    unboundParser.set_defaults(func="unbound")
    unboundParser._action_groups.pop()
    # unbound groups
    unboundRequiredArguments = unboundParser.add_argument_group('required arguments')
    unboundOptionalArguments = unboundParser.add_argument_group('optional arguments')

    actionSeed(unboundRequiredArguments)
    actionNumberOfTokens(unboundRequiredArguments)
    actionHelp(unboundOptionalArguments)


def reBoundArgParser(bounderSubParser):
    exampleReBound = """
description : 
  rebound dot coin

example:
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -nt NUMBER_OF_TOKENS \n    
    """
    # rebound
    # rebound func parser
    reBoundParser = bounderSubParser.add_parser("rebound",
                                                help="""Rebond a portion of the stash scheduled to be unlocked.""",
                                                add_help=False, epilog=exampleReBound,
                                                formatter_class=MyHelpFormatter)
    reBoundParser.set_defaults(func="rebound")
    reBoundParser._action_groups.pop()
    # rebound group
    reBoundRequiredArguments = reBoundParser.add_argument_group('required arguments')
    reBoundOptionalArguments = reBoundParser.add_argument_group('optional arguments')

    actionSeed(reBoundRequiredArguments)
    actionNumberOfTokens(reBoundRequiredArguments)
    actionHelp(reBoundOptionalArguments)


def bondExtraArgParser(bounderSubParser):
    exampleBoundExtra = """
description : 
  boundextra dot coin

example:
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -nt NUMBER_OF_TOKENS \n
    """
    bondExtraParser = bounderSubParser.add_parser("boundextra", help="""
Add some extra amount that have appeared in the stash `free_balance` into the balance up for staking.""",
                                                  add_help=False, epilog=exampleBoundExtra,
                                                  formatter_class=MyHelpFormatter)
    bondExtraParser.set_defaults(func="boundextra")
    bondExtraParser._action_groups.pop()

    # bound extra group
    bondExtraRequiredArguments = bondExtraParser.add_argument_group('required arguments')
    bondExtraOptionalArguments = bondExtraParser.add_argument_group('optional arguments')

    actionSeed(bondExtraRequiredArguments)
    actionNumberOfTokens(bondExtraRequiredArguments)
    actionHelp(bondExtraOptionalArguments)


def withdrawUnBondedArgParser(bounderSubParser):
    exampleWithdrawUnBonded = """
description : 
  withdrawunbonded dot coin

example:
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -nt NUMBER_OF_TOKENS \n
    """
    withdrawUnBondedParser = bounderSubParser.add_parser("withdrawunbonded", help="""
Remove any unlocked chunks from the `unlocking` queue. This essentially frees up that balance to be
used by the stash account to do whatever it wants.""",
                                                         add_help=False, epilog=exampleWithdrawUnBonded,
                                                         formatter_class=MyHelpFormatter)
    withdrawUnBondedParser.set_defaults(func="withdrawunbounded")
    withdrawUnBondedParser._action_groups.pop()

    # bound extra group
    withdrawUnBondedExtraRequiredArguments = withdrawUnBondedParser.add_argument_group('required arguments')
    withdrawUnBondedExtraOptionalArguments = withdrawUnBondedParser.add_argument_group('optional arguments')

    actionSeed(withdrawUnBondedExtraRequiredArguments)
    actionNumberOfTokens(withdrawUnBondedExtraRequiredArguments)
    actionHelp(withdrawUnBondedExtraOptionalArguments)


def bounderArgParser(parent_parser):
    # bounder
    exampleBounder = """
description : 
  bounder interface.

example:
  python %(prog)s bond -h
  python %(prog)s unbond -h
  python %(prog)s rebond -h
  python %(prog)s bondextra -h
  python %(prog)s withdrawunbonded -h
  \n
"""
    # bounder parent parser
    bounderParser = parent_parser.add_parser("bounder", help="bond interface to DOT.", epilog=exampleBounder,
                                             formatter_class=MyHelpFormatter)
    bounderSubParser = bounderParser.add_subparsers(help='')

    # bond
    bondArgParser(bounderSubParser)
    # unbound
    unBoundArgParser(bounderSubParser)
    # rebond
    reBoundArgParser(bounderSubParser)
    # bond extra
    bondExtraArgParser(bounderSubParser)
    # withdraw unbounded
    withdrawUnBondedArgParser(bounderSubParser)

    # autocomplite
    argcomplete.autocomplete(bounderParser)

    return bounderParser
