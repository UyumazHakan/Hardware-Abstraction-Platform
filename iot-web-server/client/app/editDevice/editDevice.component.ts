import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';

import {AlertService, DeviceService, UserService} from '../_services/index';
import { User, Device} from "../_models";

@Component({
    moduleId: module.id,
    templateUrl: 'editDevice.component.html'
})

export class EditDeviceComponent implements OnInit {
    currentDevice: Device;
    loading = false;
    currentUser: User;

    constructor(
        private router: Router,
        private userService: UserService,
        private alertService: AlertService,
        private deviceService: DeviceService,
        private route: ActivatedRoute) {

        // initialize entities
        this.currentUser = JSON.parse(localStorage.getItem('currentUser'));

    }

    ngOnInit() {
        this.currentDevice = this.createDeviceEntity();

        this.route.params.subscribe(params => {
            this.currentDevice.id = params['id'];
            this.getCurrentDevice(this.currentDevice.id);
        });

    }

    getCurrentDevice(id: string) {
        this.deviceService.getById(id).subscribe( data => {

            // attributes retrieved from server & populated automatically
            this.currentDevice.name = data["name"];
            this.currentDevice.description = data["description"];
            this.currentDevice.board_type = data["board_type"];
            this.currentDevice.log_directory = data["log_directory"];

            // also retrieve the api version
            this.deviceService.getApiVersion().subscribe(api_version => {
                this.currentDevice.api_version = Number(api_version);
            });

            // attributes to be filled by the user or retrieved by server. mapper would be useful here...
            this.populateDeviceAttributes(data);

        }, error => {
            console.log("error", error);
            this.alertService.error(error);
            this.loading = false;
        });
    }

    private populateDeviceAttributes(data: Object) {
        console.log("data in populate", data);
        if (!data["communication_protocols"]) {
            this.currentDevice.communication_protocols = [];
        } else {
            this.currentDevice.communication_protocols = data["communication_protocols"];
        }

        if (!data["devices"]) {
            this.currentDevice.devices = [];
        } else {
            this.currentDevice.devices = data["devices"];
        }
    }

    public addIO(device_index: any) {
        let index_key = 0;
        if (this.currentDevice.devices[device_index].hasOwnProperty("input_output")) {
            index_key = this.currentDevice.devices[device_index].input_output.length;
        }
        this.currentDevice.devices[device_index].input_output.push({
            "type": "",
            "name": "",
            "pin": 0,
            "gpiopullupdown": "None",
            "gpioadsvalue": 0,
            "gpioadcchannel": 0,
            "bmp_address": 0,
            "base_dir": "/sys/bus/w1/devices/",
            "bcm_pin": 0,
            "slave_name": "w1_slave",
            "index_key": index_key
        });
    }

    public editDevice() {
        if (this.validateForm()) {
            console.log(this.currentDevice);
            // additional check for odroid: create default array & io if it's selected
            if (this.currentDevice.board_type === 'odroid') {
                this.currentDevice.devices = [];
                this.currentDevice.devices.push({
                    "id": this.newGuid(),
                    "type": "WEATHER2BOARD",
                    "interval": 5,
                    "input_output": []
                });
                this.currentDevice.devices[0].input_output.push({
                    "type": "I2C",
                    "name": "odroid i2c",
                    "pin": 5
                });
            } else if(this.currentDevice.board_type === 'raspberry_pi') {
                for (let i = 0; i < this.currentDevice.devices.length; i++) {
                    for (let j = 0; j < this.currentDevice.devices[i].input_output.length; j++) {
                        let io_entity = this.currentDevice.devices[i].input_output[j];

                        // filter out unnecessary fields
                        if (io_entity.type !== 'OneWireInputOutput') {
                            delete io_entity.slave_name;
                            delete io_entity.base_dir;
                        }
                        if (io_entity.type !== 'GPIOInput') {
                            delete io_entity.gpiopullupdown;
                        }
                        if (io_entity.type !== 'GPIOADCInput') {
                            delete io_entity.gpioadsvalue;
                            delete io_entity.gpioadcchannel;
                        }
                        if (io_entity.type !== 'GPIOBMP280Input') {
                            delete io_entity.bmp_address;
                        }
                        if (io_entity.type !== 'GPIODHTInput') {
                            delete io_entity.bcm_pin;
                        }
                    }
                }
            }
            console.log("device to be updated", this.currentDevice);
            this.deviceService.update(this.currentDevice).subscribe( data => {
                alert("Device is updated successfully");
                this.alertService.success(data["message"]);
            },
            error => {
                alert("Update failed");
                this.alertService.error(error);
            });
        }
    }

