# import generic dependencies
import json
import sys
# import different logger?
import argparse
import unittest
from substrateinterface import Keypair # github: https://github.com/polkascan/py-substrate-interface
import bip39
# import hypothesis# Add to requirements?
# import specific project files
# don't import AccountImplementation (class)
# from code_src.staking.dot.fxn_decorator_implementations.accountImplementation import DotAccountCall
import tempHelperTestFile


# __name = "StakingManager TESTS"
# logger = myLogger(__name)
# logger.info("Running full test suite...")

"""
TODO:
* Major WIP - DOES NOT WORK
+ Add mnemonic validations in MnemonicManager and call that function
+ Add more tests
+ Needs major refactoring
"""

def printTmp(printMe):
	print("\n\n************* %s *************\n\n" %printMe)


# code for validating mnemonic, can add later
# from: https://github.com/trezor/python-mnemonic/blob/master/src/mnemonic/mnemonic.py
# def check(self, mnemonic: str) -> bool:
#     mnemonic_list = self.normalize_string(mnemonic).split(" ")
#     # list of valid mnemonic lengths
#     if len(mnemonic_list) not in [12, 15, 18, 21, 24]:
#         return False
#     try:
#         idx = map(
#             lambda x: bin(self.wordlist.index(x))[2:].zfill(11), mnemonic_list
#         )
#         b = "".join(idx)
#     except ValueError:
#         return False
#     l = len(b)  # noqa: E741
#     d = b[: l // 33 * 32]
#     h = b[-l // 33 :]
#     nd = int(d, 2).to_bytes(l // 33 * 4, byteorder="big")
#     nh = bin(int(hashlib.sha256(nd).hexdigest(), 16))[2:].zfill(256)[: l // 33]
#     return h == nh


# separate logger for testing?



