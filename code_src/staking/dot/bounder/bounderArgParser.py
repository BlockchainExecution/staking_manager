import argcomplete

from code_src.staking.dot.bounder.boundModule import Bounder
from common import MyHelpFormatter, active_substrate
from code_src.staking.dot.dotArgparserUtil import actionSeed, actionNumberOfTokens, actionControllerAddress, \
    actionRewardsDestination, \
    actionValidatorAddress, actionHelp, subcommand
from examples import exampleBond, exampleBounder, exampleBoundExtra, exampleReBound, exampleWithdrawUnBonded


def bounderArgParser(parent_parser):
    # bounder
    bounderInstance = Bounder()
    # bounder parent parser
    bounderParser = parent_parser.add_parser("bounder", help="bond interface to DOT.", epilog=exampleBounder,
                                             formatter_class=MyHelpFormatter)
    bounderSubParser = bounderParser.add_subparsers(help='')

    # bond
    @subcommand(parent=bounderSubParser,
                subHelp="Take the origin account as a stash and lock up `value` of its balance. `controller` will be the account that controls it.",
                epilog=exampleBond, reqArgs=[actionControllerAddress(), actionNumberOfTokens()],
                optArgs=[actionRewardsDestination(), actionValidatorAddress(), actionHelp()])
    def bond(args):
        seed = args['seed']
        controllerAddress = args.controller_address
        number_of_tokens = args.number_of_tokens
        rewards_destination = args.rewards_destination

        # active_substrate, controller_addr, value, reward_address=""
        bondFunc = bounderInstance.bond(active_substrate=active_substrate,
                                        controller_addr=controllerAddress, value=number_of_tokens,
                                        reward_address=rewards_destination)
        bounderInstance.run(active_substrate=active_substrate, seed=seed, call=bondFunc)

    # unbound
    @subcommand(parent=bounderSubParser,
                subHelp="Schedule a portion of the stash to be unlocked ready for transfer out after the bond period ends.",
                epilog=exampleBond, reqArgs=[actionControllerAddress(), actionNumberOfTokens()],
                optArgs=[actionRewardsDestination(), actionValidatorAddress(), actionHelp()])
    def unbound(args):
        seed = args['seed']
        number_of_tokens = args.number_of_tokens

        unBoundFunc = bounderInstance.unBound(active_substrate=active_substrate,
                                              value=number_of_tokens)
        bounderInstance.run(active_substrate=active_substrate, seed=seed, call=unBoundFunc)

    # rebond
    @subcommand(parent=bounderSubParser,
                subHelp="Rebond a portion of the stash scheduled to be unlocked.",
                epilog=exampleReBound, reqArgs=[actionControllerAddress(), actionNumberOfTokens()],
                optArgs=[actionRewardsDestination(), actionValidatorAddress(), actionHelp()])
    def rebond(args):
        seed = args['seed']
        number_of_tokens = args.number_of_tokens

        reBoundFunc = bounderInstance.reBound(active_substrate=active_substrate,
                                              value=number_of_tokens)
        bounderInstance.run(active_substrate=active_substrate, seed=seed, call=reBoundFunc)

    # bond extra
    @subcommand(parent=bounderSubParser,
                subHelp="Add some extra amount that have appeared in the stash `free_balance` into the balance up for staking.",
                epilog=exampleBoundExtra, reqArgs=[actionControllerAddress(), actionNumberOfTokens()],
                optArgs=[actionRewardsDestination(), actionValidatorAddress(), actionHelp()])
    def bondextra(args):
        seed = args['seed']
        number_of_tokens = args.number_of_tokens

        boundExtraFunc = bounderInstance.bondExtra(active_substrate=active_substrate,
                                                   value=number_of_tokens)
        bounderInstance.run(active_substrate=active_substrate, seed=seed, call=boundExtraFunc)

    # TODO understand better num_slashing_spans
    # withdraw unbounded
    @subcommand(parent=bounderSubParser,
                subHelp="Remove any unlocked chunks from the `unlocking` queue. This essentially frees up that balance to be used by the stash account to do whatever it wants.",
                epilog=exampleWithdrawUnBonded, reqArgs=[actionControllerAddress(), actionNumberOfTokens()],
                optArgs=[actionRewardsDestination(), actionValidatorAddress(), actionHelp()])
    def withdrawunbounded(args):
        pass

    # autocomplite
    # argcomplete.autocomplete(bounderParser)

    return bounderParser
