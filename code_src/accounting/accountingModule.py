import json
from database.databaseMdule import DatabaseGlobal
from substrateinterface import Keypair, SubstrateInterface
from common import substrate_rococo


class Accounting(object):
    def __init__(self):
        self.substrate = substrate_rococo
        self.dbg = DatabaseGlobal()

    @staticmethod
    def create_mnemonic():
        return Keypair.generate_mnemonic()

    @staticmethod
    def create_keypair(mnemonic) -> Keypair:
        return Keypair.create_from_mnemonic(mnemonic)

    def account_infos(self, ss58_address):
        return self.substrate.query('System', 'Account', params=[ss58_address]).value

    def create_account(self) -> json:
        mne = self.create_mnemonic()
        keyp = self.create_keypair(mne)

        infos = {"mnemonic": mne, "Keypair": keyp}
        #sql = """insert into dotaccounts(mnemonic,keypair,account_infos) values('%s','%s');""" % (
            #mne, keyp)
        #self.dbg.execute(sql, "save accounts to database")
        return infos

    def get_accounts(self):
        sql = """select * from accounts;"""
        return self.dbg.run(sql, "get all accounts")

#print(Accounting().create_account())
#Accounting().get_accounts()
#print(Accounting().account_infos("5CwXYYfkbgATv6SNZLnXqCV77YRFHXcCGrmQcqZQqGaTm5tj"))




