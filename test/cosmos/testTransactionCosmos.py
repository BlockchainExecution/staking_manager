import json

from code_src.staking.cosmos.fxn_decorator_implementations.accountImplementation import AccountImplementation
from code_src.staking.cosmos.fxn_decorator_implementations.transactionImplementationUtils import CosmosTransactionUtils
from config import cosmosActiveConfig
from Logger import myLogger

activeConfig = cosmosActiveConfig
logger = myLogger('testing logger')
sender_addr = "cosmos18thxn5pjlwnukkufpuwhwln25n978cjwdtl2h8"
mnemonic = "skill beauty tape never chest mobile scatter coral slab surround divorce awesome army tail actor system manage slice name scout fault mask fruit state"
derivation_path = "m/44'/118'/0'/0/0"
recipient = "cosmos1qtxxcdjk9zxt9we7hvuzjl48e0x8c0e4nt6c0g"
amount = 1 * activeConfig.coinDecimalPlaces

validator_src_address = "cosmosvaloper1clpqr4nrk4khgkxj78fcwwh6dl3uw4epsluffn"
validator_dst_address = "cosmosvaloper1ec3p6a75mqwkv33zt543n6cnxqwun37rr5xlqv"

accountNum, sequence = 0,0
privKey = AccountImplementation(config=activeConfig, logger=logger, mnemonic=mnemonic,
                                derivation_path=derivation_path).getPrivateKeyFromMnemonic()

"""
"""

tx_0 = CosmosTransactionUtils(
    privkey=privKey,
    account_num=accountNum,
    sequence=sequence,
    fee=activeConfig.fee,
    gas=activeConfig.gas,
    memo=activeConfig.memo,
    chain_id=activeConfig.chain_id,
    sync_mode=activeConfig.sync_mode,
)

tx_0.addTransferMsgSend(
    recipient=recipient, amount=amount
)

addTransferMsgSend_tx = tx_0.get_pushable()
print(addTransferMsgSend_tx)

# (self, delegationType, validator_address: str, amount: int, denom: str = "uatom")
# MsgDelegate
tx_1 = CosmosTransactionUtils(
    privkey=privKey,
    account_num=accountNum,
    sequence=sequence,
    fee=activeConfig.fee,
    gas=activeConfig.gas,
    memo=activeConfig.memo,
    chain_id=activeConfig.chain_id,
    sync_mode=activeConfig.sync_mode,
)
tx_1.addTransferMsgDelegate(delegationType="MsgDelegate", validator_address=validator_src_address, amount=amount)
addTransferMsgDelegateDelegate_tx = tx_1.get_pushable()
print(addTransferMsgDelegateDelegate_tx)

# MsgUndelegate
tx_2 = CosmosTransactionUtils(
    privkey=privKey,
    account_num=accountNum,
    sequence=sequence,
    fee=activeConfig.fee,
    gas=activeConfig.gas,
    memo=activeConfig.memo,
    chain_id=activeConfig.chain_id,
    sync_mode=activeConfig.sync_mode,
)
tx_2.addTransferMsgDelegate(delegationType="MsgUndelegate", validator_address=validator_src_address, amount=amount)
addTransferMsgDelegateUndelegate_tx = tx_2.get_pushable()
print(addTransferMsgDelegateUndelegate_tx)
# MsgWithdrawDelegationReward
tx_3 = CosmosTransactionUtils(
    privkey=privKey,
    account_num=accountNum,
    sequence=sequence,
    fee=activeConfig.fee,
    gas=activeConfig.gas,
    memo=activeConfig.memo,
    chain_id=activeConfig.chain_id,
    sync_mode=activeConfig.sync_mode,
)
tx_3.addTransferMsgDelegate(delegationType="MsgWithdrawDelegationReward", validator_address=validator_src_address, amount=amount)
addTransferMsgDelegateWithdrawDelegationReward_tx = tx_3.get_pushable()
print(addTransferMsgDelegateWithdrawDelegationReward_tx)

# addTransferMsgBeginRedelegate
tx_4 = CosmosTransactionUtils(
    privkey=privKey,
    account_num=accountNum,
    sequence=sequence,
    fee=activeConfig.fee,
    gas=activeConfig.gas,
    memo=activeConfig.memo,
    chain_id=activeConfig.chain_id,
    sync_mode=activeConfig.sync_mode,
)
tx_4.addTransferMsgBeginRedelegate(validator_src_address=validator_src_address,validator_dst_address=validator_dst_address,amount=amount)
addTransferMsgBeginRedelegate_tx = tx_4.get_pushable()
print(json.dumps(addTransferMsgBeginRedelegate_tx, indent=4, sort_keys=True))


# addTransferMsgModifyWithdrawAddress
tx_5 = CosmosTransactionUtils(
    privkey=privKey,
    account_num=accountNum,
    sequence=sequence,
    fee=activeConfig.fee,
    gas=activeConfig.gas,
    memo=activeConfig.memo,
    chain_id=activeConfig.chain_id,
    sync_mode=activeConfig.sync_mode,
)
tx_5.addTransferMsgModifyWithdrawAddress(withdraw_address=recipient)
addTransferMsgModifyWithdrawAddress_tx = tx_5.get_pushable()
print(json.dumps(json.loads(addTransferMsgModifyWithdrawAddress_tx), indent=2))