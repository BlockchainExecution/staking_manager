import argparse
import os
import sys

from utils import get_project_root_dir

MyHelpFormatter = argparse.RawTextHelpFormatter

main_script = os.path.join(get_project_root_dir(), "StakingManager.py")
if sys.platform.lower().startswith("win"):
    venv_env = os.path.join(get_project_root_dir(), "venv\Scripts\python.exe")
else:
    venv_env = os.path.join(get_project_root_dir(), "venv/bin/python3")
