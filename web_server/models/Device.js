 const mongoose = require('mongoose');

const deviceSchema = new mongoose.Schema({
    ip_address: { type: String, unique: true },
    name: String,
});

const Device = mongoose.model('Device', deviceSchema);
module.exports = Device;
