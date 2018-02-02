import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';

import {AlertService, DeviceService, UserService} from '../_services/index';
import { User, Device} from "../_models";
import { forEach } from "@angular/router/src/utils/collection";
import { appConfig } from "../app.config";

@Component({
    moduleId: module.id,
    templateUrl: 'deviceDetails.component.html'
})

export class DeviceDetailsComponent implements OnInit {
    apiUrl: String;

    currentDevice: Device;
    loading = false;
    currentUser: User;
    is_enough_logs = false;
    file_paths: string[] = [];
    trimmed_file_paths: string[] = []; // split \ / etc. for better UI

    constructor(
        private router: Router,
        private userService: UserService,
        private alertService: AlertService,
        private deviceService: DeviceService,
        private route: ActivatedRoute) {

        // initialize entities
        this.currentUser = JSON.parse(localStorage.getItem('currentUser'));
        this.apiUrl = appConfig.apiUrl;
    }

    ngOnInit() {
        this.currentDevice = this.createDeviceEntity();

        this.route.params.subscribe(params => {
            this.currentDevice.id = params['id'];
        });
        this.getCurrentDevice(this.currentDevice.id);

    }

    getCurrentDevice(id: string) {
        this.deviceService.getById(id).subscribe( data => {
            console.log("retrieved", data);
            // attributes retrieved from server & populated automatically
            this.currentDevice.name = data["name"];
            this.currentDevice.description = data["description"];
            this.currentDevice.board_type = data["board_type"];
            this.currentDevice.log_directory = data["log_directory"];
            this.currentDevice.log_level = data["log_level"];

            // also retrieve the api version
            this.deviceService.getApiVersion().subscribe(api_version => {
                this.currentDevice.api_version = Number(api_version);
            });

            this.populateDeviceAttributes(data);

            // also retrieve paths of log files
            // this.deviceService.getFilePaths(this.currentDevice).subscribe(filePaths => {
            //     this.file_paths = filePaths; // keep the original for download
            //     console.log(filePaths);
            //     for (var i = 0; i < filePaths.length; i++) {
            //
            //         // https://stackoverflow.com/questions/423376/how-to-get-the-file-name-from-a-full-path-using-javascript
            //         var file_name = filePaths[i].replace(/^.*[\\\/]/, '');
            //         console.log(this.file_paths[i]);
            //         this.trimmed_file_paths.push(file_name);
            //     }
            //
            // });

        }, error => {
            this.alertService.error(error);
            this.loading = false;
        });
    }

    private populateDeviceAttributes(data: Object) {
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
            log_directory: "/var/log/iot/",
            log_level: null
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
