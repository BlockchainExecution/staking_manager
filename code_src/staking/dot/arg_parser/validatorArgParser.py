from code_src.staking.dot.dotArgparserUtil import actionHelp, subcommand
from code_src.staking.dot.dotCmdDecorator import DotValidatorCall
from code_src.staking.dot.fxn_decorator_implementations.substrateCallImplementation import DotSubstrateCall

from examples import exampleStaker


# TODO https://support.polkadot.network/support/solutions/articles/65000150130-how-do-i-know-which-validators-to-choose-
def validatorDotArgParser(parent_parser):
    # bounder parent parser
    @subcommand(parent=parent_parser,
                subHelp="Get a list of validator that meat polkadot requirements.",
                epilog=exampleStaker, reqArgs=[],
                optArgs=[actionHelp()])
    def validator(args):
        @DotSubstrateCall()
        def check():
            pass
