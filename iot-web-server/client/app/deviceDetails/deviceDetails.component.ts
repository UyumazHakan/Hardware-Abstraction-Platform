import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';

import {AlertService, DeviceService, UserService} from '../_services/index';
import { User, Device} from "../_models";

@Component({
    moduleId: module.id,
    templateUrl: 'deviceDetails.component.html'
})

export class DeviceDetailsComponent implements OnInit {
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
        });
        this.getCurrentDevice(this.currentDevice.id);
        console.log(this.currentDevice);
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
            log_directory: "/var/log/iot/"
        };
        return device
    }

    /** returns keys of a Map object as Array */
    public keys(object: any) : Array<string> {
        if (object !== null && object !== undefined) {
            return Array.from(object.keys());
        }
    }

    /** returns values of a Map object as Array */
    public values(object: any) : Array<string> {
        if (object !== null && object !== undefined) {
            return Array.from(object.values());
        }
    }

}
