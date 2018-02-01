#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
MAIN_SH_FILE="sensors.sh"
MAIN_FILE="system_manager.py"

sleep 1m

if ! pgrep -f $DST_DIR/$MAIN_FILE > /dev/null
	then
	python3 $DIR/$MAIN_FILE &
fi

sleep 5m

sudo bash $DIR/$MAIN_FILE &
