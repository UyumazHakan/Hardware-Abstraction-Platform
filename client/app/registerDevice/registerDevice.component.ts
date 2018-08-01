import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { AlertService, UserService, DeviceService } from '../_services/index';
import { User, Device } from "../_models";

@Component({
    moduleId: module.id,
    templateUrl: 'registerDevice.component.html'
})

export class RegisterDeviceComponent {
    model: any = {
        id: "",
        name: "",
        created_by: "",
        description: "",
        board_type: "raspberry_pi",
    };

    loading = false;
    currentUser: User;

    constructor(
        private router: Router,
        private userService: UserService,
        private alertService: AlertService,
        private deviceService: DeviceService) {

        this.currentUser = JSON.parse(localStorage.getItem('currentUser'));
        this.model.created_by = this.currentUser.username;
    }

    // ref: https://stackoverflow.com/questions/26501688/a-typescript-guid-class
    public registerDevice() {
        this.model.id = this.newGuid();
        this.loading = true;

        this.deviceService.create(this.model).subscribe(
            data => {
                this.loading = false;
                this.router.navigate(['/all_devices']);
                alert("Device is registered successfully");
                this.alertService.success("Device is registered successfully");
            }, error2 => {
                this.loading = false;
                console.log(error2);
                alert("Error occurred: " + error2.message);
                this.alertService.error(error2.message);
            }
        );
    }

    public newGuid() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
            return v.toString(16);
        });
    }
}
