import json

import requests as r
from config import cosmosActiveConfig


class CosmosApi(object):
    def __init__(self):
        self.activeConfig = cosmosActiveConfig
        self.apiUrl = self.activeConfig.apiUrl

    @staticmethod
    def reqGet(url, data_in=None):
        if data_in:
            return r.get(url=url, data=data_in).json()
        else:
            return r.get(url=url).json()

    @staticmethod
    def reqPost(url, data_in=None):
        """
        requests.post(url, data={key: value}, json={key: value}, args)
        """
        if data_in:
            return r.post(url=url, data=data_in)
        else:
            return r.post(url=url)

    # node_info
    def nodeInfo(self):
        nodeInfoUrl = self.apiUrl.format("node_info")
        return self.reqGet(url=nodeInfoUrl).json()

    # Transaction
    def simulateSendTransaction(self, s):
        simulateSendTransactionUrl = self.apiUrl.format("/cosmos/tx/v1beta1/simulate")

    def sendSignedTransaction(self, pushable_tx):
        sendSignedTransactionUrl = self.apiUrl.format(f"txs")
        print(sendSignedTransactionUrl)

        return self.reqPost(url=sendSignedTransactionUrl, data_in=pushable_tx)

    def encodeSignedTransaction(self, signed_transaction):
        # encodeSignedTransactionUrl = self.apiUrl.format("/cosmos/tx/v1beta1/txs/encode")
        # https://api.cosmos.network/txs/encode
        encodeSignedTransactionUrl = self.apiUrl.format("/cosmos/tx/v1beta1/txs/encode")
        return self.reqPost(url=encodeSignedTransactionUrl, data_in=signed_transaction).json()

    def decodeSignedTransaction(self, encoded_transaction):
        pass

    # Staking
    # /staking/delegators/{delegatorAddr}/delegations
    def sendDelegation(self, delegation_action, delegatorAddr, pushable_tx):
        # delegation_action --> delegations, unbonding_delegations and redelegations <--
        sendDelegationUrl = self.apiUrl.format(f"/staking/delegators/{delegatorAddr}/{delegation_action}")
        params = {"body": pushable_tx}
        return self.reqPost(url=sendDelegationUrl, data_in=params).json()

    # Get a Tx by hash
    def getATxByhash(self, txHash):
        getATxByhashurl = self.apiUrl.format(f"/cosmos/tx/v1beta1/txs/{txHash}")
        return self.reqGet(url=getATxByhashurl)

    # Validators
    def getListOfLastestValidator(self):
        validatorSetUrl = self.apiUrl.format("validatorsets/latest")
        results = self.reqGet(url=validatorSetUrl)
        return [addr['address'] for addr in results['result']['validators']]

    # Account
    def getAccountBalance(self, address):
        availableBalance = 0.0
        balanceUrl = self.apiUrl.format(f"bank/balances/{address}")
        # print(balanceUrl)
        result = self.reqGet(url=balanceUrl)['result']
        print(result)
        if result and result is not None:
            for res in result:
                if res['denom'] == self.activeConfig.denom:
                    availableBalance = float(res['amount']) / self.activeConfig.coinDecimalPlaces

        return availableBalance

    def getAccountDelegationsInfo(self, delegatorAddr):
        delegatedBalance = 0.0
        stackingUrl = self.apiUrl.format(f"/staking/delegators/{delegatorAddr}/delegations")
        result = self.reqGet(url=stackingUrl)['result']
        if result and result is not None:
            for delegatedRes in result:
                delegatedBalance += float(delegatedRes['balance']['amount'])
        return delegatedBalance / 10 ** 6

    def getAccountUnbondingDelegationsInfo(self, delegatorAddr):
        unbondingDelegationsAmount = 0.0
        unbondingDelegationsUrl = self.apiUrl.format(f"staking/delegators/{delegatorAddr}/unbonding_delegations")
        result = self.reqGet(url=unbondingDelegationsUrl)['result']
        if result and result is not None:
            for res in result:
                entries = res['entries']
                for entrie in entries:
                    unbondingDelegationsAmount += float(entrie['balance'])
        return unbondingDelegationsAmount / 10 ** 6

    # rewards
    def getAccountRewardsInfo(self, delegatorAddr):
        rewardBalance = 0.0
        accountRewardsUrl = self.apiUrl.format(f"/distribution/delegators/{delegatorAddr}/rewards")
        result = self.reqGet(url=accountRewardsUrl)['result']
        if result and result is not None:
            if result['total'] is not None and len(result['total']) != 0:
                rewardBalance = float(result['total'][0]['amount']) / 10 ** 6
        return rewardBalance

    def getAccountInfo(self, address):
        infoUrl = self.apiUrl.format(f"auth/accounts/{address}")
        result = self.reqGet(url=infoUrl)['result']
        if result and result is not None:
            return result['value']
        else:
            return ""

    def getAccountNumberAndSequence(self, SIGNER_ADDRESS):
        account_number, sequence = 0, 0
        getAccountNumberAndSequenceUrl = self.apiUrl.format(f"auth/accounts/{SIGNER_ADDRESS}")
        print(self.reqGet(url=getAccountNumberAndSequenceUrl))
        result = self.reqGet(url=getAccountNumberAndSequenceUrl)['result']
        if result and result is not None:
            try:
                if result['value']['account_number']:
                    account_number = result['value']['account_number']
            except:
                pass
            try:
                if result['value']['sequence']:
                    sequence = result['value']['sequence']
            except:
                pass

        return account_number, sequence
