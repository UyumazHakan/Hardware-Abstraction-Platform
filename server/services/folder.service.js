var fs = require('fs');
var Device = require("../schemas/deviceSchema");
var fs = require('fs');
var path = require('path');

var service = {};
service.createFoldersForDevices = createFoldersForDevices;
service.walkSync = walkSync;

module.exports = service;

function createFoldersForDevices() {
    Device.find({}, function(err, devices) {
        if (err) {
            console.log("err at createFoldersForDevices", err);
        } else {
            for (var i = 0; i < devices.length; i++) {
                var dir = './uploads/'+ devices[i].id;
                if (!fs.existsSync(dir)){
                    fs.mkdirSync(dir);
                }
            }
        }
    });
}

// https://stackoverflow.com/questions/2727167/how-do-you-get-a-list-of-the-names-of-all-files-present-in-a-directory-in-node-j
function walkSync(folderName, callback) {
    fs.readdirSync(folderName).forEach(function (file) {
        // https://stackoverflow.com/questions/7083045/fs-how-do-i-locate-a-parent-folder
        var filePath = path.join(folderName, file);
        var stat = fs.statSync(filePath);
        if (stat.isFile()) {
            callback(filePath, stat);
        } else if (stat.isDirectory()) {
            walkSync(filePath, callback);
        }
    });
}