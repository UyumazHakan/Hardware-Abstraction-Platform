const bluebird = require('bluebird');
const crypto = bluebird.promisifyAll(require('crypto'));
const nodemailer = require('nodemailer');
const passport = require('passport');
const User = require('../models/User');
const Device = require('../models/Device');

/**
 * GET /register_device
 * Device Registration Page.
 */
exports.getRegisterDevice = (req, res) => {
    res.render('device/register_device', {
        title: 'Register Device'
    });
};


/**
 * POST /register_device
 * Register the device with given information
 */
exports.postRegisterDevice = (req, res, next) => {
    req.assert('ip_address', 'IP Address is not valid').notEmpty();
    req.assert('name', 'Device name cannot be blank').notEmpty();
    // req.assert('type', 'I/O type should be selected').notEmpty();
    // req.sanitize('email').normalizeEmail({ gmail_remove_dots: false });

    const errors = req.validationErrors();

    if (errors) {
        req.flash('errors', errors);
        return;
    }

    const device = new Device({
        ip_address: req.body.ip_address,
        name: req.body.name
    });

    Device.findOne({ ip_address: req.body.ip_address }, (err, existingDevice) => {
        if (err) {
            console.log(err);
            return next(err);
        }
        if (existingDevice) {
            console.log(existingDevice);
            req.flash('errors', { msg: 'Device with that ip address already exists.' });
            return;
        }
        device.save((err) => {
            if (err) { return next(err); }
            req.flash('success', { msg: 'Device has been registered.' });
            return res.redirect('/all_devices');
        });
    });
};

/**
 * GET /all_devices
 * Retrieve All Devices' Information.
 */
exports.getAllDevices = (req, res) => {
    Device.find({}, (err, devices) => {
        console.log("Devices: ", devices);
        if (err) { return next(err); }
        res.render('device/all_devices', {
            title: 'All Devices',
            devices: devices
        });
    });
};




