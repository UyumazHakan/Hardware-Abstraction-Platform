﻿require('rootpath')();
var express = require('express');
var fileUpload = require('express-fileupload');
var app = express();
var cors = require('cors');
var bodyParser = require('body-parser');
var expressJwt = require('express-jwt');
var config = require('config.json');
var mongoose = require('mongoose');
var fs = require('fs');
var folderService = require('./services/folder.service');
var serveIndex = require('serve-index');
var pathToRegexp = require('path-to-regexp');
var serveStatic = require('serve-static');
var contentDisposition = require('content-disposition');
var path = require('path');

mongoose.connect(config.connectionString);

app.use(cors());
app.use(bodyParser.json());

// default options for file-upload
app.use(fileUpload());

// Use unprotected APIs
const unprotected = [
    pathToRegexp('/users/authenticate'),
    pathToRegexp('/users/register'),
    pathToRegexp('/devices/api'),
    pathToRegexp('/uploads'),
    pathToRegexp('/uploads/:file_name'),
    pathToRegexp('/uploads/:id/:file_name'),
    pathToRegexp('/favicon.ico')
];

// use JWT auth to secure the api, the token can be passed in the authorization header or querystring
app.use(expressJwt({
    secret: config.secret,
    getToken: function (req) {
        if (req.headers.authorization && req.headers.authorization.split(' ')[0] === 'Bearer') {
            return req.headers.authorization.split(' ')[1];
        } else if (req.query && req.query.token) {
            return req.query.token;
        }
        return null;
    }
}).unless({ path: unprotected }));


// Set header to force download
function setHeaders (res, path) {
    res.setHeader('Content-Disposition', contentDisposition(path))
}
const dirToServe = process.cwd();

// routes
app.use('/uploads', serveIndex('uploads', {'icons': true})); // shows you the file list
app.use('/', serveStatic(dirToServe, {setHeaders: setHeaders})); // https://stackoverflow.com/questions/38208658/node-js-file-server-with-file-index
app.use('/users', require('./controllers/users.controller'));
app.use('/devices', require('./controllers/devices.controller'));


// error handler
app.use(function (err, req, res, next) {
    if (err.name === 'UnauthorizedError') {
        res.status(401).send('Invalid Token');
    } else {
        throw err;
    }
});

// start server
var port = process.env.NODE_ENV === 'production' ? 80 : 4000;
var server = app.listen(port, function () {

    // also create an uploads folder upon server start
    var dir = './uploads';
    if (!fs.existsSync(dir)){
        fs.mkdirSync(dir);
    }

    // also create folders for previously existing devices in DB
    folderService.createFoldersForDevices();

    console.log('Server listening on port ' + port);
});