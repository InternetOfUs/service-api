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
- /task_transaction (POST)
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

## Versions

### 0.0.3

- Added DB an Dao for Apps
- Integrated Profile Manager and Task Manager services
- Updated WeNetUserProfile model

### 0.0.2

- Model and endpoints for App
- Model and endpoints for Message

### 0.0.1

- Model WeNetUserProfile and Task models
- Example endpoint for WeNetUserProfile and Task