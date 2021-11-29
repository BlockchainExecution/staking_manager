import json
import sys
from bip39 import bip39_validate
# TODO: can you confirm the below github for the substrateinterface library?
from substrateinterface import Keypair # github: https://github.com/polkascan/py-substrate-interface
from substrateinterface.exceptions import SubstrateRequestException
from config import activeConfig
from Logger import myLogger
from code_src.staking.dot.fxn_decorator_implementations.accountManagerUtils import *


"""
Generic class for executing account related calls for DOT
The following calls are made to this class:
* All calls in accountingArgParser.py (mnemonic, keypair, info, create)
"""
class DotAccountCall:
    def __init__(self, mnemonic="", ss58_address=""):
        self.cli_name = "Accounting"
        self.mnemonic = mnemonic
        self.ss58_address = ss58_address
        self.logger = myLogger(self.cli_name)
        self.logger.info("Start %s Program." % self.cli_name)

    def createMnemonic(self):
        mnemonic = Keypair.generate_mnemonic()
        createMnemonicLogMessage = f"""create mnemonic phrase

    mnemonic : {mnemonic}

    note : please write down this mnemonic in paper and stored in a save place.
    learn more about mnemonic : https://coinmarketcap.com/alexandria/glossary/mnemonic-phrase
            """
        try:
            self.logger.info(createMnemonicLogMessage)
            return mnemonic
        except Exception as e:
            self.logger.critical(f"error : {e}")
            return False

    def getAccountInfos(self, ss58_address):
        try:
            value = activeConfig.activeSubstrate.query('System', 'Account', params=[ss58_address]).value
            fee_frozen = int(value['data']['fee_frozen']) / activeConfig.coinDecimalPlaces
            free = int(value['data']['free']) / activeConfig.coinDecimalPlaces
            reserved = int(value['data']['reserved']) / activeConfig.coinDecimalPlaces
            misc_frozen = int(value['data']['misc_frozen']) / activeConfig.coinDecimalPlaces

            self.logger.info(f"""account {ss58_address} infos

    nonce : {value['nonce']}
    consumers : {value['consumers']}
    providers : {value['providers']}
    sufficients : {value['sufficients']}
    free : {free} {activeConfig.coinName}
    reserved : {reserved} {activeConfig.coinName}
    misc_frozen : {misc_frozen} {activeConfig.coinName}
    fee_frozen : {fee_frozen} {activeConfig.coinName}
    """)
        except Exception as e:
            self.logger.error(f"{e}")

    def createAccount(self) -> json:
        createAccountMnemonic = self.createMnemonic()
        createAccountKeyPair = dotCreateKeyPair(self.logger, createAccountMnemonic)
        # check if mnemonic is created if this pass keypair will pass without errors
        if not createAccountKeyPair:
            return False
        return True

    def __call__(self, func):
        name = func.__name__
        if name == "mnemonic":
            self.createMnemonic()
        elif name == "create":
            self.createAccount()
        elif name == "info":
            self.getAccountInfos(self.ss58_address)
        elif name == "keypair":
            dotCreateKeyPair(self.logger, mnemonic=self.mnemonic)
        else:
            pass


# TODO:
# * rename AccountBalance class; better inheretence/abstraction
# * use accountManager
# * called in substrateCallManagerUtils.py
class AccountBalanceForBonding:
    def __init__(self):
        #self.ss58_address = ss58_address
        return

    @staticmethod
    def getAccountBalance(ss58_address):
        # query balance info for an account
        accountBalanceInfo = activeConfig.activeSubstrate.query('System', 'Account',
                                                                params=[ss58_address]).value

        # we only need free and reserved information from the balance info
        # free and reserved explained: https://wiki.polkadot.network/docs/learn-accounts#balance-types
        # TODO: decide what the account balance calculation "should" be, i.e. free + reserved or only free?
        free,reserved = accountBalanceInfo['data']['free'], accountBalanceInfo['data']['reserved']
        printTmp(free)

        # free and reserved are given as uint quantity; convert to float
        totalAccountBalance = free / activeConfig.coinDecimalPlaces + reserved / activeConfig.coinDecimalPlaces

        return totalAccountBalance

