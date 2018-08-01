# READ ME


This document provides a step by step guide to set up the HAL, retrieve data from the sensor devices, send it to various other devices / IoT Core Team.

## Features


-   Support for numerous sensors.

-   Modular and extensible structure.

-   Simple UI to enable user to configure his devices and sensors.

-   Secure data transmission to other devices/IoT Core Layer.

-   Intermediate data storage.

-   Detection of sensor failures.

-   Machine to Machine communication.


## Deployment


-   Clone this repo

-   Assuming that the config web server(https://gitlab.lrz.de/IoT-Practicum-Group/sensors/tree/v2018) is running smoothly, use it to register yourself, create your device and edit the device details accordingly.

-   Make sure to mention the appropriate sensor, communication and security protocols without fail.

-   Make sure that the device is connected to Internet.

-   Install python3.5+ on the device

-   Run `sudo bash install.sh <config-web-server-ip:4000>`

## Components Supported


-   Raspberry Pi:
 - List of sensors mentioned in the [SensorKit X40](http://sensorkit.en.joy-it.net/index.php?title=Main_Page)

-   Odroid XU4:

 -   Weather Board

 -   myAHRS+

 -   List of sensors mentioned in the [SensorKit X40](http://sensorkit.en.joy-it.net/index.php?title=Main_Page) that are based on RPGPIO library



## Usage

### To send data to IoT Core Team


-   Register the device and respective sensors with the IoT Core Team via[ http://iot.pcxd.me:8080/](http://iot.pcxd.me:8080/)

-   Note down the **Sensor_ID**, **Device_ID** and also download the **Device Key**.

-   Login to the config web server and modify the config details accordingly

 -   HAL_custom_id = Sensor_ID

 -   Topic = Device_ID

 -   Bootstrap Server Username = "JWT"

 -   Bootstrap Server Password = Device Key

-   Run `sudo bash install.sh <config-web-server-ip:4000>`  to collect data from the sensor and send it to the IoT Core Team.

## Machine-to-Machine Communication


### To send data to another machine: 

Follow "To send data to IoT Core Team" section except,

-   Topic = (Could be anything)

-   Bootstrap Server Username = (mosquitto username of listener machine, if any or a blank space)

-   Bootstrap Server Password = (mosquitto password of listener machine, if any or a blank space)

-   To receive data in another machine

-   Download files from m2m folder

-   Run `sudo mosquitto_install.sh`

-   To receive data, run - `sudo python3 mqtt_subscribe.py`

## Documentation for Intermediate Data Storage on Edge Device
- http://tinydb.readthedocs.io/en/latest/usage.html


## Contributors
- Ali Naci Uysal ([Github page](https://github.com/alinaciuysal), [LinkedIn page](https://www.linkedin.com/in/ali-naci-uysal/))
- Hakan Uyumaz ([Github page](https://github.com/UyumazHakan), [LinkedIn page](https://www.linkedin.com/in/uyumazhakan/))
- Erkin Kırdan
- Mikayil Murad [LinkedIn page](https://www.linkedin.com/in/mikayilmurad/)
- Anjali Sasihithlu
- Admir Jashari
- Rakibul Alam

## License
>You can check out the full license [here](https://gitlab.lrz.de/IoT-Practicum-Group/sensors/blob/master/LICENSE)

This project is licensed under the terms of the MIT license.