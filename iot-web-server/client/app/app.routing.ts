import { Routes, RouterModule } from '@angular/router';

import { HomeComponent } from './home/index';
import { LoginComponent } from './login/index';
import { RegisterComponent } from './register/index';
import { RegisterDeviceComponent } from './registerDevice/index';
import { EditDeviceComponent } from './editDevice/index';
import { AllDevicesComponent } from './allDevices/index';
import { DeviceDetailsComponent } from './deviceDetails/index';
import { AuthGuard } from './_guards/index';
import { EditAuthGuard } from './_guards/index';

const appRoutes: Routes = [
    { path: 'home', component: HomeComponent},
    { path: 'login', component: LoginComponent },
    { path: 'register', component: RegisterComponent},
    { path: 'register_device', component: RegisterDeviceComponent, canActivate: [AuthGuard] },
    { path: 'all_devices', component: AllDevicesComponent, canActivate: [AuthGuard] },
    { path: 'devices/edit/:id', component: EditDeviceComponent, canActivate: [AuthGuard, EditAuthGuard] },
    { path: 'devices/details/:id', component: DeviceDetailsComponent, canActivate: [AuthGuard] },
    { path: '', component: HomeComponent},

    // otherwise redirect to home
    { path: '**', redirectTo: 'home' }
];

export const routing = RouterModule.forRoot(appRoutes);