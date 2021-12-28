import unittest
from common import venv_env, main_script
from utils import executeCliCommand

account = "5C7piVESupk6paengZYaGMzdU79YTgWKoafJPfE76pYkwdEM"
mnemonic = "tomorrow pet when height sight target term flip deposit web moment wine"


class StakeTest(unittest.TestCase):
    def setUp(self):
        pass

    # stake
    def test_stake_without_args(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_stake_without_args", "dot", "stake")
        self.assertTrue(
            "error: the following arguments are required: -m/--mnemonic, -ca/--controller_address, -nt/--number_of_tokens" in stdIn)

    def test_stake_missing_args(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_stake_missing_args ", "dot", "stake",
                                          "-m", mnemonic, "-ca", account)
        self.assertTrue(
            "error: the following arguments are required: -nt/--number_of_tokens" in stdIn)

    def test_stake_success(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_stake_success ", "dot", "stake",
                                          "-m", mnemonic, "-ca", account, "-nt", "1")
        self.assertTrue(
            "sent and included in block" in stdIn)


if __name__ == '__main__':
    unittest.main()
