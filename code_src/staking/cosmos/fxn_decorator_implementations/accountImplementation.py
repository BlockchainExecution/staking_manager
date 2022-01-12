import json
from Logger import myLogger
from cosmospy import generate_wallet, BIP32DerivationError, seed_to_privkey, privkey_to_pubkey, pubkey_to_address, \
    privkey_to_address

from code_src.staking.cosmos.cosmosAPI import CosmosApi
from config import cosmosActiveConfig


class AccountImplementation:
    """
    """

    def __init__(self, config, logger, mnemonic=None, address=None, derivation_path=None):
        self.activeConfig = config
        self.logger = logger
        self.mnemonic = mnemonic
        self.address = address
        self.derivation_path = derivation_path

    def createNewAccount(self):
        # MnemonicImplementation is called here instead of self.createMnemonic() because it's better
        # for functions in the AccountImplementation class to directly call the implementation classes

        cosmosWallet = generate_wallet()
        # check if mnemonic is created if this pass keypair will pass without errors
        if not cosmosWallet:
            return False

        createWalletLogMessage = f"""create wallet    
please store in a save place: 
    ⎇ seed : {cosmosWallet['seed']}
    ⎇ derivation_path : {cosmosWallet['derivation_path']}
    ⎇ private_key : {cosmosWallet['private_key'].hex()}
    ⎇ public_key : {cosmosWallet['public_key'].hex()}
    ⎇ address : {cosmosWallet['address']}
                    """

        self.logger.info(createWalletLogMessage)
        return cosmosWallet

    def getPrivateKeyFromMnemonic(self):
        try:
            privkey = seed_to_privkey(self.mnemonic, path=self.derivation_path)
            self.logger.info(f""" Private Key
    private key : {privkey.hex()}
""")
            return privkey

        except BIP32DerivationError:
            self.logger.error("No valid private key in this derivation path!")

    def getPublicKeyFromPrivateKey(self, priv_key):
        privkey = bytes.fromhex(priv_key)
        pubkey = privkey_to_pubkey(privkey)
        self.logger.info(f""" Public Key
    public key : {pubkey.hex()}
""")
        return pubkey.hex()

    def getAddressFromPublicKey(self, pub_key):
        pubkey = bytes.fromhex(pub_key)
        addr = pubkey_to_address(pubkey)

        self.logger.info(f""" Address
    address : {addr}
        """)
        return addr

    def getAddressFromPrivateKey(self, priv_key):
        privkey = bytes.fromhex(priv_key)
        addr = privkey_to_address(privkey)

        self.logger.info(f"""
    address : {addr}
                """)
        return addr

    def getAllAccountInfo(self):
        acctInfo = CosmosApi().getAccountInfo(self.address)
        balance = CosmosApi().getAccountBalance(self.address)
        delegatedBalance = CosmosApi().getAccountDelegationsInfo(self.address)
        unbondingDelegationsBalance = CosmosApi().getAccountUnbondingDelegationsInfo(self.address)

        rewardBalance = CosmosApi().getAccountRewardsInfo(self.address)

        # https://www.cryps.info/en/microAtomiccoin_to_ATOM/1/
        sequence = 0
        if acctInfo:
            availableBalance = float(balance) / 10 ** 6
            accountNum = acctInfo['account_number']
            # sequence = acctInfo['sequence']
        else:
            availableBalance = 0.0
            accountNum = 0
            sequence = 0
        self.logger.info(f""" {self.address}
    Available Balance : {availableBalance} {self.activeConfig.coinName}
    Delegated Balance : {delegatedBalance} {self.activeConfig.coinName}
    Reward Balance : {rewardBalance} {self.activeConfig.coinName}
    Unbonding Amount : {unbondingDelegationsBalance} {self.activeConfig.coinName}
    Account Number : {accountNum}
    Account Sequence : sequence
""")

        return availableBalance, delegatedBalance, rewardBalance, unbondingDelegationsBalance, accountNum, sequence


class AtomAccountCall:
    """
    Class for executing account related calls for DOT
    The following calls are made to this class:
    * All calls in accountingArgParser.py (mnemonic, keypair, info, create)
    """

    def __init__(self, mnemonic="", address="", derivation_path=""):
        self.cli_name = "Accounting"
        self.mnemonic = mnemonic
        self.address = address
        self.derivation_path = derivation_path
        self.logger = myLogger(self.cli_name)
        self.logger.info("Start %s Program." % self.cli_name)

    def __call__(self, func):
        name = func.__name__

        if name == "create":
            AccountImplementation(config=cosmosActiveConfig, logger=self.logger).createNewAccount()
        elif name == "info":
            AccountImplementation(config=cosmosActiveConfig, logger=self.logger,
                                  address=self.address).getAllAccountInfo()
        elif name == "keypair":
            priv_key = AccountImplementation(config=cosmosActiveConfig, logger=self.logger, mnemonic=self.mnemonic,
                                             derivation_path=self.derivation_path).getPrivateKeyFromMnemonic()
            AccountImplementation(config=cosmosActiveConfig, logger=self.logger,
                                  address=self.address).getPublicKeyFromPrivateKey(priv_key)
        else:
            pass


# helper print method for checking the code, can delete function and all references anytime
def printTmp(printMe):
    print("\n\n****************\n %s \n****************\n\n" % printMe)


def jsonPrityPrint(jsn):
    print(json.dumps(jsn, indent=4, sort_keys=True))


"""
    "seed": skill beauty tape never chest mobile scatter coral slab surround divorce awesome army tail actor system manage slice name scout fault mask fruit state,
    "derivation_path": m/44'/118'/0'/0/0,
    "private_key": 072ed13728ffbca87950f022a17780b13e110c64be40bae56f29d3f98373e20d,
    "public_key": 03d22e027e57cc24e9fa7bfe98b8a85ce96f0c8862b6e08d6cb5b0b908db3483da,
    "address": cosmos18thxn5pjlwnukkufpuwhwln25n978cjwdtl2h8
"""
ai = AccountImplementation(config=cosmosActiveConfig, logger=myLogger("cosmos"))
# ai.createNewAccount()
"""ai.getPrivateKeyFromMnemonic(
    "skill beauty tape never chest mobile scatter coral slab surround divorce awesome army tail actor system manage slice name scout fault mask fruit state",
    "m/44'/118'/0'/0/0")
ai.getPublicKeyFromPrivateKey("072ed13728ffbca87950f022a17780b13e110c64be40bae56f29d3f98373e20d")
ai.getAddressFromPrivateKey("072ed13728ffbca87950f022a17780b13e110c64be40bae56f29d3f98373e20d")
ai.getAddressFromPublicKey("03d22e027e57cc24e9fa7bfe98b8a85ce96f0c8862b6e08d6cb5b0b908db3483da")"""

# ai.getAllAccountInfo("cosmos19xe0dvn6cae6wem5pfs96jrnkrk8dwxdl83mjx")
# ai.getAllAccountInfo("cosmos1nm0rrq86ucezaf8uj35pq9fpwr5r82cl8sc7p5")
