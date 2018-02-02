var mongoose = require('mongoose');
﻿var config = require('config.json');
var Schema = mongoose.Schema;


var bootstrap_server = new Schema({
    ip_address: String,
    port: Number
});

var io_entry = new Schema({
    type: String,
    name: String,
    pin : Number,
    base_dir: String,
    slave_name: String,
    index_key: Number,
    bmp_address: String,
    gpioadcchannel: Number,
    gpioadsvalue: Number,
    gpiopullupdown: String,
    bcm_pin: Number
});


var communicationProtocol = new Schema({
    id: String,
    device_id: String,
    security_type: String,
    communication_type: String,
    bootstrap_servers: [bootstrap_server],
    topic: String,
    time_interval: Number,
    api_version: {
        type: Number,
        default: config.api_version
    }
});

var device = new Schema({
    id: String,
    type: String,
    input_output: [io_entry],
    interval: Number
});

var deviceSchema = new Schema({
    id: String,
    name: {
        type: String,
        // required: true,
        unique: true
    },
    created_by: String,
    description: String,
    log_directory: {
        type: String,
        default: "/var/log/iot/"
    },
    board_type: {
        type: String,
        // required: true
    },
    log_level: Number,
    communication_protocols: [communicationProtocol],
    devices: [device]
});
var Device = mongoose.model('Device', deviceSchema);
module.exports = Device;