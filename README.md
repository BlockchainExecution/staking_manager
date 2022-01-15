# StakingManager
Python based CLI tool for staking (nominating) in Polkadot
<br />⚠️ Not production ready ⚠️

## Instructions:
run `python StakingManager.py dot -h`
    <br />- NOTE: because only polkadot is supported, you must give `dot` as the first argument.
    In the future, when we support additional networks, there will be other options to `dot`

### Testing:
run `python test/endToEndTests.py`

### Features:
* Pretty intuitive ArgParser (see examples.py) for:
	- Creating a mnemonic, keypair, getting acct info
	- Bonding, unbonding, rebonding, withdrawing
	- Nominating (Staking), setting staker requirements
* Validations
	- Keep-alive checks (existential deposit)
	- https://wiki.polkadot.network/docs/maintain-errors
* Error handling
	- TODO
* Tests
	- e2e tests (inclusive of CLI commands) in `test/endToEndTests.py`
	- Tests are major WIP, may fail and exit
	- TODO: Setting up and testing on local network (see Testing Tools below)

### Recommended Reading
* DOT: https://wiki.polkadot.network/docs/maintain-guides-how-to-nominate-polkadot
* KSM: https://wiki.polkadot.network/docs/maintain-guides-how-to-nominate-kusama

### Codebase Notes:
* To run the program, execute StakingManager.py
* Most "unique" logic is in fxn_decorator_implementations folder
* config.py specifies the network (see bottom of config file), right now only Polkadot mainnet and Westend are really functional
* Under the hood:
    - SubstrateInterface (py):
    	+ Github: https://github.com/polkascan/py-substrate-interface
    	+ Documentation: https://polkascan.github.io/py-substrate-interface/
    - SS58:
    	+ Github: https://github.com/paritytech/ss58-registry/blob/main/ss58-registry.json
    - TODO: Testing Tools:
    	+ https://github.com/wpank/polkadot-local-network
    	+ https://github.com/w3f/1k-validators-be/blob/master/src/misc/testSetup.ts

### Coding Patterns (Ideals):
* SOLID - https://gist.github.com/dmmeteo/f630fa04c7a79d3c132b9e9e5d037bfd
* If a filename has a corresponding Utils file, one should not ever need to import the Utils file except in its pair.
    - For example, accountManager.py should import accountManagerUtils.py, but no other files should import accountManagerUtils.py.
Instead, all other files should only ever have to import accountManager.py.
* Pass "generic" arguements first in a function and more unique arguements subsequently
    - For example, in `def __init__(self, logger, accountManager)`, `self` and `logic` generic and therefore passed before `accountManager`

### Architecture:
* TODO
* Code for parsing CLI commands is in `/arg_parser` folder
* The program "logic" is in `/fxn_decorator_implementations`
   - accountImplementation contains classes related to accounts
   - substrateCallImplementation contains classes related to bonding and nominating

#### Immediate TODOs:
* Improved testing
* Improved validations and error handling, e.g. to avoid existential deposit
* Adding new substrate based chains to stake on
* check TODOs in substrateCallImplementationUtils
* rename code_src > src
* rename all cases of "bounder" to "bonder"



