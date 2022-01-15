from Logger import myLogger

"""

This file can still be used for adding new, unorganized code before it gets refactored into
a more organized architecture/file system

"""

"""
TODO -

Generic class for executing validator calls to DOT network
The following calls are made to this class:
* All calls in validator.py (validator)
"""


class DotValidatorCall:
    def __init__(self):
        self.cli_name = "Validator"
        self.logger = myLogger(self.cli_name)
        self.logger.info("Start %s Program." % self.cli_name)

    def __exit__(self):
        pass


# helper print method for checking the code, can delete function and all references anytime
def printTmp(printMe):
    print("\n\n****************\n %s \n****************\n\n" % printMe)
