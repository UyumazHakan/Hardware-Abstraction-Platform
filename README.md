## Sensor Layer of  IoT Practical Course Project - TUM
This project contains different components to retrieve data from a wide variety of sensors that can be deployed with Raspberry PIs and Odroid devices. 

## Features
- Support for most of the sensors (NOT actuators, i.e. buttons etc.) in [SensorKit X40](http://sensorkit.en.joy-it.net/index.php?title=Main_Page)
- Support for [Odroid XU 4](https://www.odroid.co.uk/hardkernel-odroid-xu4) and its [weather board](http://www.hardkernel.com/main/products/prdt_info.php?g_code=G140264897696)
- Modular & extensible architecture
- Configuration of devices and their sensors easily with the help of its web-server. [See](https://gitlab.lrz.de/IoT-Practicum-Group/sensors/tree/master/iot-web-server)
- Data transfer to [Layer 2](https://gitlab.lrz.de/IoT-Practicum-Group/data_layer)

## Deployment & Usage

- Deploy supported sensors to your device (Raspberry PI, Odroid etc.) and note-down sensors' corresponding PINs etc.
- Clone this repository, and follow [web-server deployment instructions](https://gitlab.lrz.de/IoT-Practicum-Group/sensors/tree/master/iot-web-server)
- Assuming that web-server is running smoothly in a cloud environment, use it to register yourself as a user (write down your username), create a device, and make necessary edit operations for newly-created device.
- Make sure your device is connected to the internet
- Install [Python 3.5+](https://www.python.org/) to your device
- run `sudo bash install.sh <username>` in the root folder of this repository, and follow instructions via command line

## Documentation for Intermediate Data Storage on Edge Device
- http://tinydb.readthedocs.io/en/latest/usage.html

## Contributors
- Ali Naci Uysal ([Github page](https://github.com/alinaciuysal), [LinkedIn page](https://www.linkedin.com/in/ali-naci-uysal/))
- Hakan Uyumaz ([Github page](https://github.com/UyumazHakan), [LinkedIn page](https://www.linkedin.com/in/uyumazhakan/))
- Erkin Kırdan
- Mikayil Murad [LinkedIn page](https://www.linkedin.com/in/mikayilmurad/)

## License
>You can check out the full license [here](https://gitlab.lrz.de/IoT-Practicum-Group/sensors/blob/master/LICENSE)

This project is licensed under the terms of the MIT license.