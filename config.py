from substrateinterface import SubstrateInterface
import os
from utils import get_project_root_dir

# execution environment (for testing) --------------
main_script = os.path.join(get_project_root_dir(), "StakingManager.py")
# to get your python env, execute "which python" in CLI with env activated
# E.g. for anaconda read https://docs.anaconda.com/anaconda/user-guide/tasks/integration/python-path/

"""
 Lucas:
 I put my env below, just comment it out and run yours. We'll put
 everything in a docker container later to resolve this issue
"""
venv_env = "/Users/lucas/opt/anaconda3/envs/crypto_hedge_fund/bin/python"
# venv_env = os.path.join(get_project_root_dir(), "venv\\Scripts\\python.exe")


# websockets ---------------------------------------
# substrate are a modular framework for building blockchains.
# Polkadot is built using Substrate. Chains built with Substrate will be easy to connect as parachains.
# dot
# https://github.com/paritytech/ss58-registry/blob/main/ss58-registry.json
def substratePolkadot():
    substrate_polkadot = SubstrateInterface(
        url="wss://rpc.polkadot.io",
        ss58_format=0,
        type_registry_preset='polkadot'
    )
    return substrate_polkadot


# Kusama
def substrateKusama():
    substrate_kusama = SubstrateInterface(
        url="wss://kusama-rpc.polkadot.io/",
        ss58_format=2,
        type_registry_preset='kusama'
    )
    return substrate_kusama


# Rococo
def substrateRococo():
    substrate_rococo = SubstrateInterface(
        url="wss://rococo-rpc.polkadot.io",
        ss58_format=42,
        type_registry_preset='rococo'
    )
    return substrate_rococo


# Westend
def substrateWestend():
    substrate_westend = SubstrateInterface(
        url="wss://westend-rpc.polkadot.io",
        ss58_format=42,
        type_registry_preset='westend'
    )
    return substrate_westend


# ---------------------------------------
# validator
westendValidator = ["5C556QTtg1bJ43GDSgeowa3Ark6aeSHGTac1b2rKSXtgmSmW"]
binanceValidator = ["114SUbKCXjmb9czpWTtS3JANSmNRwVa4mmsMrWYpRG1kDH5"]

# There is also a maximum of 22,500 nominators in place at the moment. That means,
# if there are already 22,500 nominators, you will not be able to nominate,
# even if you have more than the minimum of 120 DOT staked.
# You can double-check the current number of nominators
# on https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Frpc.pinknode.io%2Fpolkadot%2Fexplorer#/staking
# TODO a function that check number of active nominator if the value > 22500 return False (no place to nominate) else True
# configs
# TODO `value` must be more than the `minimum_balance` specified by`T::Currency`. how to use substrate to fetch this information
class ProductionConfig:
    activeSubstrate = substratePolkadot()
    activeValidator = binanceValidator
    ss58_format = 0
    coinDecimalPlaces = 10 ** 10
    coinDecimalPlacesLength = 10
    coinName = "DOT"
    # Nominating currently requires a minimum of 120 DOT staked funds on Polkadot
    stakeMinimumAmount = 120
    # On the Polkadot network, an address is only active when it holds a minimum amount, currently set at 1 DOT
    existentialDeposit = 1


class TestingConfig:
    activeSubstrate = substrateWestend()
    activeValidator = westendValidator
    ss58_format = 42
    coinDecimalPlaces = 10 ** 12
    coinDecimalPlacesLength = 12
    coinName = "WND"
    stakeMinimumAmount = 1
    existentialDeposit = 1


activeConfig = TestingConfig
