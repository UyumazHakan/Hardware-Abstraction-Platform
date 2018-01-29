#!/bin/bash
if [[ ! $# -gt 0 ]]
	then
		echo "Usage: sudo bash install.sh [username]"
		exit 0
fi
USERNAME=$1
echo "STARTING..."
CONFIG="config.json"
DEV_CONFIG="config.dev_local.json"
INITD="/etc/init.d"
STARTUP_SCRIPT_NAME="sensor_startup.sh"
STARTUP_SCRIPT="$INITD/$STARTUP_SCRIPT_NAME"
MAIN_SH_FILE="sensors.sh"
INSTALL_SCRIPT_NAME="install.sh"
DST_DIR="/home/$USERNAME/sensors"
TMP_DIR="/tmp/sensors"
LOG_DIR="/var/log/iot"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "DELETING OLD FILES..."



if [ -f $STARTUP_SCRIPT ]
	then
		sudo rm -f $STARTUP_SCRIPT
fi

if [ -d $TMP_DIR ]
	then
		sudo rm -rf $TMP_DIR
fi


if [ -d $DST_DIR ]
	then
		if pgrep -f $DST_DIR/system_manager.py > /dev/null
			then
			sudo pkill -9 -f $DST_DIR/system_manager.py
		fi
		sudo rm -rf $DST_DIR
fi

echo "CREATING LOG DIRECTORY..."

if [ ! -d $LOG_DIR ]
	then
		sudo mkdir $LOG_DIR
fi

echo "CREATING CONFIG FILE..."

if [ ! -f $DIR/$CONFIG ]
	then
		sudo cp $DIR/$DEV_CONFIG $DIR/$CONFIG
fi

echo "ADDING STARTUP FUNCTIONALITY..."

sudo echo "#!/bin/bash" > /etc/rc.local
sudo echo "sudo bash $DST_DIR/$MAIN_SH_FILE &" >> /etc/rc.local
sudo echo "exit 0" >> /etc/rc.local



echo "COPYING FILES TO DESTINATION..."

sudo cp -r $DIR $TMP_DIR

sudo cp -r $TMP_DIR $DST_DIR

sudo rm -rf $TMP_DIR

echo "STARTING..."

sudo bash $DST_DIR/$MAIN_SH_FILE &
echo "FINISHED"