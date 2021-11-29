# StakingManager
Python based CLI tool for staking (nominating) in Polkadot
<br />⚠️ Not production ready ⚠️

## Instructions:
run `python StakingManager.py dot -h`
    <br />- NOTE: because only polkadot is supported, you must give `dot` as the first argument.
    In the future, when we support additional networks, there will be other options to `dot`

### Features:
* Pretty intuitive ArgParser (see examples.py) for:
	- Creating a mnemonic, keypair, getting acct info
	- Bonding, unbonding, rebonding, withdrawing
	- Nominating (Staking), setting staker requirements
* Validations and error handling for staking:
	- Keep-alive checks (existential deposit)
	- https://wiki.polkadot.network/docs/maintain-errors

### Codebase Notes:
* StakingManager.py is the cli executed file
* Most "unique" logic is in fxn_decorator_implementations folder
* config.py specifies the network (see bottom of config file), right now only Polkadot mainnet and Westend are really functional
* Under the hood:
    - SubstrateInterface (py): https://github.com/polkascan/py-substrate-interface
    - https://github.com/paritytech/ss58-registry/blob/main/ss58-registry.json

### Architecture:
* TODO

### Coding Patterns:
* If a filename has a corresponding Utils file, one should not ever need to import the Utils file except in its pair.
    - For example, accountManager.py should import accountManagerUtils.py, but no other files should import accountManagerUtils.py.
Instead, all other files should only ever have to import accountManager.py.


#### Immediate TODOs:
* Improved testing
* Improved validations and error handling, e.g. to avoid existential deposit
* Adding new substrate based chains to stake on
* rename code_src/ to src/

