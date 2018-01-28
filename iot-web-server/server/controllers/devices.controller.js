﻿var config = require('config.json');
var express = require('express');
var router = express.Router();
var Device = require("../schemas/deviceSchema");
// routes
router.get('/api', getApi);
router.post('/create', createDevice);
router.get('/external', getAllDevicesForExternal);
router.get('/', getAllDevices);
router.get('/:id', getDevice);
router.put('/:id', update);
router.delete('/:id', deleteDevice);

function getAllDevices(req, res) {
    Device.find({}, function(err, devices) {
        if (err) {
            res.status(400).send(err);
        } else {
            console.log("devices", devices);
            res.status(200).send(devices);
        }
    });
}

function getAllDevicesForExternal(req, res) {
    Device.find({}, function(err, devices) {
        if (err) {
            res.status(204).send([]);
        } else {
            var deviceArr = [];
            for (var i = 0; i < devices.length; i++) {
                var deviceJSON = {};
                deviceJSON.name = devices[i].name;
                deviceJSON.description = devices[i].description;
                deviceJSON.id = devices[i].id;
                deviceArr.push(deviceJSON);
            }
            console.log("deviceArr", deviceArr);
            res.status(200).send(deviceArr);
        }
    });
}

function getDevice(req, res) {
    Device.findOne({id: req.params.id}, function(err, device) {
        if (err) {
            res.status(400).send(err);
        } else {
            res.send(device);
        }
    });
}

function createDevice(req, res) {
    var deviceParam = req.body;

    // create a new device
    var newDevice = Device({
        id: deviceParam.id,
        name: deviceParam.name,
        description: deviceParam.description,
        created_by: deviceParam.created_by,
        board_type: deviceParam.board_type
    });

    newDevice.save(function(err) {
        if (err) {
            res.status(400).json({message: "Device already exists"});
        } else {
            res.json({device: newDevice});
        }
    });
}

function update(req, res) {
    var deviceParam = req.body;
    console.log(req.params.id);
    Device.findOne({id: req.params.id}, function(err1, device){
        if(err1) {
            res.status(400).send(err1);
        }
        if (device) {
            device.name = deviceParam.name;
            device.description = deviceParam.description;
            device.board_type = deviceParam.board_type;
            device.communication_protocols = deviceParam.communication_protocols;
            device.devices = deviceParam.devices;
            device.save(function(err2, updatedDevice){
                if(err2) {
                    // console.log("err2", err2);
                    // console.log(err2.errors);
                    res.status(400).send(err2);
                }
                res.json({message: "Device updated successfully", device: updatedDevice});
            });

        } else {
            res.status(400).send({message: "Device not found"});
        }
    });
}

function deleteDevice(req, res) {
    Device.findOneAndRemove({ id: req.params.id }, function(err) {
        if (err) {
            res.status(400).send(err);
        } else {
            res.json('success');
        }
    });
}

function getApi(req, res) {
    res.write(config.api_version.toString());
    res.end();
}

module.exports = router;