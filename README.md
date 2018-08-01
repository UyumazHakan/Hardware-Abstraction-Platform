# MEAN Stack with Angular 5 

[For more info](https://gitlab.lrz.de/IoT-Practicum-Group/sensors)

### Technical University of Munich - IoT Practical Course Project


### Contributors:
- Admir Jashari
- Anjali Sasihithlu
- Rakibul Alam
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
- if using pm2 - `pm2 start npm --name "ui" -- start`

#### How to Deploy Frontend Module
- `cd client`
- `npm install`
- `npm start` or `forever start -c "npm start" ./`
- navigate to `<ip_address_of_server>:3001`

#### How to Deploy Backend and Frontend using Kubernetes
See: 
 
- [Installing kubeadm](https://kubernetes.io/docs/setup/independent/install-kubeadm/) 

- [Creating a single master cluster with kubeadm](https://kubernetes.io/docs/setup/independent/create-cluster-kubeadm/)

- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#creating-a-deployment)
