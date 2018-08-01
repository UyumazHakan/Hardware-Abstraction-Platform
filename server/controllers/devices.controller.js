﻿var config = require('config.json');
var express = require('express');
var router = express.Router();
var Device = require("../schemas/deviceSchema");
var jwt = require('jsonwebtoken');
var fs = require('fs');
var rimraf = require('rimraf'); // to remove devices' log directories
var folderService = require('../services/folder.service');

// routes
router.get('/api', getApi);
router.post('/create', createDevice);
router.post('/upload', uploadFileToDeviceFolder);
router.post('/getFileNames', getFileNames);
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

function getFileNames(req, res) {
    if (req.body.id) {
        Device.findOne({id: req.body.id}, function(err, device) {
            if (err) {
                res.status(400).send(err);
            } else {
                console.log(device);
                var filePaths = [];
                folderService.walkSync('./uploads/' + device.id, function(filePath, stat) {
                    filePaths.push(filePath);
                });
                res.status(200).send(filePaths);
            }
        });
    } else {
        res.status(400).send("Please provide an id in body to search for its logs in server");
    }

}

function uploadFileToDeviceFolder(req, res) {
    if (!req.files)
        return res.status(400).send('No files were uploaded.');

    // The name of the input field (i.e. "file") is used to retrieve the uploaded file(s)
    var files = req.files.file;
    var id = req.body.id;

    if (files.length) {
        for (var i = 0; i < files.length; i++) {
            var file = files[i];
            var fileName = file.name;
            var destination = './uploads/' + id + '/' + fileName;
            // Use the mv() method to place files somewhere on your server
            file.mv(destination, function(err) {
                if (err) {
                    return res.status(400).send("Either id is wrong or server does not have a folder for given id");
                }
            });
        }
        return res.send('Files are uploaded successfully');
    } else {
        var file = files;
        var fileName = file.name;
        var destination = './uploads/' + id + '/' + fileName;
        // Use the mv() method to place files somewhere on your server
        file.mv(destination, function(err) {
            if (err) {
                return res.status(400).send("Either id is wrong or server does not have a folder for given id");
            } else {
                return res.send('File is uploaded successfully');
            }
        });
    }


}

function getAllDevicesForExternal(req, res) {
    Device.find({}, function(err, devices) {
        if (err) {
            res.status(204).send([]);
        } else {
            var token = req.headers.authorization.split(' ')[1] || req.headers['x-access-token'];
            if (token) {
                jwt.verify(token, config.secret, function (err, decoded) {
                    if (err) {
                        console.error('JWT Verification Error', err);
                        return res.status(403).send(err);
                    } else {
                        req.decoded = decoded;
                        var username = req.decoded.username;

                        var deviceArr = [];
                        for (var i = 0; i < devices.length; i++) {
                            if (devices[i].created_by === username) {
                                var deviceJSON = {};
                                deviceJSON.name = devices[i].name;
                                deviceJSON.description = devices[i].description;
                                deviceJSON.id = devices[i].id;
                                deviceArr.push(deviceJSON);
                            }
                        }
                        console.log("deviceArr", deviceArr);
                        res.status(200).send(deviceArr);
                    }
                });
            }
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
            var dir = './uploads/'+ newDevice.id;
            if (!fs.existsSync(dir)){
                fs.mkdirSync(dir);
            }
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
            device.log_level = deviceParam.log_level;
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
            var dirToDelete = './uploads/' + req.params.id;
            rimraf(dirToDelete, function () {
                res.json('success');
            });
        }
    });
}

function getApi(req, res) {
    res.write(config.api_version.toString());
    res.end();
}

module.exports = router;