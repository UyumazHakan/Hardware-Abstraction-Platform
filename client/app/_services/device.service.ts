import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { appConfig } from '../app.config';
import { Device } from '../_models/index';
import {Observable} from "rxjs/Observable";

@Injectable()
export class DeviceService {
    constructor(private http: HttpClient) { }

    getAll() {
        return this.http.get<Device[]>(appConfig.apiUrl + '/devices');
    }

    getById(id: string) {
        return this.http.get(appConfig.apiUrl + '/devices/' + id);
    }

    create(device: Device){
        return this.http.post(appConfig.apiUrl + '/devices/create', device);
    }

    update(device: Device) {
        return this.http.put(appConfig.apiUrl + '/devices/' + device.id, device);
    }

    delete(id: string) {
        return this.http.delete(appConfig.apiUrl + '/devices/' + id);
    }

    getApiVersion() {
        return this.http.get(appConfig.apiUrl + '/devices/api');
    }

    getFilePaths(device: Device) {
        return this.http.post<string[]>(appConfig.apiUrl + '/devices/getFileNames', device);
    }
}