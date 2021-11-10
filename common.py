import json

from substrateinterface import SubstrateInterface

database_name = "dotdb"

# dot
# required properties ---------------------------------------
substrate_polkadot = SubstrateInterface(
    url="wss://rpc.polkadot.io",
    ss58_format=0,
    type_registry_preset='polkadot'
)
# Kusama

substrate_kusama = SubstrateInterface(
    url="wss://kusama-rpc.polkadot.io/",
    ss58_format=2,
    type_registry_preset='kusama'
)
# Rococo

substrate_rococo = SubstrateInterface(
    url="wss://rococo-rpc.polkadot.io",
    ss58_format=42,
    type_registry_preset='rococo'
)
# Westend

substrate_westend = SubstrateInterface(
    url="wss://westend-rpc.polkadot.io",
    ss58_format=42,
    type_registry_preset='westend'
)

# ---------------------------------------

active_substrate = substrate_westend

for el in substrate_polkadot.get_metadata_call_functions():
    try:
        if "Staking" in el['module_prefix'] and "set" in el['call_name']:
            print(el)
            print("*" * 20)
    except:
        continue
