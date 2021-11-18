from code_src.staking.dot.nominator.nominatorModule import Nominator
from common import MyHelpFormatter, active_substrate
from code_src.staking.dot.dotArgparserUtil import actionSeed, actionValidatorAddress, actionHelp, subcommand, actionTest
from Logger import myLogger
from examples import exampleNominator, exampleNominate, exampleUnominate


def nominatorArgParser(parser_parent):
    # nominator
    nominateInstance = Nominator()
    # nominator parent parser
    nominatorParser = parser_parent.add_parser(name="nominator", help="""nomination interface to DOT.""",
                                               add_help=False, epilog=exampleNominator,
                                               formatter_class=MyHelpFormatter)
    nominatorSubParser = nominatorParser.add_subparsers(help='')

    # nominate
    @subcommand(parent=nominatorSubParser, subHelp=exampleNominate, reqArgs=[actionSeed()],
                optArgs=[actionValidatorAddress(), actionHelp()])
    def nominate(args):
        seed = args.seed
        validator_address = args.validator_address

        nominateFunc = nominateInstance.nominate(active_substrate=active_substrate,
                                                 targets=validator_address)
        nominateInstance.run(active_substrate=active_substrate, seed=seed, call=nominateFunc)

    @subcommand(parent=nominatorSubParser, subHelp=exampleUnominate, reqArgs=[actionSeed()], optArgs=[actionTest()])
    def unnominate(args):
        myLogger('unnominate').info(args.unominate)

    return nominatorParser
