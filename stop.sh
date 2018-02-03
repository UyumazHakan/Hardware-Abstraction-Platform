DST_DIR="/home/$USER/sensors"

if pgrep -f $DST_DIR/system_manager.py > /dev/null
	then
	sudo pkill -9 -f $DST_DIR/system_manager.py
else
	echo "Nothing to stop"
fi