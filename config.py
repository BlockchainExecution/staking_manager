from substrateinterface import SubstrateInterface
import json


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

# staking errors mapper
dotModulesErrors = json.loads("""{
  "6": {
    "0": "NotController Not a controller account.",
    "1": "NotStash Not a stash account.",
    "2": "AlreadyBonded Stash is already bonded.If you want to bond more coins you can use <bondextra> command line utilities",
    "3": "AlreadyPaired Controller is already paired.",
    "4": "EmptyTargets Targets cannot be empty.",
    "5": "DuplicateIndex Duplicate index.",
    "6": "InvalidSlashIndex Slash record index out of bounds.",
    "7": "InsufficientValue Can not bond with value less than minimum balance.",
    "8": "NoMoreChunks Can not schedule more unlock chunks.",
    "9": "NoUnlockChunk Can not rebond without unlocking chunks.",
    "10": "FundedTarget Attempting to target a stash that still has funds.",
    "1&": "InvalidEraToReward Invalid era to reward.",
    "12": "InvalidNumberOfNominations Invalid number of nominations.",
    "13": "NotSortedAndUnique Items are not sorted and unique.",
    "14": "AlreadyClaimed Rewards for this era have already been claimed for this validator.",
    "15": "OffchainElectionEarlySubmission The submitted result is received out of the open window.",
    "16": "OffchainElectionWeakSubmission The submitted result is not as good as the one stored on chain.",
    "17": "SnapshotUnavailable The snapshot data of the current window is missing.",
    "18": "OffchainElectionBogusWinnerCount Incorrect number of winners were presented.",
    "19": "OffchainElectionBogusWinner One of the submitted winners is not an active candidate on chain (index is out of range in snapshot).",
    "20": "OffchainElectionBogusCompact Error while building the assignment type from the compact. This can happen if an index is invalid, or if the weights overflow.",
    "21": "OffchainElectionBogusNominator One of the submitted nominators is not an active nominator on chain.",
    "22": "OffchainElectionBogusNomination One of the submitted nominators has an edge to which they have not voted on chain.",
    "23": "OffchainElectionSlashedNomination One of the submitted nominators has an edge which is submitted before the last non-zero slash of the target.",
    "24": "OffchainElectionBogusSelfVote A self vote must only be originated from a validator to ONLY themselves.",
    "25": "OffchainElectionBogusEdge The submitted result has unknown edges that are not among the presented winners.",
    "26": "OffchainElectionBogusScore The claimed score does not match with the one computed from the data.",
    "27": "OffchainElectionBogusElectionSize The election size is invalid.",
    "28": "CallNotAllowed The call is not allowed at the given time due to restrictions of election period.",
    "29": "IncorrectHistoryDepth Incorrect previous history depth input provided.",
    "30": "IncorrectSlashingSpans Incorrect number of slashing spans provided."
  },
 "System": {
  "0" : ""
 }
}""")


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
    existentialDeposit = 0


activeConfig = TestingConfig
