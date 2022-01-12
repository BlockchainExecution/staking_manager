import unittest
from common import venv_env, main_script
from utils import executeCliCommand

account = "5C7piVESupk6paengZYaGMzdU79YTgWKoafJPfE76pYkwdEM"
mnemonic = "tomorrow pet when height sight target term flip deposit web moment wine"


class BounderTest(unittest.TestCase):
    def setUp(self):
        pass

    # nominate
    def test_nominate_without_args(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_bond_without_args ", "dot", "nominator",
                                          "nominate")
        self.assertTrue(
            "error: the following arguments are required: -m/--mnemonic" in stdIn)

    def test_nominate_success(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_bond_without_args ", "dot", "nominator",
                                          "nominate", "-m", mnemonic)
        self.assertTrue(
            "sent and included in block" in stdIn)

    # stop_nominate_tmp
    def test_stop_nominate_tmp_without_args(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_unnominate_tmp_without_args ", "dot",
                                          "nominator",
                                          "stop_nominate_tmp")
        self.assertTrue(
            "error: the following arguments are required: -m/--mnemonic" in stdIn)

    def test_stop_nominate_tmp_success(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_stop_nominate_tmp_success ", "dot", "nominator",
                                          "stop_nominate_tmp", "-m", mnemonic)
        self.assertTrue(
            "sent and included in block" in stdIn)

    # stop_nominate_all
    def test_stop_nominate_all_without_args(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_stop_nominate_all_without_args", "dot",
                                          "nominator",
                                          "stop_nominate_all")
        self.assertTrue(
            "error: the following arguments are required: -m/--mnemonic" in stdIn)

    def test_stop_nominate_all_success(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_unnominate_all_success ", "dot", "nominator",
                                          "stop_nominate_all", "-m", mnemonic,"-nt","3")
        self.assertTrue(
            "sent and included in block" in stdIn)


if __name__ == '__main__':
    unittest.main()
