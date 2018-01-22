 const mongoose = require('mongoose');

const deviceSchema = new mongoose.Schema({
    ip_address: { type: String, unique: true },
    name: String,
    created_by: {
        "email": String,
        "id": String
    },
    communication_protocols: Array,

});

const Device = mongoose.model('Device', deviceSchema);
module.exports = Device;
