import os

from substrateinterface import SubstrateInterface


def get_project_root_dir():
    return os.path.dirname(os.path.abspath(__file__))


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
