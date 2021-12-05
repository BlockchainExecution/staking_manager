# import generic dependencies
import json
import sys
import argparse
# import specific project files
# don't import AccountImplementation (class)
from testFileTmpName import *


def printTmp(printMe):
	print("\n\n************* %s *************\n\n" %printMe)

if __name__ == "__main__":
	printTmp("In main in tempHelperTestFile.py")
	import sys
	printMe = sys.argv[1:]
	printTmp("Command is: %s" %printMe)