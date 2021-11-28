import json
import sys
from bip39 import bip39_validate
# TODO: can you confirm the below github for the substrateinterface library?
from substrateinterface import Keypair # github: https://github.com/polkascan/py-substrate-interface
from substrateinterface.exceptions import SubstrateRequestException
from config import activeConfig
from Logger import myLogger


# TODO: Should we keep this fxn outside DotAccountCall, why?

"""
Function creates a keypair for dot given a mnemonic and returns it (or exits the system if it fails).
It's currently kept outside the DotAccountCall as an auxilary function in order to keep the pre-defined
function set in DotAccountCall (i.e. createMnemonic, getAccountInfos, etc.)
Function is (currently) called *only* from DotAccountCall
"""
def dotCreateKeyPair(logger, mnemonic):
    invalidCharacters = "[@_!#$%^&*()<>?/|}{~:]0123456789"

    # If a mnemonic is not passed in, the default in the above library will be used
    # however, we will enforce that "something" is passed in to avoid the default (len 10 is arbitrary)
    if (len(mnemonic) < 10):
            logger.critical("A bad mnemonic as been passed to create the keypair")
            return False

    try:
        # Keypair ~ https://github.com/polkascan/py-substrate-interface#keypair-creation-and-signing
        key = Keypair.create_from_mnemonic(mnemonic=mnemonic, ss58_format=activeConfig.ss58_format)
        logger.info(f"""create key pair\n\n
    {key}
     \n\n""")

        # do a quick verification that the key signs normally
        if key.verify("This is a test message", key.sign("This is a test message")):
            return key
        else:
            # if the key verification fails, exit immediatly
            logger.critical("\nDO NOT USE KEY. KEY INCORRECTLY GENERATED.\n")
            return False

    except ValueError:
        # more thorough check for the mnemonic below

        # split mnemonic by space into words
        splitMnemonic = mnemonic.split(" ")

        lengthMnemonic = len(splitMnemonic)
        # check word length and special character
        lengthWordInMnemonic = any(word for word in splitMnemonic if len(word) < 3 or len(word) > 8)
        lengthOfDigitInMnemonicIfAny = any(s for s in mnemonic if s in invalidCharacters)

        # Checking mnemonic length
        # length doesn't meet the standard
        if lengthMnemonic not in [12, 15, 18, 21, 24]:
            logger.critical(
                "Number of words must be one of the following: [12, 15, 18, 21, 24], but it is not (%d)."
                % lengthMnemonic)
            return False

        # length meet the standard
        else:
            # Checking mnemonic for invalid characters (non alphabet)
            if lengthOfDigitInMnemonicIfAny:
                logger.critical("Mnemonic words must be alphabet words.")
                return False

            # check word len in mnemonic min = 2 max = 8 or the mnemonic doesn't have valid word
            elif lengthWordInMnemonic or not bip39_validate(mnemonic):
                logger.critical("Please check for messing strings.")
                return False
