import json

from code_src.staking.cosmos.fxn_decorator_implementations.accountImplementation import AccountImplementation
from code_src.staking.cosmos.fxn_decorator_implementations.transactionImplementationUtils import CosmosTransactionUtils
from code_src.staking.cosmos.cosmosAPI import CosmosApi
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

capi = CosmosApi()
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

tx_0.addTransferMsgDelegate(delegationType="MsgDelegate", validator_address=validator_src_address, amount=amount)
addTransferMsgDelegateDelegate_tx = tx_0.get_pushable()

jstx = json.dumps(json.loads(addTransferMsgDelegateDelegate_tx), indent=2)

import python3_protobuf

print(json.dumps(json.loads(addTransferMsgDelegateDelegate_tx), indent=2))

print(capi.sendDelegation("MsgDelegate",sender_addr, jstx))

