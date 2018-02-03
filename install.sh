#!/bin/bash
if [[ ! $# -gt 0 ]]
	then
		echo "Usage: sudo bash install.sh [username]"
		exit 0
fi
USERNAME=$1
echo "Starting..."
CONFIG="config.json"
DEV_CONFIG="config.dev_local.json"
MAIN_SH_FILE="sensors.sh"
INSTALL_SCRIPT_NAME="install.sh"
DST_DIR="/home/$USERNAME/sensors"
TMP_DIR="/tmp/sensors"
LOG_DIR="/var/log/iot"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SERVER_IP="http://141.40.254.141:4000"

echo "Installing dependencies..."

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install curl jq wget
pip3 install kafka

echo "Deleting old files..."

if [ -d $TMP_DIR ]
	then
		sudo rm -rf $TMP_DIR
fi

echo "Killing old processes..."

if [ -d $DST_DIR ]
	then
		if pgrep -f $DST_DIR/system_manager.py > /dev/null
			then
			sudo pkill -9 -f $DST_DIR/system_manager.py
		fi
		sudo rm -rf $DST_DIR
fi

echo "Creating log folder..."

if [ ! -d $LOG_DIR ]
	then
		sudo mkdir $LOG_DIR
fi

while true; 
do
	read -p 'Do you want to use web server capabilities?[Y/n] ' yn
	case $yn in
		[Nn]* )
			echo "Creating config file..."
			if [ ! -f $DIR/$CONFIG ]
				then
					sudo cp $DIR/$DEV_CONFIG $DIR/$CONFIG
			fi
			echo "Config file located at $DIR/$CONFIG"
			break
			;;
		[Yy]* )
			while true; 
			do
				read -p 'Username: ' USERNAME_PLATFORM
				read -sp 'Password: ' PASSWORD_PLATFORM
				echo
				DATA='{
				    "username": "'$USERNAME_PLATFORM'",
				    "password": "'$PASSWORD_PLATFORM'"
				}'
				# store the whole response with the status
				HTTP_RESPONSE=$(curl -s -w "HTTPSTATUS:%{http_code}" -X POST \
				 $SERVER_IP/users/authenticate \
				 -H 'Content-Type: application/json' \
				 -d "$DATA")
				HTTP_STATUS=$(echo $HTTP_RESPONSE | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
				HTTP_BODY=$(echo $HTTP_RESPONSE | sed -e 's/HTTPSTATUS\:.*//g')
				if [ ! $HTTP_STATUS -eq 200  ]; then
					echo "Error [$HTTP_BODY]"
					continue
				fi
				break
			done
			TOKEN=$(echo "$HTTP_BODY" | \
			jq -r '.token')
			while true; 
			do
				DEVICES=$(curl -s -X GET \
				 $SERVER_IP/devices/external \
				 -H 'Authorization: Bearer '$TOKEN)
				echo "Your boards:"
				echo "$DEVICES" | jq -r 'to_entries | map("\(.key)\t\(.value.name)\t\(.value.description)") | .[]'
				read -p 'Select a board to configure: ' BOARD_SELECTION
				BOARD_ID=$(echo "$DEVICES" | jq -r '.['$BOARD_SELECTION'].id')
				if [ "$BOARD_ID" == "null" ]; then
					echo "No such a board, try again."
					continue
				fi
				echo "Downloading the config file..."
				HTTP_STATUS=$(wget -q \
				 --server-response \
				 --method GET \
				 --header 'Authorization: Bearer '$TOKEN \
				 --output-document $DIR/$CONFIG \
				 - $SERVER_IP/devices/$BOARD_ID 2>&1 | awk '/^  HTTP/{print $2}')
			 	if [ ! $HTTP_STATUS -eq 200  ]; then
					echo "Could not retrieve asked board configuration, try again."
					continue
				fi
				jq '.username |= . + "'$USERNAME_PLATFORM'" | .password |= . + "'$PASSWORD_PLATFORM'"' $DIR/$CONFIG \
				> $DIR/$CONFIG.tmp && mv $DIR/$CONFIG.tmp $DIR/$CONFIG

				break
			done
			break
			;;
	esac
done




echo "Adding startup functionality..."

sudo echo "#!/bin/bash" > /etc/rc.local
sudo echo "sudo bash $DST_DIR/$MAIN_SH_FILE &" >> /etc/rc.local
sudo echo "exit 0" >> /etc/rc.local



echo "Copying files to destination..."

sudo cp -r $DIR $TMP_DIR

sudo cp -r $TMP_DIR $DST_DIR

sudo rm -rf $TMP_DIR

echo "Running..."

sudo bash $DST_DIR/$MAIN_SH_FILE &

echo "Installation finished."
