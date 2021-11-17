import argparse
from code_src.staking.dot.accounting.accountingArgParser import accountingArgParser
from code_src.staking.dot.nominator.nominatorArgParser import nominatorArgParser
from code_src.staking.dot.bounder.bounderArgParser import bounderArgParser
from code_src.staking.dot.stake.stakerArgParser import stakeDotArgParser
from code_src.staking.dot.nominator.nominatorModule import Nominator
from code_src.staking.dot.bounder.boundModule import Bounder
from code_src.staking.dot.accounting.accountingModule import Accounting
from Logger import myLogger
from common import active_substrate

# TODO re-create this code with less complexity

__name = "StakingManager"
logger = myLogger(__name)

logger.info("Start XStake Program.")

# Parent parser
parentParser = argparse.ArgumentParser(prog='stakingmanager.py')

# staking coin groups
stakeCoinSubParsers = parentParser.add_subparsers(help='Available staking coins')

dotParentParser = stakeCoinSubParsers.add_parser(name='dot', help='Polkadot staking interface')
# xtzParentParser = stakeCoinSubParsers.add_parser(name='xtz', help='Tezos staking interface')

# dot
dotSubParser = dotParentParser.add_subparsers(dest="dot", help='Available dot staking commands')
accounting = accountingArgParser(dotSubParser)
staker = stakeDotArgParser(dotSubParser)
nominator = nominatorArgParser(dotSubParser)
bounder = bounderArgParser(dotSubParser)
# xtz
# xtzSubParser = xtzParentParser.add_subparsers(dest="xtz", help='Available xtz staking commands')

if __name__ == "__main__":
    args = parentParser.parse_args()
    # print(args)
    var_args = vars(args)
    if var_args:
        # dot work flow
        if 'dot' in var_args:
            dot = var_args['dot']
            if dot:

                # stake
                if dot == "staker":
                    bounderInstance = Bounder()
                    nominateInstance = Nominator()
                    seed = var_args['seed']
                    controllerAddress = var_args['controller_address']
                    number_of_tokens = var_args['number_of_tokens']
                    rewards_destination = var_args['rewards_destination']
                    validator_address = var_args['validator_address']

                    bondFunc = bounderInstance.bond(active_substrate=active_substrate, value=number_of_tokens,
                                                    controller_addr=controllerAddress,
                                                    reward_address=rewards_destination)

                    bounderInstance.run(active_substrate=active_substrate, seed=seed, call=bondFunc)

                    nominateFunc = nominateInstance.nominate(active_substrate=active_substrate,
                                                             targets=validator_address)
                    nominateInstance.run(active_substrate=active_substrate, seed=seed, call=nominateFunc)

                # nominator
                elif dot == "nominator":
                    bounderInstance = Bounder()
                    nominateInstance = Nominator()
                    try:
                        if var_args['func'] == 'nominate':
                            seed = var_args['seed']
                            validator_address = var_args['validator_address']

                            nominateFunc = nominateInstance.nominate(active_substrate=active_substrate,
                                                                     targets=validator_address)
                            nominateInstance.run(active_substrate=active_substrate, seed=seed, call=nominateFunc)
                        elif var_args['func'] == 'unnominate':
                            bounderInstance = Bounder()
                            nominateInstance = Nominator()
                            pass
                        else:
                            nominator.print_help()
                    except KeyError:
                        nominator.print_help()

                # bounder
                elif dot == "bounder":

                    try:
                        if var_args['func'] == 'bond':
                            bounderInstance = Bounder()
                            nominateInstance = Nominator()
                            seed = var_args['seed']
                            controllerAddress = var_args['controller_address']
                            number_of_tokens = var_args['number_of_tokens']
                            rewards_destination = var_args['rewards_destination']
                            validator_address = var_args['validator_address']
                            # active_substrate, controller_addr, value, reward_address=""
                            bondFunc = bounderInstance.bond(active_substrate=active_substrate,
                                                            controller_addr=controllerAddress, value=number_of_tokens,
                                                            reward_address=rewards_destination)
                            print("bond coins")
                            bounderInstance.run(active_substrate=active_substrate, seed=seed, call=bondFunc)
                        elif var_args['func'] == "rebound":
                            bounderInstance = Bounder()
                            nominateInstance = Nominator()
                            seed = var_args['seed']
                            number_of_tokens = var_args['number_of_tokens']

                            reBoundFunc = bounderInstance.reBound(active_substrate=active_substrate,
                                                                  value=number_of_tokens)
                            bounderInstance.run(active_substrate=active_substrate, seed=seed, call=reBoundFunc)

                        elif var_args['func'] == "unbound":
                            bounderInstance = Bounder()
                            nominateInstance = Nominator()
                            seed = var_args['seed']
                            number_of_tokens = var_args['number_of_tokens']

                            unBoundFunc = bounderInstance.unBound(active_substrate=active_substrate,
                                                                  value=number_of_tokens)
                            bounderInstance.run(active_substrate=active_substrate, seed=seed, call=unBoundFunc)
                        else:
                            bounder.print_help()
                    except KeyError:
                        bounder.print_help()
                # TODO fix stakingmanager.py: error: unrecognized arguments: -h for accounting
                elif dot == "accounting":
                    try:
                        if var_args['func'] == 'mnemonic':
                            account = Accounting()
                            account.createMnemonic()
                        elif var_args['func'] == 'keypair':
                            account = Accounting()
                            mnemonic = var_args['mnemonic']
                            account.createKeypair(mnemonic)
                        elif var_args['func'] == 'create':
                            account = Accounting()
                            account.create_account()
                        elif var_args['func'] == 'info':
                            account = Accounting()
                            ss58_address = var_args['address']
                            account.accountInfos(active_substrate=active_substrate, ss58_address=ss58_address)
                        else:
                            accounting.print_help()
                    except KeyError:
                        accounting.print_help()

            else:
                dotParentParser.print_help()
        """        elif "xtz" in var_args:
            xtz = var_args['xtz']
            if xtz:
                pass
            else:
                xtzParentParser.print_help()"""
    else:
        parentParser.print_help()
