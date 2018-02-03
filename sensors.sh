#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
MAIN_SH_FILE="sensors.sh"
MAIN_FILE="system_manager.py"
LOG_DIR="/var/log/iot/"

#sleep 1m




if ! pgrep -f $DIR/$MAIN_FILE > /dev/null
	then
	CURRENT_DIR=$(pwd)
	cd $LOG_DIR

	for LOG_FILE in "$LOG_DIR"/*
		do
			LOG_FILE_BASENAME_EXT=${LOG_FILE##*/}
			LOG_FILE_EXT=${LOG_FILE_BASENAME_EXT##*.}
			LOG_FILE_BASENAME=${LOG_FILE_BASENAME_EXT%.*}
			LOG_FILE_TAR=$LOG_FILE_BASENAME".tar.gz"
			if [ ! "$LOG_FILE_EXT" = ".tar.gz" ];
				then
				tar -czf $LOG_FILE_TAR $LOG_FILE_BASENAME_EXT
				rm $LOG_FILE_BASENAME_EXT
			fi
		done

	cd $CURRENT_DIR
	echo "Starting script again..."
	python3 $DIR/$MAIN_FILE &
fi



sleep 5m

sudo bash $DIR/$MAIN_SH_FILE &
