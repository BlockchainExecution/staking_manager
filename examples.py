# accounting -----------------------------------------------------------------------------------------------------------
# stake dot
exampleAccount = """
Description
  Account interface to Polkadot..

example:
  python %(prog)s create -h
  python %(prog)s info -h
  python %(prog)s mnemonic -h
  python %(prog)s keypair -h
    """
# create mnemonic
exampleCreateMnemonic = """
description : 
  create Mnemonic dot

example:
  python %(prog)s create_mnemonic \n
    """
# create keypair
exampleCreateKeypair = """
description : 
  create Keypair dot

example:
  python %(prog)s keypair -m/--mnemonic "MNEMONIC" \n
    """
# account info
exampleAccountInfos = """
description : 
  accountInfos dot

example:
  python %(prog)s info \n
    """
# create account
exampleCreateAccount = """
description : 
  createAccount dot

example:
  python %(prog)s \n
        """
# nominator ------------------------------------------------------------------------------------------------------------
exampleNominator = """
Note: 
You need to bond you <coin> before you can use nominate option.
check stakingmanager.py <coin> bounder -h for more information

example:
    python %(prog)s -h

    """
# nominate
exampleNominate = """
description : 
  nominate dot coin

example:
  python %(prog)s nominate -s/--seed "MNEMONIC_PHRASE" -va/--validator_address VALIDATOR_ADDRESS \n
  python %(prog)s nominate -s/--seed "MNEMONIC_PHRASE" -va/--validator_address VALIDATOR_ADDRESS_1,VALIDATOR_ADDRESS_2,VALIDATOR_ADDRESS_N \n
    """
# unnominate_tmp
exampleUnominateTmp = """
description : 
  temporarily pause active engagement in staking but does not  unbond funds

example:
  python %(prog)s unnominate_tmp -s/--seed "MNEMONIC_PHRASE" -va/--validator_address VALIDATOR_ADDRESS \n
  python %(prog)s unnominate_tmp -s/--seed "MNEMONIC_PHRASE" -va/--validator_address VALIDATOR_ADDRESS_1,VALIDATOR_ADDRESS_2,VALIDATOR_ADDRESS_N \n
    """
# unnominate_all
exampleUnominateAll = """
description : 
  stop active engagement in staking and unbond funds

example:
  python %(prog)s unnominate_all -s/--seed "MNEMONIC_PHRASE" -va/--validator_address VALIDATOR_ADDRESS \n
  python %(prog)s unnominate_all -s/--seed "MNEMONIC_PHRASE" -va/--validator_address VALIDATOR_ADDRESS_1,VALIDATOR_ADDRESS_2,VALIDATOR_ADDRESS_N \n
    """
# bounder --------------------------------------------------------------------------------------------------------------
exampleBonder = """
description : 
  bonder interface.

example:
  python %(prog)s bond -h
  python %(prog)s unbond -h
  python %(prog)s rebond -h
  python %(prog)s bondextra -h
  python %(prog)s withdrawunbonded -h
  \n
"""
# bond
exampleBond = """
description : 
  bond dot coin before nomination

example:
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -ca/--controller_address CONTROLLER_ADDRESS -nt/--number_of_tokens NUMBER_OF_TOKENS \n
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -ca/--controller_address CONTROLLER_ADDRESS -nt NUMBER_OF_TOKENS -va/--validator_address VALIDATOR_ADDRESS \n
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -ca/--controller_address CONTROLLER_ADDRESS -nt NUMBER_OF_TOKENS -va/--validator_address VALIDATOR_ADDRESS_1,VALIDATOR_ADDRESS_2,VALIDATOR_ADDRESS_N \n

"""
# unbound
exampleUnBound = """
description : 
  unbound dot coin

example:
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -nt NUMBER_OF_TOKENS \n
"""
# rebound
exampleReBound = """
description : 
  rebound dot coin

example:
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -nt NUMBER_OF_TOKENS \n    
    """
# bound extra
exampleBoundExtra = """
description : 
  boundextra dot coin

example:
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -nt NUMBER_OF_TOKENS \n
    """
# withdraw
exampleWithdrawUnBonded = """
description : 
  withdrawunbonded dot coin

example:
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -nt NUMBER_OF_TOKENS \n
    """

# staker ---------------------------------------------------------------------------------------------------------------
exampleStaker = """
Description\n
  This script will bond and nominate DOT to a validator.\n

example:\n
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -ca/--controller_address "CONTROLLER_ADDRESS" -nt/--number_of_tokens NUMBER_OF_TOKENS\n
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -ca/--controller_address "CONTROLLER_ADDRESS" -nt/--number_of_tokens NUMBER_OF_TOKENS -rd/--rewards_destination "REWARD_DESTINATION"\n
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -ca/--controller_address "CONTROLLER_ADDRESS" -nt/--number_of_tokens NUMBER_OF_TOKENS -va/--validator_address "VALIDATOR_ADDRESS"\n
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -ca/--controller_address "CONTROLLER_ADDRESS" -nt/--number_of_tokens NUMBER_OF_TOKENS -va/--validator_address "VALIDATOR_ADDRESS_1","VALIDATOR_ADDRESS_2","VALIDATOR_ADDRESS_N"\n
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -ca/--controller_address "CONTROLLER_ADDRESS" -nt/--number_of_tokens NUMBER_OF_TOKENS -rd/--rewards_destination "REWARD_DESTINATION" -va/--validator_address "VALIDATOR_ADDRESS"\n
  python %(prog)s -s/--seed "MNEMONIC_PHRASE" -ca/--controller_address "CONTROLLER_ADDRESS" -nt/--number_of_tokens NUMBER_OF_TOKENS -rd/--rewards_destination "REWARD_DESTINATION" -va/--validator_address "VALIDATOR_ADDRESS_1","VALIDATOR_ADDRESS_2","VALIDATOR_ADDRESS_N"\n
    """
# validator
# guide
exampleGuide = """
Description
  Guide interface to Polkadot..

example:
  python %(prog)s

"""
