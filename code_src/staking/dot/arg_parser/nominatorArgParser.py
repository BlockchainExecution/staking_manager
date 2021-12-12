from code_src.staking.dot.fxn_decorator_implementations.substrateCallImplementation import DotSubstrateCall
from common import MyHelpFormatter
from code_src.staking.dot.dotArgparserUtil import actionMnemonic, actionValidatorAddress, actionHelp, subcommand, \
    actionTest, actionNumberOfTokens
from examples import exampleNominator, exampleNominate, exampleUnominateTmp, exampleUnominateAll


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

    @subcommand(parent=nominatorSubParser, subHelp=exampleNominate, reqArgs=[actionMnemonic()],
                optArgs=[actionValidatorAddress(), actionHelp()])
    def nominate(args):
        @DotSubstrateCall(cli_name="Nominator", call_module="Staking", call_params={'targets': args.validator_address},
                          seed=args.mnemonic)
        def nominate():
            pass

    # chill
    # https://githubhelp.com/polkascan/py-scale-codec
    # Stakers can be in any one of the three states: validating, nominating, or chilling. When a staker wants to
    # temporarily pause their active engagement in staking but does not want to unbond their funds, they can choose
    # to "chill" their involvement and keep their funds staked.
    # so in fact to totally unstacked all the coin you need to chill and then unbound
    # https://wiki.polkadot.network/docs/maintain-guides-how-to-chill
    """
    Declare no desire to either validate or nominate.
    Effects will be felt at the beginning of the next era.
    The dispatch origin for this call must be _Signed_ by the controller, not the stash.
    # <weight>
    - Independent of the arguments. Insignificant complexity.
    - Contains one read.
    - Writes are limited to the `origin` account key.
    # </weight>"
    """

    @subcommand(parent=nominatorSubParser, subHelp=exampleUnominateTmp, reqArgs=[actionMnemonic()],
                optArgs=[actionTest()])
    def stop_nominate_tmp(args):
        @DotSubstrateCall(cli_name="Nominator", call_module="Staking", call_params={}, seed=args.mnemonic)
        def chill():
            pass

    # chill + unbond
    """
    Declare a `controller` to stop participating as either a validator or nominator.
    Effects will be felt at the beginning of the next era.
    The dispatch origin for this call must be _Signed_, but can be called by anyone.
    If the caller is the same as the controller being targeted, then no further checks are enforced, and this function 
    behaves just like `chill`.
    If the caller is different than the controller being targeted, the following conditions must be met:
    * A `ChillThreshold` must be set and checked which defines how close to the max
    nominators or validators we must reach before users can start chilling one-another.
     * A `MaxNominatorCount` and `MaxValidatorCount` must be set which is used to determine
       how close we are to the threshold.
     * A `MinNominatorBond` and `MinValidatorBond` must be set and checked, which determines  if this is a person that 
       should be chilled because they have not met the threshold bond required.
    This can be helpful if bond requirements are updated, and we need to remove old users who do not satisfy these 
    requirements.
    """

    @subcommand(parent=nominatorSubParser, subHelp=exampleUnominateAll,
                reqArgs=[actionMnemonic(), actionNumberOfTokens()],
                optArgs=[actionTest()])
    def stop_nominate_all(args):
        @DotSubstrateCall(cli_name="Nominator", call_module="Staking", call_params={'value': args.number_of_tokens},
                          seed=args.mnemonic)
        def stop_nominate_all():
            pass

    return nominatorParser
