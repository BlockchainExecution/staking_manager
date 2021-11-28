# StakingManager
Python based CLI tool for staking (nominating) in Polkadot

Instructions:
run `python StakingManager.py dot -h`
    - NOTE: because only polkadot is supported, you must give `dot` as the first argument.
    In the future, when we support additional networks, there will be other options to `dot`

Features:
* Pretty intuitive ArgParser for (see examples.py):
	- Creating a mnemonic, keypair, getting acct info
	- Bonding, unbonding, rebonding, withdrawing
	- Nominating (Staking), setting staker requirements
* Validations and error handling for staking
	- Keep-alive checks (existential deposit)
	- https://wiki.polkadot.network/docs/maintain-errors

Architecture:
* StakingManager.py is the cli executed file
* Most "unique" logic is in fxn_decorator_implementations folder
* config.py specifies the network (see bottom of config file), right now only Polkadot mainnet and Westend are really functional
* Under the hood:
    - SubstrateInterface (py): https://github.com/polkascan/py-substrate-interface
    - https://github.com/paritytech/ss58-registry/blob/main/ss58-registry.json

Immediate TODOs:
* Improved testing
* Improved validations and error handling, e.g. to avoid existential deposit
* Adding new substrate based chains to stake on
* rename code_src/ to src/

