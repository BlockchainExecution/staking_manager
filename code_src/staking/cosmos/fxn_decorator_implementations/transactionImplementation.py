import sys

from code_src.staking.cosmos.fxn_decorator_implementations.accountImplementation import *

from code_src.staking.cosmos.fxn_decorator_implementations.transactionImplementationUtils import CosmosTransactionUtils


class CosmosCall:
    """
    """

    def __init__(self, config, cli_name, call_params, mnemonic):
        self.activeConfig = config
        self.call_params = call_params
        self.mnemonic = mnemonic
        self.logger = myLogger(cli_name)
        self.logger.info("Start %s Program." % cli_name)

    def __call__(self, func):
        self.logger.info("execute %s function." % func.__name__)
        if func.__name__ == "delegate":
            print("delegate")

        if func.__name__ == "unbonding_delegations":
            print("unbonding_delegations")

        # redelegations
        if func.__name__ == "redelegations":
            print("redelegations")

        self.__exit__()

    def __exit__(self):
        # close connection with remote socket
        # self.activeConfig.activeSubstrate.close()
        # exit system
        sys.exit(0)


class CosmosTransaction(object):
    def __init__(self, config, logger, mnemonic, derivation_path=None, amount=None, recipient=None,
                 delegationType=None,
                 validator_address=None, validator_src_address=None, validator_dst_address=None, withdraw_address=None):
        self.activeConfig = config
        self.logger = logger
        self.mnemonic = mnemonic

        # none parameters
        self.derivation_path = derivation_path
        if delegationType is None:
            self.derivation_path = self.activeConfig.DEFAULT_DERIVATION_PATH
        self.amount = amount
        self.recipient = recipient
        self.delegationType = delegationType
        self.validator_address = validator_address
        self.validator_src_address = validator_src_address
        self.validator_dst_address = validator_dst_address
        self.withdraw_address = withdraw_address

        # transaction params
        self.denom = self.activeConfig.denom
        self.fee = self.activeConfig.fee
        self.gas = self.activeConfig.gas
        self.memo = self.activeConfig.memo
        self.chain_id = self.activeConfig.chain_id
        self.sync_mode = self.activeConfig.sync_mode

        # Transactions

    def createTransactionObject(self):
        privKey = AccountImplementation(config=self.activeConfig, logger=self.logger, mnemonic=self.mnemonic,
                                        derivation_path=self.derivation_path).getPrivateKeyFromMnemonic()
        sender_addr = privkey_to_address(privKey, hrp=self.activeConfig.DEFAULT_BECH32_HRP)
        accountInfo = AccountImplementation(config=self.activeConfig, logger=self.logger, address=sender_addr,
                                            mnemonic=self.mnemonic).getAllAccountInfo()
        accountNum, sequence = accountInfo[4], accountInfo[5]

        tx = CosmosTransactionUtils(
            privkey=privKey,
            account_num=accountNum,
            sequence=sequence,
            fee=self.fee,
            gas=self.gas,
            memo=self.memo,
            chain_id=self.chain_id,
            sync_mode=self.sync_mode,
        )

        return tx

    def createTransferMsgSend(self):
        return self.createTransactionObject().addTransferMsgSend(recipient=self.recipient, amount=self.amount,
                                                                 denom=self.denom)

    # MsgDelegate
    def createTransferMsgDelegateDelegate(self):
        return self.createTransactionObject().addTransferMsgDelegate(delegationType="MsgDelegate",
                                                                     validator_address=self.validator_address,
                                                                     amount=self.amount, denom=self.denom)

    # MsgUndelegate
    def createTransferMsgDelegateMsgUndelegate(self):
        return self.createTransactionObject().addTransferMsgDelegate(delegationType="MsgUndelegate",
                                                                     validator_address=self.validator_address,
                                                                     amount=self.amount, denom=self.denom)

    # MsgWithdrawDelegationReward
    def createTransferMsgDelegateMsgWithdrawDelegationReward(self):
        return self.createTransactionObject().addTransferMsgDelegate(delegationType="MsgWithdrawDelegationReward",
                                                                     validator_address=self.validator_address,
                                                                     amount=self.amount, denom=self.denom)

    def createTransferMsgBeginRedelegate(self):
        return self.createTransactionObject().addTransferMsgBeginRedelegate(
            validator_src_address=self.validator_src_address,
            validator_dst_address=self.validator_dst_address,
            amount=self.amount, denom=self.denom)

    def createTransferMsgModifyWithdrawAddress(self):
        return self.createTransactionObject().addTransferMsgModifyWithdrawAddress(withdraw_address=self.recipient)



