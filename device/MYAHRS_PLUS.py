from device.device import Device
import copy
import serial
import time
import traceback



class MYAHRS_PLUS(Device):

        values = [
        {
            "name": "ROLL",
            "value": None,
            "unit": "%%"
        },
        {
            "name": "PITCH",
            "value": None,
            "unit": "%%"
        },
        {
            "name": "YAW",
            "value": None,
            "unit": "%%"
        },
        {
            "name": "ACCEL_X",
            "value": None,
            "unit": "%%"
        },
        {
            "name": "ACCEL_Y",
            "value": None,
            "unit": "%%"
        },
        {
            "name": "ACCEL_Z",
            "value": None,
            "unit": "%%"
        },
        {
            "name": "GYRO_X",
            "value": None,
            "unit": "%%"
        },
        {
            "name": "GYRO_Y",
            "value": None,
            "unit": "%%"
        },
        {
            "name": "GYRO_Z",
            "value": None,
            "unit": "%%"
        },
        {
            "name": "MAG_X",
            "value": None,
            "unit": "%%"
        },
        {
            "name": "MAG_Y",
            "value": None,
            "unit": "%%"
        },
        {
            "name": "MAG_Z",
            "value": None,
            "unit": "%%"
        },
        {
            "name": "TEMPERATURE",
            "value": None,
            "unit": "%%"
        }
    ]

        def __init__(self, config, callback):
                super(MYAHRS_PLUS, self).__init__(config, callback)
                #self.si1132 = SI1132(str(config["input_output"][0]["pin"]))
                #self.bme280 = BME280(str(config["input_output"][0]["pin"]), 0x03, 0x02, 0x02, 0x02)
                self.read_value_imp = self.__read_value

        def __read_value(self):
                serial_device = '/dev/ttyACM0'
                #serial_device = 'COM5'
                return self.read_example(serial_device)

        def send_command(self,serial_port, cmd_msg):
                cmd_msg = '@' + cmd_msg.strip()
                crc = 0
                for c in cmd_msg:
                    crc = crc ^ ord(c)
                serial_port.write((cmd_msg + '*%02X' % crc + '\r\n').encode())

                #
                # wait for response
                #
                if (cmd_msg != '@trig'):
                    while (True):
                        line = serial_port.readline().strip()
                        line = line.decode()
                        if (line[0] == '~'):
                            return line
        
        def parse_data_message_rpyimu(self,data_message):
                # $RPYIMU,39,0.42,-0.31,-26.51,-0.0049,-0.0038,-1.0103,-0.0101,0.0014,-0.4001,51.9000,26.7000,11.7000,41.5*1F
                data_message = data_message.decode().split('*')[0]
                data_message = data_message.strip()  # discard crc field
                fields = [x.strip() for x in data_message.split(',')]

                if (fields[0] != '$RPY'):
                    return None

                sequence_number, roll, pitch, yaw, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z, temperature = (
                    float(x) for x in fields[1:])
                return (
                    int(sequence_number), roll, pitch, yaw, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y,
                        mag_z,temperature)

        def read_example(self, serial_device):
                
                try:
                    serial_port = serial.Serial(serial_device, 115200, timeout=1.0)
                
                except serial.serialutil.SerialException:
                    print('Can not open serial port(%s)' % (serial_device))
                    traceback.print_exc()
                    return

                # for i in range(50):
                time.sleep(0.5)
                rsp = self.send_command(serial_port, 'version')
                rsp = self.send_command(serial_port, 'mode,AT')
                rsp = self.send_command(serial_port, 'asc_out,RPYIMU')
                self.send_command(serial_port, 'trig')

                line = serial_port.readline().strip()
                #print(line)
                # 'DATA MESSAGE : <%s>' % line

                items = self.parse_data_message_rpyimu(line)
                #print items
                self.values = items
                if self.values == None:
                    print('Error collecting data')
                else:
                    #print(self.values)
                    return self.values
