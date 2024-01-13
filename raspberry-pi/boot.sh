#!/bin/bash

# activate python venv
source ~/[YOUR_VENV_DIR]/bin/activate >> sh.log

# cd workspace
cd ~/[YOUR_WORKSPACE_DIR] >> sh.log

# run
nohup python main.py >> sh.log