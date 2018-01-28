import { DeviceService} from "../_services/device.service";
import { AlertService} from "../_services/alert.service";

﻿import { Injectable } from '@angular/core';
import {Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, ActivatedRoute} from '@angular/router';
import {Observable} from "rxjs/Observable";

@Injectable()
export class EditAuthGuard implements CanActivate {

    constructor(private router: Router,
                private deviceService: DeviceService,
                private alertService: AlertService) {}

    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
        var device_id = route.params["id"];
        let currentUser = JSON.parse(localStorage.getItem('currentUser'));
        return this.deviceService.getById(device_id).map(data => {
            if (currentUser && currentUser["username"] === data["created_by"]) {
                return true;
            }
            this.router.navigate(['/devices/details/' + device_id]);
            this.alertService.error("You can't edit other user's devices");
            return false;
        }).catch((err) => {
            this.router.navigate(['/all_devices']);
            this.alertService.error(err);
            return Observable.of(false);
        });
    }
}