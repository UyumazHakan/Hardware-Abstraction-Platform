﻿﻿require('rootpath')();
var express = require('express');
var fileUpload = require('express-fileupload');
var app = express();
var cors = require('cors');
var bodyParser = require('body-parser');
var expressJwt = require('express-jwt');
var config = require('config.json');
var mongoose = require('mongoose');
var fs = require('fs');
mongoose.connect(config.connectionString);

app.use(cors());
app.use(bodyParser.json());

// default options
app.use(fileUpload());

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
}).unless({ path: ['/users/authenticate', '/users/register', '/devices/api']}));

// routes
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

    console.log('Server listening on port ' + port);
});