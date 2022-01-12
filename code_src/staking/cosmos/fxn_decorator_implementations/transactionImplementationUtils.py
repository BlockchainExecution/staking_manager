from code_src.staking.cosmos.fxn_decorator_implementations.accountImplementation import *
import base64
import hashlib
import json
from typing import Any, Dict, List
import ecdsa
from config import cosmosActiveConfig


class CosmosTransactionUtils:
    """A Cosmos transaction.

    After initialization, one or more token transfers can be added by
    calling the `add_transfer()` method. Finally, call `get_pushable()`
    to get a signed transaction that can be pushed to the `POST /txs`
    endpoint of the Cosmos REST API.
    """

    def __init__(
            self,
            *,
            privkey: bytes,
            account_num: int,
            sequence: int,
            fee: int,
            gas: int,
            fee_denom: str = "uatom",
            memo: str = "",
            chain_id: str = "cosmoshub-4",
            hrp: str = cosmosActiveConfig.DEFAULT_BECH32_HRP,
            sync_mode: cosmosActiveConfig.SyncMode = "sync",
    ) -> None:
        self._privkey = privkey
        self._account_num = account_num
        self._sequence = sequence
        self._fee = fee
        self._fee_denom = fee_denom
        self._gas = gas
        self._memo = memo
        self._chain_id = chain_id
        self._hrp = hrp
        self._sync_mode = sync_mode
        self._msgs: List[dict] = []

    def addTransferMsgSend(self, recipient: str, amount: int, denom: str = "uatom") -> None:
        transfer = {
            "type": "cosmos-sdk/MsgSend",
            "value": {
                "from_address": privkey_to_address(self._privkey, hrp=self._hrp),
                "to_address": recipient,
                "amount": [{"denom": denom, "amount": str(amount)}],
            },
        }
        self._msgs.append(transfer)

    def addTransferMsgDelegate(self, delegationType, validator_address: str, amount: int, denom: str = "uatom"):
        # cosmos-sdk/MsgDelegate ,cosmos-sdk/MsgUndelegate ,MsgWithdrawDelegationReward
        transferDelegate = {
            "type": f"cosmos-sdk/{delegationType}",
            "value": {
                "delegator_address": privkey_to_address(self._privkey, hrp=self._hrp),
                "validator_address": validator_address,
                "amount": [{"denom": denom, "amount": str(amount)}],
            },
        }
        self._msgs.append(transferDelegate)

    def addTransferMsgBeginRedelegate(self, validator_src_address: str, validator_dst_address: str, amount: int,
                                      denom: str = "uatom"):
        # MsgBeginRedelegate
        transferRedelegate = {
            "type": "cosmos-sdk/MsgBeginRedelegate",
            "value": {
                "delegator_address": privkey_to_address(self._privkey, hrp=self._hrp),
                "validator_src_address": validator_src_address,
                "validator_dst_address": validator_dst_address,
                "amount": [{"denom": denom, "amount": str(amount)}],
            },
        }
        self._msgs.append(transferRedelegate)

    def addTransferMsgModifyWithdrawAddress(self, withdraw_address: str):
        # cosmos-sdk/MsgModifyWithdrawAddress
        transferModifyWithdrawAddress = {
            "type": "cosmos-sdk/MsgModifyWithdrawAddress",
            "value": {
                "delegator_address": privkey_to_address(self._privkey, hrp=self._hrp),
                "withdraw_address": withdraw_address,
            },
        }
        self._msgs.append(transferModifyWithdrawAddress)

    def get_pushable(self) -> str:
        pubkey = privkey_to_pubkey(self._privkey)
        base64_pubkey = base64.b64encode(pubkey).decode("utf-8")
        pushable_tx = {
            "tx": {
                "msg": self._msgs,
                "fee": {
                    "gas": str(self._gas),
                    "amount": [{"denom": self._fee_denom, "amount": str(self._fee)}],
                },
                "memo": self._memo,
                "signatures": [
                    {
                        "signature": self._sign(),
                        "pub_key": {"type": "tendermint/PubKeySecp256k1", "value": base64_pubkey},
                        "account_number": str(self._account_num),
                        "sequence": str(self._sequence),
                    }
                ],
            },
            "mode": self._sync_mode,
        }
        return json.dumps(pushable_tx, separators=(",", ":"))

    def _sign(self) -> str:
        message_str = json.dumps(self._get_sign_message(), separators=(",", ":"), sort_keys=True)
        message_bytes = message_str.encode("utf-8")

        privkey = ecdsa.SigningKey.from_string(self._privkey, curve=ecdsa.SECP256k1)
        signature_compact = privkey.sign_deterministic(
            message_bytes, hashfunc=hashlib.sha256, sigencode=ecdsa.util.sigencode_string_canonize
        )

        signature_base64_str = base64.b64encode(signature_compact).decode("utf-8")
        return signature_base64_str

    def _get_sign_message(self) -> Dict[str, Any]:
        return {
            "chain_id": self._chain_id,
            "account_number": str(self._account_num),
            "fee": {
                "gas": str(self._gas),
                "amount": [{"amount": str(self._fee), "denom": self._fee_denom}],
            },
            "memo": self._memo,
            "sequence": str(self._sequence),
            "msgs": self._msgs,
        }
