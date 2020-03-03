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

## Migration

### Execute the existing migrations

1. Create migration script for your db

    ```bash
    migrate manage manage.py --repository=migrations --url=<db_connection_url>
    ```
    - if you want to use a local sqlite3 db:
    ```bash
    migrate manage manage.py --repository=migrations --url=sqlite:///db/_service_api.db
    ```
   
2. Initialize the database with the version control system

    ```bash
    python manage.py version_control
    ```
   
3. execute all the migration

    ```bash
    python manage.py upgrade
    ```

## Deploy

A docker-compose file for deploy this service is available in the [wenet-service-api-deployment](https://bitbucket.org/wenet/wenet-service-api-deployment/src/master/) repository.

## Configuration

### Environmental variables:

- DB_CONNECTION_STRING: connection string for database, for example `sqlite:///db/service_api.db`
- APIKEY: apikey for used fo authenticate the requests
- PROFILE_MANAGER_CONNECTOR_BASE_URL: base url for the profile manager connection
- TASK_MANAGER_CONNECTOR_BASE_URL: base url for the task manager endpoints

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