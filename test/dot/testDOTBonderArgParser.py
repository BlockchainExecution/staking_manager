import unittest
from common import venv_env, main_script
from utils import executeCliCommand

account = "5C7piVESupk6paengZYaGMzdU79YTgWKoafJPfE76pYkwdEM"
mnemonic = "tomorrow pet when height sight target term flip deposit web moment wine"


class bonderTest(unittest.TestCase):
    def setUp(self):
        pass

    # bond
    def test_bond_without_args(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_bond_without_args ", "dot", "bonder", "bond")
        self.assertTrue(
            "error: the following arguments are required: -m/--mnemonic, -ca/--controller_address, -nt/--number_of_tokens" in stdIn)

    def test_bond_missing_args(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_bond_missing_args ", "dot", "bonder", "bond",
                                          "-m", mnemonic, "-ca", account)
        self.assertTrue(
            "error: the following arguments are required: -nt/--number_of_tokens" in stdIn)

    # BondingValidator
    # BondSize
    def test_bond_size_failure(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_bond_size_failure ", "dot", "bonder", "bond",
                                          "-m", mnemonic, "-ca", account, "-nt", "0.8")
        self.assertTrue(
            "but the minimum required for bonding is" in stdIn)

    # validateAcctBalanceForBonding
    def test_bond_low_balance_failure(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_bond_low_balance_failure ", "dot", "bonder",
                                          "bond",
                                          "-m", mnemonic, "-ca", account, "-nt", "100")
        self.assertTrue(
            "Low balance" in stdIn)

    # validateDecimalPoint
    def test_bond_decimal_point_failure(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_bond_decimal_point_failure ", "dot", "bonder",
                                          "bond",
                                          "-m", mnemonic, "-ca", account, "-nt", "1.25555254548754858")
        self.assertTrue(
            "wrong token value token take max" in stdIn)

    def test_bond_success(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_bond_success ", "dot", "bonder", "bond",
                                          "-m", mnemonic, "-ca", account, "-nt", "1")
        self.assertTrue(
            "sent and included in block" in stdIn)

    def test_bond_failure(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_bond_failure", "dot", "bonder", "bond",
                                          "-m", mnemonic, "-ca", account, "-nt", "1")
        self.assertTrue(
            "AlreadyBonded Stash is already bonded.If you want to bond more coins you can use <bondextra> command line utilities" in stdIn)

    # unbond
    def test_unbond_without_args(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_unbond_without_args ", "dot", "bonder",
                                          "unbond")
        self.assertTrue(
            "error: the following arguments are required: -m/--mnemonic, -nt/--number_of_tokens" in stdIn)

    def test_unbond_missing_args(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_unbond_missing_args ", "dot", "bonder",
                                          "unbond",
                                          "-m", mnemonic)
        self.assertTrue(
            "error: the following arguments are required: -nt/--number_of_tokens" in stdIn)

    def test_unbond_success(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_unbond_success ", "dot", "bonder", "unbond",
                                          "-m", mnemonic, "-nt", "1")
        self.assertTrue(
            "sent and included in block" in stdIn)

    # rebond
    def test_rebond_without_args(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_rebond_without_args ", "dot", "bonder",
                                          "rebond")
        self.assertTrue(
            "error: the following arguments are required: -m/--mnemonic, -nt/--number_of_tokens" in stdIn)

    def test_rebond_missing_args(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_rebond_missing_args ", "dot", "bonder",
                                          "rebond",
                                          "-m", mnemonic)
        self.assertTrue(
            "error: the following arguments are required: -nt/--number_of_tokens" in stdIn)

    def test_rebond(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_rebond_success ", "dot", "bonder", "rebond",
                                          "-m", mnemonic, "-nt", "1")
        self.assertTrue(
            "sent and included in block" in stdIn)

    # bondextra
    def test_bondextra_without_args(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_bondextra_without_args ", "dot", "bonder",
                                          "bondextra")
        self.assertTrue(
            "error: the following arguments are required: -m/--mnemonic, -ca/--controller_address, -nt/--number_of_tokens" in stdIn)

    def test_bondextra_missing_args(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_bondextra_missing_args ", "dot", "bonder",
                                          "bondextra",
                                          "-m", mnemonic,"-ca",account)
        self.assertTrue(
            "error: the following arguments are required: -nt/--number_of_tokens" in stdIn)

    def test_bondextra_success(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_bondextra_success", "dot", "bonder",
                                          "bondextra", "-m", mnemonic,"-ca",account, "-nt", "1")
        self.assertTrue(
            "sent and included in block" in stdIn)

    # withdrawunbonded
    def test_withdrawunbonded_without_args(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_withdrawunbonded_without_args ", "dot",
                                          "bonder", "withdrawunbonded")
        self.assertTrue(
            "error: the following arguments are required: -m/--mnemonic" in stdIn)

    def test_withdrawunbonded_missing_args(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_withdrawunbonded_missing_args ", "dot",
                                          "bonder", "withdrawunbonded",
                                          "-m")
        self.assertTrue(
            "error: argument -m/--mnemonic: expected one argument" in stdIn)

    def test_withdrawunbonded_success(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_withdrawunbonded_success", "dot", "bonder",
                                          "withdrawunbonded",
                                          "-m", mnemonic, "-nss", "1")
        self.assertTrue(
            "sent and included in block" in stdIn)


if __name__ == '__main__':
    unittest.main()
