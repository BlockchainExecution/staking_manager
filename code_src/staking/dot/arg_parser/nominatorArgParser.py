from code_src.staking.dot.dotCmdDecorator import DotSubstrateCall

from common import MyHelpFormatter
from code_src.staking.dot.dotArgparserUtil import actionSeed, actionValidatorAddress, actionHelp, subcommand, actionTest
from Logger import myLogger
from examples import exampleNominator, exampleNominate, exampleUnominate


def nominatorArgParser(parser_parent):
    # nominator parent parser
    nominatorParser = parser_parent.add_parser(name="nominator", help="""nomination interface to DOT.""",
                                               add_help=False, epilog=exampleNominator,
                                               formatter_class=MyHelpFormatter)
    nominatorSubParser = nominatorParser.add_subparsers(help='')

    # nominate
    """
    {'call_name': 'nominate',
    'call_args': [{'name': 'targets', 'type': 155, 'typeName': 'Vec<<T::Lookup as StaticLookup>::Source>', 'docs': []}],
    'documentation': "Declare the desire to nominate `targets` for the origin controller.
    Effects will be felt at the beginning of the next era.
    The dispatch origin for this call must be _Signed_ by the controller, not the stash.
    # <weight>
    - The transaction's complexity is proportional to the size of `targets` (N)
    which is capped at CompactAssignments::LIMIT (MAX_NOMINATIONS).
    - Both the reads and writes follow a similar pattern.
    # </weight>",
    'module_prefix': 'Staking', 'module_name': 'Staking', 'spec_version': 9122}
    :return:
    """
    @subcommand(parent=nominatorSubParser, subHelp=exampleNominate, reqArgs=[actionSeed()],
                optArgs=[actionValidatorAddress(), actionHelp()])
    def nominate(args):
        seed = args.seed
        validator_address = args.validator_address

        @DotSubstrateCall(cli_name="Nominator", call_module="Staking", call_params={'targets': validator_address},
                          seed=seed)
        def nominate():
            pass

    @subcommand(parent=nominatorSubParser, subHelp=exampleUnominate, reqArgs=[actionSeed()], optArgs=[actionTest()])
    def unnominate(args):
        myLogger('unnominate').info(args.seed)
        seed = args.seed

        @DotSubstrateCall(cli_name="unnnominate", call_module="Staking", call_params={}, seed=seed)
        def unnnominate():
            pass

    return nominatorParser
