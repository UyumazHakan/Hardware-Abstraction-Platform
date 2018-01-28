var config = require('config.json');
var _ = require('lodash');
var jwt = require('jsonwebtoken');
var Q = require('q');
var mongo = require('mongoskin');
var deviceSchema = require('../schemas/deviceSchema');
// var db = mongo.db(config.connectionString, { native_parser: true });
// db.bind('devices');

var service = {};

service.getAllDevices = getAllDevices;
service.getById = getById;
service.create = create;
service.update = update;
service.delete = _delete;

module.exports = service;


function getAllDevices() {
    deviceSchema.find({}, function(err, devices) {
        if (err) throw err;
        return devices;
    });
}

function getById(id) {
    deviceSchema.findOne({id: id}, function(err, device) {
        if (err) throw err;
        return device;
    });
}

function create(deviceParam) {
    // create a new device
    var newDevice = deviceSchema({
        id: deviceParam.id,
        name: deviceParam.name,
        description: deviceParam.description,
        log_directory: deviceParam.log_directory,
        board_type: deviceParam.board_type,
    });

    // save the user
    newDevice.save(function(err) {
        if (err) throw err;
        console.log('Device created!');
    });
}

function update(id, deviceParam) {
    var deferred = Q.defer();

    // validation
    db.devices.findById(id, function (err, device) {
        if (err) deferred.reject(err.name + ': ' + err.message);

        if (device.name !== deviceParam.name) {
            // device name has changed so check if the new device name is already taken
            db.devices.findOne(
                { name: deviceParam.name },
                function (err, device) {
                    if (err) {
                        deferred.reject(err.name + ': ' + err.message);
                    }

                    if (device) {
                        // device name already exists
                        deferred.reject('Device name "' + device.name + '" is already taken')
                    } else {
                        updateDevice(deviceParam);
                    }
                });
        } else {
            updateDevice(deviceParam);
        }
    });

    function updateDevice(deviceParam) {

        for(var i = 0; i < deviceParam.devices.length; i++) {
            var device = deviceParam.devices[i];
            var outer_map_to_be_replaced = new Map();
            for(var j = 0; j < device.input_output.length; j++) {
                var inner_map = new Map();
                var key = device.input_output[j][0];
                var value = device.input_output[j][1];
                inner_map.set(key, value);
                outer_map_to_be_replaced.set(j, inner_map);
            }
            deviceParam.devices[i] = outer_map_to_be_replaced;

        }

        // fields to update
        var set = {
            name: deviceParam.name,
            bootstrap_servers: deviceParam.bootstrap_servers,
            description: deviceParam.description,
            log_directory: deviceParam.log_directory,
            board_type: deviceParam.board_type,
            communication_protocols: deviceParam.communication_protocols,
            devices: deviceParam.devices
            // TODO: should we also save api_version to the device db?
            // api_version: number
        };


        db.devices.update(
            { id: mongo.helper.toObjectID(id) },
            { $set: set },
            function (err, doc) {
                if (err) {
                    console.log("err", err);
                    deferred.reject(err.name + ': ' + err.message);
                }

                deferred.resolve();
            });
    }

    return deferred.promise;
}

function _delete(id) {
    // find the user with id 4
    deviceSchema.findOneAndRemove({ id: id }, function(err) {
        if (err) throw err;
    });
}