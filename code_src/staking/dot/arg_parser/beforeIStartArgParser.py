# beforeIStartArgParser
from code_src.staking.dot.dotArgparserUtil import actionHelp, subcommand
from examples import exampleGuide
from Logger import myLogger


def beforeIStartArgParser(parent_parser):
    # bounder parent parser
    @subcommand(parent=parent_parser,
                subHelp="Get most helpfull tips abount polkadot protocol and staking.",
                epilog=exampleGuide,
                optArgs=[actionHelp()])
    def guide(args):
        userGuide = """Polkadot staking notes
        
    - Nominating currently requires a minimum of 120 DOT staked funds on Polkadot.
    - On the Polkadot network, an address is only active when it holds a minimum amount, currently set at 1 DOT.
        - If an account drops below the ED, the account is reaped (“deactivated”) and any remaining funds are destroyed. 
    - If an account is already bonded the use of bond command will be not needed else use (bondextra)           
        """
        myLogger("Guide").info(userGuide)
