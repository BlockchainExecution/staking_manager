import argparse
from code_src.staking.dot.arg_parser.accountArgParser import accountArgParser
from code_src.staking.dot.arg_parser.beforeIStartArgParser import beforeIStartArgParser
from code_src.staking.dot.arg_parser.nominatorArgParser import nominatorArgParser
from code_src.staking.dot.arg_parser.bonderArgParser import bonderArgParser
from code_src.staking.dot.arg_parser.stakerArgParser import stakeDotArgParser
from Logger import myLogger
from code_src.staking.dot.arg_parser.validatorArgParser import validatorDotArgParser

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
# xtzParentParser = stakeCoinSubParsers.add_parser(name='xtz', help='Tezos staking interface')

#
# dot
dotSubParser = dotParentParser.add_subparsers(dest="dot", help='Available dot staking commands')
account = accountArgParser(dotSubParser)
staker = stakeDotArgParser(dotSubParser)
nominator = nominatorArgParser(dotSubParser)
bounder = bonderArgParser(dotSubParser)
validator = validatorDotArgParser(dotSubParser)
guide = beforeIStartArgParser(dotSubParser)
# xtz
# xtzSubParser = xtzParentParser.add_subparsers(dest="xtz", help='Available xtz staking commands')


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
                        nominator.print_help()
                # bounder
                elif dot == "bonder":

                    try:
                        args.func(args)
                    except AttributeError:
                        bounder.print_help()

                # accounting
                elif dot == "account":
                    try:
                        # print(args)
                        args.func(args)
                    except AttributeError:
                        account.print_help()
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
    else:
        parentParser.print_help()