    private validateIPAddress(ip_address: string): Boolean {
        if (/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(ip_address)) {
            return true;
        }
        return false;
    }

    private validateForm(): Boolean {
        if (this.currentDevice.communication_protocols.length === 0) {
            this.alertService.error('Specify at least one communication protocol', true);
            return false;
        }
        for (let i = 0; i < this.currentDevice.communication_protocols.length; i++) {
            if (this.currentDevice.communication_protocols[i].bootstrap_servers.length === 0) {
                this.alertService.error('Specify at least one bootstrap server to send data', true);
                return false;
            }
            else {
                for (let j = 0; j < this.currentDevice.communication_protocols[i].bootstrap_servers.length; j++) {
                    if (!this.validateIPAddress(this.currentDevice.communication_protocols[i].bootstrap_servers[j].ip_address)){
                        this.alertService.error('Provide valid ip address(es)');
                        return false;
                    }
                }
            }
        }

        if (this.currentDevice.devices.length === 0 && this.currentDevice.board_type === 'raspberry_pi') {
            this.alertService.error('Specify at least one sensor', true);
            return false;
        }
        else {
            for (let i = 0; i < this.currentDevice.devices.length; i++) {
                if (this.currentDevice.devices[i]["input_output"].length === 0) {
                    this.alertService.error('Specify at least I/O type', true);
                    return false;
                }
            }
        }
        return true;
    }

    public addCommunicationProtocol() {
        this.currentDevice.communication_protocols.push({
            "id": this.newGuid(),
            "device_id": this.currentDevice.id,
            "security_type": "PlainText",
            "communication_type": "Kafka",
            "topic": "sensor-input", // default
            "time_interval": 5,
            "api_version": this.currentDevice.api_version,
            "bootstrap_servers": []
        });
    }

    public removeCommunicationProtocol(index: Number) {
        this.currentDevice.communication_protocols.splice(index, 1);
    }

    public removeAllCommunicationProtocols() {
        this.currentDevice.communication_protocols.splice(0);
    }

    createDeviceEntity(): Device {
        let device: Device = {
            board_type: "",
            description: "",
            created_by: "",
            id: "",
            communication_protocols: [],
            devices: [], // denotes the devices array in our config.json
            name: "",
            api_version: null,
            log_directory: "/var/log/iot/",
            log_level: 0
        };
        return device
    }

    public newGuid(): string {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
            return v.toString(16);
        });
    }

    public addBootstrapServer(communication_protocol_index: any) {
        this.currentDevice.communication_protocols[communication_protocol_index]["bootstrap_servers"].push({
            "ip_address": "",
            "port": 9092
        });
    }

    public removeBootstrapServer(communication_protocol_index: any, bootstrap_server_index: any) {
        this.currentDevice.communication_protocols[communication_protocol_index]["bootstrap_servers"].splice(bootstrap_server_index, 1);
    }

    public removeAllBootstrapServers(communication_protocol_index: any) {
        this.currentDevice.communication_protocols[communication_protocol_index]["bootstrap_servers"].splice(0);
    }

    public removeIO(device_index: any, io_entry_index: any) {
        this.currentDevice.devices[device_index]["input_output"].splice(io_entry_index, 1);
    }

    public removeAllIO(device_index: any) {
        this.currentDevice.devices[device_index]["input_output"].splice(0);
    }

    // do not mix up Device array in our config.json with Device entity here. They are different.
    // for this context, Sensor is a subset of Device
    // for config.json context, Device is a subset of Devices array

    public addDevice() {
        this.currentDevice.devices.push({
            "id": this.newGuid(),
            "type": "",
            "interval": 5,
            "input_output": []
        });
    }

    public removeDevice(index: Number) {
        this.currentDevice.devices.splice(index, 1);
    }

    public removeAllDevices() {
        this.currentDevice.devices.splice(0);
    }
}
