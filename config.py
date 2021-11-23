from substrateinterface import SubstrateInterface


# websockets ---------------------------------------
# substrate are a modular framework for building blockchains.
# Polkadot is built using Substrate. Chains built with Substrate will be easy to connect as parachains.
# dot
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


# configs
# TODO `value` must be more than the `minimum_balance` specified by`T::Currency`. how to use substrate to fetch this information
class ProductionConfig:
    activeSubstrate = substratePolkadot()
    activeValidator = binanceValidator
    coinDecimalPlaces = 10 ** 10
    coinName = "DOT"
    stakeMinimumAmount = 120
    existentialDeposit = 1


class TestingConfig:
    activeSubstrate = substrateWestend()
    activeValidator = westendValidator
    coinDecimalPlaces = 10 ** 12
    coinName = "WND"
    stakeMinimumAmount = 1


activeConfig = TestingConfig
