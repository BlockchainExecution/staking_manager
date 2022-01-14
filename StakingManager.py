import argparse

from code_src.staking.cosmos.arg_parser.atomAccountArgParser import atomAccountArgParser
from code_src.staking.cosmos.arg_parser.atomDelegatorArgParser import atomDelegatorArgParser

from code_src.staking.polkadotAndKusama.dot.arg_parser.accountArgParser import accountArgParser
from code_src.staking.polkadotAndKusama.dot.arg_parser.beforeIStartArgParser import beforeIStartArgParser
from code_src.staking.polkadotAndKusama.dot.arg_parser.dotNominatorArgParser import dotNominatorArgParser
from code_src.staking.polkadotAndKusama.dot.arg_parser.dotBonderArgParser import dotBonderArgParser
from code_src.staking.polkadotAndKusama.dot.arg_parser.dotStakerArgParser import dotStakeDotArgParser
from code_src.staking.polkadotAndKusama.ksm.arg_parser.ksmStakerArgParser import ksmStakeDotArgParser
from Logger import myLogger
from code_src.staking.polkadotAndKusama.dot.arg_parser.validatorArgParser import validatorDotArgParser
from code_src.staking.polkadotAndKusama.ksm.arg_parser.ksmBonderArgParser import ksmBonderArgParser
from code_src.staking.polkadotAndKusama.ksm.arg_parser.ksmNominatorArgParser import ksmNominatorArgParser

__name = "StakingManager"
logger = myLogger(__name)
logger.info("BlockchainExecution Staking Program Starting.")

"""
a parser can have 
1 - positional arguments
2 - required arguments 
3 - optional arguments

We arrange functionally into categories using a tree of parsers
- coin
   └─── functionX
    ...
        └─── subFunctionY 
        ...

Example:
topParentParser
└───coinSuppParser
    ├───dotParentParser
    │   └───anotherSuppParser
    │       └───anotherParentParser
    │           └───anotherSuppParser
    ├───solParentParser
    │   ...
    │   └───
    └───xtzParentParser
    │   ...
    │   └───
    ...      
"""

# parent parser (top level arguments parser)
parentParser = argparse.ArgumentParser(prog='stakingmanager.py')

# parent subparser (top level arguments subparser)
# declaring more then one subparser/parser will raise (error: cannot have multiple subparser arguments)
stakeCoinSubParsers = parentParser.add_subparsers(help='Available staking coins.')

# staking coin parsers group
# parent parser for any added coin will be declared here
# naming will be as follow (xCoinParentParser)
dotParentParser = stakeCoinSubParsers.add_parser(name='dot', help='Polkadot staking interface')
# ksm
ksmParentParser = stakeCoinSubParsers.add_parser(name='ksm', help='Kusama staking interface')
# atom
atomParentParser = stakeCoinSubParsers.add_parser(name='atom', help='Cosmos staking interface')

# dot
dotSubParser = dotParentParser.add_subparsers(dest="dot", help='Available dot staking commands')
dotAccount = accountArgParser(dotSubParser, "DOT")
dotStaker = dotStakeDotArgParser(dotSubParser)
dotNominator = dotNominatorArgParser(dotSubParser)
dotBonder = dotBonderArgParser(dotSubParser)
dotValidator = validatorDotArgParser(dotSubParser)
guide = beforeIStartArgParser(dotSubParser)

# ksm
ksmSubParser = ksmParentParser.add_subparsers(dest="ksm", help='Available ksm staking commands')
ksmAccount = accountArgParser(dotSubParser, "KSM")
ksmStaker = ksmStakeDotArgParser(ksmSubParser)
ksmNominator = ksmNominatorArgParser(ksmSubParser)
ksmBonder = ksmBonderArgParser(ksmSubParser)
ksmValidator = validatorDotArgParser(ksmSubParser)

# atom
atomSubParser = atomParentParser.add_subparsers(dest="atom", help='Available atom staking commands')
atomAccount = atomAccountArgParser(atomSubParser)
atomatomDelegator = atomDelegatorArgParser(atomSubParser)


if __name__ == "__main__":
    args = parentParser.parse_args()
    var_args = vars(args)

    if var_args:
        # dot work flow
        if 'dot' in var_args:
            dot = var_args['dot']
            if dot:
                if dot == "stake":
                    args.func(args)

                # nominator
                elif dot == "nominator":

                    try:
                        args.func(args)
                    except AttributeError:
                        dotNominator.print_help()
                # bounder
                elif dot == "bonder":

                    try:
                        args.func(args)
                    except AttributeError:
                        dotBonder.print_help()

                # accounting
                elif dot == "account":
                    try:
                        # print(args)
                        args.func(args)
                    except AttributeError:
                        dotAccount.print_help()
                # TODO
                elif dot == "validator":
                    pass
                elif dot == "guide":
                    try:
                        # print(args)
                        args.func(args)
                    except AttributeError:
                        guide.print_help()

            else:
                dotParentParser.print_help()
        elif 'ksm' in var_args:
            ksm = var_args['ksm']
            if ksm:
                if ksm == "stake":
                    args.func(args)

                # nominator
                elif ksm == "nominator":

                    try:
                        args.func(args)
                    except AttributeError:
                        ksmNominator.print_help()
                # bounder
                elif ksm == "bonder":

                    try:
                        args.func(args)
                    except AttributeError:
                        ksmBonder.print_help()

                # accounting
                elif ksm == "account":
                    try:
                        # print(args)
                        args.func(args)
                    except AttributeError:
                        ksmAccount.print_help()
                # TODO
                elif ksm == "validator":
                    pass
                elif ksm == "guide":
                    try:
                        # print(args)
                        args.func(args)
                    except AttributeError:
                        guide.print_help()

            else:
                ksmParentParser.print_help()
               
        elif 'atom' in var_args:
            atom = var_args['atom']
            if atom:
                if atom == "stake":
                    args.func(args)

                # nominator

                # bounder
                elif atom == "delegator":

                    try:
                        args.func(args)
                    except AttributeError:
                        atomatomDelegator.print_help()

                # accounting
                elif atom == "account":
                    try:
                        # print(args)
                        args.func(args)
                    except AttributeError:
                        atomAccount.print_help()
                # TODO
                elif atom == "validator":
                    pass
                elif atom == "guide":
                    try:
                        # print(args)
                        args.func(args)
                    except AttributeError:
                        guide.print_help()

            else:
                atomParentParser.print_help()

    else:
        parentParser.print_help()
