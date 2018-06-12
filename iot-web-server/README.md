# MEAN Stack Web Application 

### Technical University of Munich - [IoT Practical Course](http://www.caps.in.tum.de/en/teaching/ss18/practical-courses/internet-of-things-iot/) Project


### Contributors:
- Ali Naci Uysal
- Hakan Uyumaz
- Erkin Kırdan
- Mikayil Murad

[Original project readme](http://jasonwatmore.com/post/2017/02/22/mean-with-angular-2-user-registration-and-login-example-tutorial)


## Deployment
Tested with 
- `Ubuntu 16.04.3 LTS`,
- `MongoDB v3.2.18`,
- `npm v3.5.2`
    
#### How to Deploy MongoDB
See [MongoDB installation instructions](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)

#### How to Deploy Backend Module
- `cd server`
- `npm install`
- `node server.js` or `forever start server.js` to run in the background. See [forever package](https://www.npmjs.com/package/forever)

#### How to Deploy Frontend Module
- `cd client`
- `npm install`
- `npm start` or `forever start -c "npm start" ./`
- navigate to `<ip_address_of_server>:3001`

