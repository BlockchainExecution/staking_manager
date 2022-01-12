import json

from Logger import myLogger
from code_src.staking.cosmos.cosmosAPI import CosmosApi
from code_src.staking.cosmos.fxn_decorator_implementations.accountImplementation import AccountImplementation
from code_src.staking.cosmos.fxn_decorator_implementations.transactionImplementation import CosmosTransaction
from config import cosmosActiveConfig

seed_0 = "oak enact invite stereo grunt what stay erode matter where into copper"
addr_0 = "cosmos1uvenyjazulhzyd4707k7gracxpfmffa6vmvewf"

seed_1 = "truth effort scatter pioneer add possible battle typical satoshi genius silent merry"
addr_1 = "cosmos1k6a85zhwxnh3zth2zk897zmsgtyt99r580qjsx"

seed_2 = "news rhythm angry during earn cloth fun lounge apart beyond hat morning"
addr_2 = "cosmos17lgg3gwazagrqkdcyeqcn2jw9f59n4pumd9jjk"

validator_src_address = "cosmosvaloper1qwl879nx9t6kef4supyazayf7vjhennyh568ys"

amount = 0.00001

ai = AccountImplementation(config=cosmosActiveConfig, logger=myLogger("cosmos"), address=addr_1,
                           mnemonic=seed_1,
                           derivation_path="m/44'/118'/0'/0/0")
# ai.getPrivateKeyFromMnemonic()


ai.getAllAccountInfo()
# ai.getAllAccountInfo("cosmos1nm0rrq86ucezaf8uj35pq9fpwr5r82cl8sc7p5")
capi = CosmosApi()

account_number, sequence = capi.getAccountNumberAndSequence(addr_0)
print(account_number, sequence)
ai.getPrivateKeyFromMnemonic()
# Signature data creation
"""
"""
"""
# account
# balance
print(capi.getAccountBalance(addr1))
print(capi.getAccountBalance(addr2))
# getAccountDelegationsInfo
print(capi.getAccountDelegationsInfo(addr1))
print(capi.getAccountDelegationsInfo(addr2))
# getAccountUnbondingDelegationsInfo
print(capi.getAccountUnbondingDelegationsInfo(addr1))
print(capi.getAccountUnbondingDelegationsInfo(addr2))
"""
# info
"""print(CosmosApi().getAccountInfo(addr1))
print(CosmosApi().getAccountInfo(addr2))"""

tx_0 = CosmosTransaction(config=cosmosActiveConfig,
                                logger=myLogger("test tx"),
                                mnemonic=seed_0,
                                derivation_path="m/44'/118'/0'/0/0",
                                recipient=addr_0,
                                amount=amount).createTransactionObject()

tx_0.addTransferMsgDelegate(delegationType="MsgDelegate", validator_address=validator_src_address, amount=amount)
addTransferMsgDelegateDelegate_tx = tx_0.get_pushable()

# print(json.loads(pushable_tx)['tx']['msg'][0])
# print(CosmosApi().sendDelegation(delegation_action="delegations",delegatorAddr="cosmos18thxn5pjlwnukkufpuwhwln25n978cjwdtl2h8",pushable_tx=pushable_tx))
# x_64 = base64.b64encode(bytes(pushable_tx, encoding='utf8'))
# print(x_64)
# print(pushable_tx)
print(capi.encodeSignedTransaction(signed_transaction=json.dumps(addTransferMsgDelegateDelegate_tx)))
# print(pushable_tx)
# print(CosmosApi().sendSignedTransaction(pushable_tx=pushable_tx))
"""import httpx

api_base_url = "https://api.cosmos.network"
print(httpx.post(api_base_url + "/txs", data=pushable_tx).text)"""

"""pushable_tx = {"tx": {"msg": [{"type": "cosmos-sdk/MsgSend",
                               "value": {"from_address": "cosmos1lgharzgds89lpshr7q8kcmd2esnxkfpwvuz5tr",
                                         "to_address": "cosmos103l758ps7403sd9c0y8j6hrfw4xyl70j4mmwkf",
                                         "amount": [{"denom": "uatom", "amount": "387000"}]}},
                              {"type": "cosmos-sdk/MsgSend",
                               "value": {"from_address": "cosmos1lgharzgds89lpshr7q8kcmd2esnxkfpwvuz5tr",
                                         "to_address": "cosmos1lzumfk6xvwf9k9rk72mqtztv867xyem393um48",
                                         "amount": [{"denom": "uatom", "amount": "123"}]}}],
                      "fee": {"gas": "70000", "amount": [{"denom": "uatom", "amount": "1000"}]}, "memo": "",
                      "signatures": [{
                                         "signature": "uPK+lk6zYHpWRXZOLKfAaMfSO13BRVz3OaP159VohighEQt+aGuoJo+OmswhSctqOXNYM//vb2YnZE+danL+PA==",
                                         "pub_key": {"type": "tendermint/PubKeySecp256k1",
                                                     "value": "A49sjCd3Eul+ZXyof7qO460UaO73otrmySHyTNSLW+Xn"},
                                         "account_number": "11335", "sequence": "0"}]}, "mode": 0}
import httpx

api_base_url = "https://api.cosmos.network/cosmos/tx/v1beta1/txs"
print(httpx.post(api_base_url, json=pushable_tx).text)"""
