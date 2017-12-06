#!/bin/bash

CONFIG="config.json"
DEV_CONFIG="config.dev_local.json"
LOG_DIR="/var/log/iot"

MAIN_FILE="system_manager.py"

if [ ! -f $CONFIG ]
	then
		sudo cp $DEV_CONFIG $CONFIG
fi

if [ ! -d $LOG_DIR ]
	then
		sudo mkdir $LOG_DIR
fi

python $MAIN_FILE