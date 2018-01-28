import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule }    from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { AppComponent }  from './app.component';
import { routing }        from './app.routing';

import { AlertComponent } from './_directives/index';
import { AuthGuard } from './_guards/index';
import { EditAuthGuard } from './_guards/index';
import { JwtInterceptorProvider, ErrorInterceptorProvider } from './_helpers/index';
import { AlertService, AuthenticationService, DeviceService, UserService } from './_services/index';
import { HomeComponent } from './home/index';
import { LoginComponent } from './login/index';
import { RegisterComponent } from './register/index';
import { RegisterDeviceComponent } from './registerDevice/index';
import { AllDevicesComponent } from './allDevices/index';
import { EditDeviceComponent}  from "./editDevice/index";
import { DeviceDetailsComponent}  from "./deviceDetails/index";


@NgModule({
    imports: [
        BrowserModule,
        FormsModule,
        HttpClientModule,
        routing,
    ],
    declarations: [
        AppComponent,
        AlertComponent,
        HomeComponent,
        LoginComponent,
        RegisterComponent,
        RegisterDeviceComponent,
        AllDevicesComponent,
        EditDeviceComponent,
        DeviceDetailsComponent
    ],
    providers: [
        AuthGuard,
        EditAuthGuard,
        AlertService,
        AuthenticationService,
        UserService,
        DeviceService,
        JwtInterceptorProvider,
        ErrorInterceptorProvider
    ],
    bootstrap: [AppComponent]
})

export class AppModule { }