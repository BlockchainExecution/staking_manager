import os
import sys
from subprocess import Popen, PIPE, STDOUT


def get_project_root_dir():
    return os.path.dirname(os.path.abspath(__file__))


def printTmp(printMe):
    print("\n**************** %s ****************\n" % printMe)


def executeCliCommand(venv_env, main_script, func, *args):
    cmdList = [venv_env, main_script]
    for arg in args:
        cmdList.append(arg)
    if sys.platform.lower().startswith("win"):
        p = Popen(cmdList, text=True, shell=True, stdin=PIPE, stdout=PIPE,
                  stderr=STDOUT)
    else:
        p = Popen(cmdList, text=True, stdin=PIPE, stdout=PIPE,
                  stderr=STDOUT)
    stdIn, sdtOut = p.communicate()
    printTmp(f"{func} \n{stdIn}")
    return stdIn, sdtOut
