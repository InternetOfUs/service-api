# WENET SERVICE API


## Server

The dummy service is available at [https://wenet.u-hopper.com](https://wenet.u-hopper.com)

## Maintainers

- Carlo Caprini (carlo.caprini@u-hopper.com)
- Stefano Tavonatti (stefano.tavonatti@u-hopper.com)

## Build with docker

A build script is available in the `docker-support` folder, simply type:

```bash
./docker-support/build.sh
```

## Completed endpoints

- /user/profile/<profile_id> (GET, PUT, POST)
- /task/<task_id> (GET, PUT)
- /task (POST)
- /task/transaction (POST)
- /app/<app-id> (GET)

## Deploy

A docker-compose file for deploy this service is available in the [wenet-service-api-deployment](https://bitbucket.org/wenet/wenet-service-api-deployment/src/master/) repository.

## Configuration

### Environmental variables:

- DB_CONNECTION_STRING: connection string for database, for example `mysql+pymysql://user:pwd@host:port/db`
- APIKEY: apikey for used fo authenticate the requests
- PROFILE_MANAGER_CONNECTOR_BASE_URL: base url for the profile manager connection
- TASK_MANAGER_CONNECTOR_BASE_URL: base url for the task manager endpoints
- DEBUG: if set put the ws in "DEBUG" mode, the debug mode consist in:
    - use dummy endpoint for profile and task manager instead of the production one
    
    
## Gitlab CI/CD
This project includes the support for Gitlab CI pipelines.
In order to take advantage of the CI integration, the following CI/CD variables should be setup in the repository configuration.
* DEPLOYMENT_SERVER_IP - the ip of the server hosting the deployment instances
* DEPLOYMENT_TEST_DIR - the directly with the docker configuration of the test instance
* GITLAB_SSH_KEY - the ssh key allowing the connection to the server
* REGISTRY_USERNAME - the username used for authorizing with the registry
* REGISTRY_PASSWORD - the password used for authorizing with the registry