if __name__ == "__main__":

	printTmp("In main in testFileTmpName.py")
	# below 3 lines work as expected
	import sys
	printMe = sys.argv[1:]
	printTmp("Command is: %s" %printMe)

	# tempHelperTestFile.main() ~ does not call main, AttributeError, would need to change StakingManager
	#execfile('file.py')

	"""
	Testing the accounting commands
	"""

	"""
	Test 1: Accounting command > create
	"""

	# create mnemonic
	# how do I want to write these tests...
	# start with "e2e" tests which demonstrate the intended functionality of the system

	# make e2e tests this way... expected function behavior.
	testCmd = "python StakingManager.py dot accounting create"
	testCmd1 = "StakingManager.py dot accounting create"

	import os
	# need to set directory
	# os.system(testCmd)

	# stream = os.popen("python StakingManager.py dot accounting create")
	# myOut = stream.read()
	# printTmp(myOut)

	import sys
	sys.path.append("../staking_manager")

	# Remember to _always_ set config.py to test -> should always be test, set here
	# Make sure this is executed correctly
	import config
	config.activeConfig = config.TestingConfig

	def generateCliDotAccountingCommand(cmd: list) -> list:
		argList = ['StakingManager.py', 'dot', 'accounting']
		argList = argList + cmd
		command = ['python'] + argList
		return command

	def executeCliCommand(commandToExecute: list):
		"""
		Sends command as list to CLI. Returns the output as UTF8 string
		"""
		import subprocess

		process = subprocess.Popen(commandToExecute,
		                     stdout=subprocess.PIPE, 
		                     stderr=subprocess.PIPE)
		stdout, logOutput = process.communicate()
		printTmp(stdout) #nothing gets printed here, kind of useless
		printTmp(logOutput)
		printTmp(type(logOutput))
		# converting logOutput from types bytes to string
		logOutput = logOutput.decode('utf-8')
		return logOutput

	# What do I want to test in output?
	# 1) address
	# 2) keypair
	# 3) log message? later, keep it simple (MVP)

	createCmd = generateCliDotAccountingCommand(["create"])
	createCmdOutput = executeCliCommand(createCmd)

	import re

	# mnemonic can be btwn 12 and 24 words
	teststring = re.search("(mnemonic :)((\\s\\w+){12,24})", createCmdOutput)
	# get the relevant string from Match object (returned by re)
	teststring = teststring.group()
	# get rid of the "mnemonic : ", leaving only the mnemonic itself
	testMnemonic = teststring[11:]

	# TODO: validate the mnemonic is legitimate in MnemonicImplementation; import and call fxn

	# seem to be in another shell, probably because of subprocess
	# I must be in /test/, need to import from parent dir
	# Even though print(os.getcwd()) returns /staking_manager/
	# ugh https://stackoverflow.com/questions/714063/importing-modules-from-parent-folder/50194143#50194143

	# fixed the ModuleNotFoundError: No module named 'code_src' error
	# what happens if executed twice?
	# import sys
	# sys.path.append("../staking_manager")

	from code_src.staking.dot.fxn_decorator_implementations.accountImplementationUtils import *
	from Logger import myLogger

	keypairObjectWithAddress = Keypair.create_from_mnemonic(mnemonic=testMnemonic, 
		ss58_format=config.activeConfig.ss58_format)
	# get public key in ss58 format
	# https://polkascan.github.io/py-substrate-interface/#substrateinterface.Keypair
	addressToValidate = keypairObjectWithAddress.ss58_address

	# getting address to validate
	teststring = re.search("(address=)\\w+", createCmdOutput)
	# get the relevant string from Match object (returned by re)
	teststring = teststring.group()
	# get rid of the "mnemonic : ", leaving only the mnemonic itself
	testAddress = teststring[8:]

	# printTmp(addressToValidate)
	# printTmp(testAddress)

	if(addressToValidate == testAddress):
		printTmp("TEST 1 PASSED")
	else:
		printTmp("TEST 1 FAILED")



	"""
	Test 2: Accounting command > info
	"""
	# Account 5GVz... is fixed, it should not recieve/send funds
	infoCmd = generateCliDotAccountingCommand(["info", "-ca", "5GVzG3QJvRc6MEtxaJZnLB3PAhQT8eMgesqgHxYiiQJE4HNv"])
	infoCmdOutput = executeCliCommand(infoCmd)

	def validateTest2(infoCmdOutput):
		# match free : 0.314159
		teststring = re.search("(free : \\d\\.\\d+)", infoCmdOutput)

		# get the relevant string from Match object (returned by re)
		if (teststring):
			teststring = teststring.group()
			testValue = teststring[7:]
			return testValue
		else:
			printTmp("TEST 2 FAILED")
			return False

	testValue = validateTest2(infoCmdOutput)

	if(float(testValue) == 0.314159):
		printTmp("TEST 2 PASSED")
	else:
		printTmp("TEST 2 FAILED")


	"""
	Test 3: Accounting command > mnemonic
	"""
	mnemonicCmd = generateCliDotAccountingCommand(["mnemonic"])
	mnemonicCmdOutput = executeCliCommand(mnemonicCmd)

	def validateTest3(infoCmdOutput):
		# match free : 0.314159
		teststring = re.search("(mnemonic :)((\\s\\w+){12,24})", infoCmdOutput)

		# get the relevant string from Match object (returned by re)
		if (teststring):
			teststring = teststring.group()
			testValue = teststring[:11]
			return testValue
		else:
			printTmp("TEST 2 FAILED")
			return False

	testValue = validateTest3(mnemonicCmdOutput)

	# TODO: need a much better way to check mnemonic correctness
	if(testValue == "mnemonic : "):
		printTmp("TEST 3 PASSED")
	else:
		printTmp("TEST 3 FAILED")

	"""
	Test 4: Accounting command > keypair
	"""
	# TODO: create this test, Test 4. Probably not urgent given tests 1-3


	"""
	Testing the bonding commands
	"""

