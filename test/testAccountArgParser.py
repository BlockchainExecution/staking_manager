import unittest
from common import venv_env, main_script
from utils import executeCliCommand

account = "5C7piVESupk6paengZYaGMzdU79YTgWKoafJPfE76pYkwdEM"
mnemonic = "tomorrow pet when height sight target term flip deposit web moment wine"
mnemonic13 = "tomorrow pet when height sight target term flip deposit web moment wine gth"
mnemonicMinMax = "tomorrow pet when height sight target term flip deposit web moment winefdgfdgfdgfdg"
mnemonicInvalidChar = "t#morrow pet w'en height sight target term flip /eposit web moment wine"


# test class AccountImplementation
class AccountTest(unittest.TestCase):
    def setUp(self):
        pass

    # test func createNewAccount
    def test_create(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_create ", "dot", "account", "create")
        self.assertTrue("<Keypair (address=" in stdIn)

    # test func getAllAccountInfo
    def test_info(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_info", "dot", "account", "info", "-ca", account)
        self.assertTrue(f"account {account} infos" in stdIn)

    def test_info_failure(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_info_failure", "dot", "account", "info", "-ca")
        self.assertFalse(f"account {account} infos" in stdIn)

    # test func createMnemonic
    def test_mnemonic(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_mnemonic", "dot", "account", "mnemonic")
        self.assertTrue(
            "learn more about mnemonic : https://coinmarketcap.com/alexandria/glossary/mnemonic-phrase" in stdIn)

    # test func getAddressFromMnemonic
    def test_keypair(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_keypair", "dot", "account", "keypair", "-m",
                                          mnemonic)
        self.assertTrue(
            "<Keypair (address=5C7piVESupk6paengZYaGMzdU79YTgWKoafJPfE76pYkwdEM)>" in stdIn)

    # lengthMnemonic not in [12, 15, 18, 21, 24]
    def test_keypair_length_mnemonic_less_then_ten(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_keypair_length_mnemonic_less_then_ten", "dot",
                                          "account", "keypair", "-m",
                                          " ".join(mnemonic.split(" ")[:8]))
        self.assertTrue("A bad mnemonic as been passed to create the keypair" in stdIn)

    def test_keypair_length_mnemonic_no_in_standard(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_keypair_length_mnemonic_no_in_standard", "dot",
                                          "account", "keypair", "-m", mnemonic13)
        self.assertTrue("Number of words must be one of the following: [12, 15, 18, 21, 24]" in stdIn)

    # check word len in mnemonic min = 2 max = 8 or the mnemonic doesn't have valid word
    def test_keypair_length_mnemonic_min_max(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_keypair_length_mnemonic_min_max", "dot",
                                          "account", "keypair", "-m", mnemonicMinMax)
        self.assertTrue(
            "Please check for messing strings" in stdIn)

    # Checking mnemonic for invalid characters (non alphabet) "[@_!#$%^&*()<>?/|}{~:]0123456789"
    def test_keypair_mnemonic_invalid_characters(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_keypair_mnemonic_invalid_characters", "dot",
                                          "account", "keypair", "-m", mnemonicInvalidChar)
        self.assertTrue(
            "Mnemonic words must be alphabet words" in stdIn)


if __name__ == '__main__':
    unittest.main()
