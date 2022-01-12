import unittest
from common import venv_env, main_script
from utils import executeCliCommand

"""
    "seed": skill beauty tape never chest mobile scatter coral slab surround divorce awesome army tail actor system manage slice name scout fault mask fruit state,
    "derivation_path": m/44'/118'/0'/0/0,
    "private_key": 072ed13728ffbca87950f022a17780b13e110c64be40bae56f29d3f98373e20d,
    "public_key": 03d22e027e57cc24e9fa7bfe98b8a85ce96f0c8862b6e08d6cb5b0b908db3483da,
    "address": cosmos18thxn5pjlwnukkufpuwhwln25n978cjwdtl2h8
"""

seed_0 =  "oak enact invite stereo grunt what stay erode matter where into copper"
addr_0 = "cosmos1uvenyjazulhzyd4707k7gracxpfmffa6vmvewf"

seed_1 = "truth effort scatter pioneer add possible battle typical satoshi genius silent merry"
addr_1 = "cosmos1k6a85zhwxnh3zth2zk897zmsgtyt99r580qjsx"

seed_2 = "news rhythm angry during earn cloth fun lounge apart beyond hat morning"
addr_2 = "cosmos17lgg3gwazagrqkdcyeqcn2jw9f59n4pumd9jjk"


# test class AccountImplementation
class AccountTest(unittest.TestCase):
    def setUp(self):
        pass

    # test func createNewAccount
    def test_create(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_create ", "atom", "account", "create")
        self.assertTrue("please store in a save place:" in stdIn)

    # test func getAllAccountInfo
    def test_info(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_info", "atom", "account", "info", "-ca", addr_0)
        self.assertTrue(f"Available Balance" in stdIn)

    def test_info_failure(self):
        stdIn, sdtOut = executeCliCommand(venv_env, main_script, "test_info_failure", "atom", "account", "info", "-ca")
        self.assertFalse(f"account {addr_0} infos" in stdIn)


if __name__ == '__main__':
    unittest.main()
