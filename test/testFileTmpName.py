# import generic dependencies
import json
import sys
# import different logger?
import argparse
import unittest
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
* Add some tests...
* Rename file...
* Include the argparser in the tests -> e2e

"""

def printTmp(printMe):
	print("\n\n************* %s *************\n\n" %printMe)


if __name__ == "__main__":

	printTmp("In main in testFileTmpName.py")
	# below 3 lines work as expected
	import sys
	printMe = sys.argv[1:]
	printTmp("Command is: %s" %printMe)

	# tempHelperTestFile.main() ~ does not call main, AttributeError, would need to change StakingManager
	#execfile('file.py')

	# make e2e tests this way... expected function behavior.
	testCmd = "python StakingManager.py dot accounting create"
	testCmd1 = "StakingManager.py dot accounting create"

	import os
	# need to set directory
	# os.system(testCmd)

	# stream = os.popen("python StakingManager.py dot accounting create")
	# myOut = stream.read()
	# printTmp(myOut)

	import subprocess

	argList = ['StakingManager.py', 'dot', 'accounting', 'create']
	testCmdList = ['python'] + argList
	process = subprocess.Popen(testCmdList,
	                     stdout=subprocess.PIPE, 
	                     stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()
	printTmp(stdout)
	printTmp(stderr)

	# What do I want to test in output?
	# 1) address
	# 2) keypair
	# 3) log message? later, keep it simple (MVP)

	"""
	Testing the accounting commands
	"""
	# create mnemonic
	# how do I want to write these tests...
	# start with "e2e" tests which demonstrate the intended functionality of the system




	# get address from mnemonic

	# get account info

	# create an account


	"""
	Testing the bonding commands
	"""

