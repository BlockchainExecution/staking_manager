from code_src.staking.dot.bounder.boundModule import Bounder
from code_src.staking.dot.dotArgparserUtil import actionSeed, actionNumberOfTokens, actionControllerAddress, \
    actionRewardsDestination, \
    actionValidatorAddress, actionHelp, subcommand
from code_src.staking.dot.nominator.nominatorModule import Nominator
from common import active_substrate
from examples import exampleStaker


def stakeDotArgParser(parent_parser):
    # bounder parent parser
    @subcommand(parent=parent_parser,
                subHelp="automatically prepare coins and send them to be staked (bond coin then nominate a validator).",
                epilog=exampleStaker, reqArgs=[actionSeed(), actionControllerAddress(), actionNumberOfTokens()],
                optArgs=[actionRewardsDestination(), actionValidatorAddress(), actionHelp()])
    def staker(args):
        bounderInstance = Bounder()
        # args from cli
        nominateInstance = Nominator()
        seed = args.seed
        controllerAddress = args.controller_address
        number_of_tokens = args.number_of_tokens
        rewards_destination = args.rewards_destination
        validator_address = args.validator_address

        bondFunc = bounderInstance.bond(active_substrate=active_substrate, value=number_of_tokens,
                                        controller_addr=controllerAddress,
                                        reward_address=rewards_destination)

        bounderInstance.run(active_substrate=active_substrate, seed=seed, call=bondFunc)

        nominateFunc = nominateInstance.nominate(active_substrate=active_substrate,
                                                 targets=validator_address)
        nominateInstance.run(active_substrate=active_substrate, seed=seed, call=nominateFunc)
