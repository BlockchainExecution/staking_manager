import unittest
from common import venv_env, main_script
from utils import executeCliCommand
from time import sleep

account = "5C7piVESupk6paengZYaGMzdU79YTgWKoafJPfE76pYkwdEM"
mnemonic = "tomorrow pet when height sight target term flip deposit web moment wine"


class ScenarioSuccessTest(unittest.TestCase):
    def setUp(self):
        pass

    # we start by creating an account
    def test_create_account(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_create ", "ksm", "account", "create")
        self.assertTrue("<Keypair (address=" in stdIn)

    # from here we will use
    # account = "5C7piVESupk6paengZYaGMzdU79YTgWKoafJPfE76pYkwdEM"
    # mnemonic = "tomorrow pet when height sight target term flip deposit web moment wine"
    # as testing arguments
    # get the mnemonic of the created account
    def test_mnemonic(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_mnemonic", "ksm", "account", "mnemonic")
        self.assertTrue(
            "learn more about mnemonic : https://coinmarketcap.com/alexandria/glossary/mnemonic-phrase" in stdIn)

    # get created account balance info
    def test_info(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_info", "ksm", "account", "info", "-ca", account)
        self.assertTrue(f"account {account} infos" in stdIn)

    def test_keypair(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_keypair", "ksm", "account", "keypair", "-m",
                                          mnemonic)
        self.assertTrue(
            "<Keypair (address=5C7piVESupk6paengZYaGMzdU79YTgWKoafJPfE76pYkwdEM)>" in stdIn)

    # we will prepare here to stake an amount of a 1 coin
    # manual
    def test_bond_success(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_bond_success ", "ksm", "bounder", "bond",
                                          "-m", mnemonic, "-ca", account, "-nt", "1")
        self.assertTrue(
            "sent and included in block" in stdIn)

    def test_nominate_success(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_bond_without_args ", "ksm", "nominator",
                                          "nominate", "-m", mnemonic)
        self.assertTrue(
            "sent and included in block" in stdIn)

    # automatic
    def test_stake_success(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_stake_success ", "ksm", "stake",
                                          "-m", mnemonic, "-ca", account, "-nt", "1")
        self.assertTrue(
            "sent and included in block" in stdIn)

    # sleep 5 seconds and then continue
    sleep(5)

    # the scenario from here depend on the actual status of the account
    # example
    #   - if an account is already bonded, func will fail
    #       - so in this state we can use bond_extra,withdraw_unbonded
    #   - if we have unbond some coins, and we are not in the end of the actual era we need to wait for the
    #       next era then we can use withdraw bounded coins (withdraw_unbonded)
    #       - This function will success

    def test_unbond_success(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_unbond_success ", "ksm", "bounder", "unbond",
                                          "-m", mnemonic, "-nt", "1")
        self.assertTrue(
            "sent and included in block" in stdIn)

    def test_bondextra_success(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_bondextra_success", "ksm", "bounder",
                                          "bondextra", "-m", mnemonic, "-nt", "1")
        self.assertTrue(
            "sent and included in block" in stdIn)

    def test_withdrawunbonded_success(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_withdrawunbonded_success", "ksm", "bounder",
                                          "withdrawunbonded",
                                          "-m", mnemonic, "-nss", "1")
        self.assertTrue(
            "sent and included in block" in stdIn)


if __name__ == '__main__':
    unittest.main()
