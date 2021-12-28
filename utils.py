import os
import sys
from subprocess import Popen, PIPE, STDOUT


def get_project_root_dir():
    return os.path.dirname(os.path.abspath(__file__))


def printTmp(printMe):
    print("\n**************** %s ****************\n" % printMe)


# def executeCliCommand(venv_env, main_script, func, *args):
#     cmdList = [venv_env, main_script]
#     for arg in args:
#         cmdList.append(arg)

#     #printTmp(cmdList)
#     p = Popen(cmdList, text=True, shell=True, stdin=PIPE, stdout=PIPE,
#               stderr=STDOUT)
#     stdIn, sdtOut = p.communicate()
#     printTmp(f"{func} \n{stdIn}")
#     return stdIn, sdtOut

"""
 Lucas:
 I'm able to run the tests with the below implementation of executeCliCommand
 but not the above (commented out) implementation. When you run the tests
 on your machine, you can comment out my code below and uncomment yours above.
 I think the long term solution is to run the tests in a docker container (maybe on aws),
 so that it's agnostic to the system it's running on

 I also put the execution paths in config.py, so you'll need to comment out
 mine there as well.
"""
def executeCliCommand(venv_env, main_script, func, *args):
    cmdList = [venv_env, main_script]
    for arg in args:
        cmdList.append(arg)

    # Double check that this function actually works on mac and then delete below commented
    #
    # # !! shell=False and set stderr=PIPE !!
    # p = Popen(cmdList, text=True, shell=False, stdin=PIPE, stdout=PIPE,
    #           stderr=PIPE)
    # stdout, logOutput = p.communicate()
    # return logOutput, stdout # only logOutput is really important here

    if sys.platform.lower().startswith("win"):
        p = Popen(cmdList, text=True, shell=True, stdin=PIPE, stdout=PIPE,
                  stderr=STDOUT)
    else:
        p = Popen(cmdList, text=True, stdin=PIPE, stdout=PIPE,
                  stderr=STDOUT)
    stdIn, sdtOut = p.communicate()
    printTmp(f"{func} \n{stdIn}")
    return stdIn, sdtOut
