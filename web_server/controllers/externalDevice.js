const passport = require('passport');
const Device = require('../models/Device');
const User = require('../models/User');
const jwt = require('jsonwebtoken');

/**
 * GET external/all_devices
 * Retrieve All Devices' Information.
 */
exports.getAllDevices = (req, res) => {
    Device.find({}, (err, devices) => {
        if (err) {
            return res.status(400).json({
                message: err
            });
        }
        return res.status(200).json({
            devices: devices
        });
    });
};

/**
 * GET external/all_devices/:device_id
 * Retrieve given device Information.
 */
exports.getDevice = (req, res) => {
    var _id = req.params.device_id;
    console.log(_id);

    Device.findById({_id}, (err, device) => {
        if (err) {
            return res.status(400).json({
                success: false,
                message: "Provided id does not exist"
            });
        }
        return res.status(200).json({
            device: device
        })
    });
};

/**
 * POST external/auth
 * Retrieve the JWT token if provided email and password is valid.
 */
exports.postAuth = (req, res) => {
    req.assert('email', 'Email is not valid').isEmail();
    req.assert('email', 'Email cannot be blank').notEmpty();
    req.assert('password', 'Password cannot be blank').notEmpty();

    const errors = req.validationErrors();

    if (errors) {
        return res.status(400).json({
            success: false,
            message: errors
        });
    }
    const email = req.body.email;
    const password = req.body.password;

    User.findOne({ email: email.toLowerCase() }, (err, user) => {
        if (err) {
            return res.status(400).json({
                success: false,
                message: err
            });
        }
        if (!user) {
            return res.status(400).json({
                success: false,
                message: "User e-mail is not found."
            });
        }

        user.comparePassword(password, (err, isMatch) => {
            if (err) {
                return res.status(400).json({
                    success: false,
                    message: err
                });
            }
            if (isMatch) {
                // create a token with user payload
                const payload = {
                    user: user
                };
                var token = jwt.sign(payload, 'super_secret_key_for_web_server', {
                    expiresIn: "1h" // expires in 1 hour
                });
                return res.status(200).json({
                    success: true,
                    token: token
                });
            }
            return res.status(400).json({
                success: false,
                message: "Invalid email or password"
            });
        });
    })
};