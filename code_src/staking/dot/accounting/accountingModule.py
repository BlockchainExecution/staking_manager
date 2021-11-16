import json
from Logger import myLogger
from substrateinterface import Keypair


class Accounting(object):
    def __init__(self):
        self.name = "Accounting"
        self.logger = myLogger(self.name)

        self.logger.info("Starting accounting Program.")

    def createMnemonic(self):
        return self.logger.info(Keypair.generate_mnemonic())

    def createKeypair(self, mnemonic):
        return self.logger.info(Keypair.create_from_mnemonic(mnemonic))

    def accountInfos(self, active_substrate, ss58_address):
        return self.logger.info(active_substrate.query('System', 'Account', params=[ss58_address]).value)

    def create_account(self) -> json:
        mne = self.createMnemonic()
        keyp = self.createKeypair(mne)
        return self.logger.info(f"mnemonic: {mne}, Keypair: {keyp}")
