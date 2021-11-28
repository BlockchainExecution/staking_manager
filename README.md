# StakingManager
Python based CLI tool for staking (nominating) in Polkadot

Instructions:
* run python StakingManager.py dot -h
    - NOTE: because only polkadot is supported, you must give `dot` as the first argument.
    In the future, when we support additional networks, there will be other options to `dot`


Features:
* Pretty intuitive ArgParser for (see examples.py):
	- Creating a mnemonic, keypair, getting acct info
	- ... (will write later)

Architecture:
* StakingManager.py is the main file
* Most "unique" logic is in dotCmdDecorator
* config.py specifies the network (see bottom of file), right now only Polkadot mainnet and Westend are really functional
* Under the hood:
    - SubstrateInterface (py): https://github.com/polkascan/py-substrate-interface
    - https://github.com/paritytech/ss58-registry/blob/main/ss58-registry.json


Immediate TODOs:
* Improved testing
* Improved validations and error handling, e.g. to avoid existential deposit
* Adding new substrate based chains to stake on
* rename code_src/ to src/

