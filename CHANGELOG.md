# Changelog

## Version 5.*

### 5.0.0

:house: Internal

* Updated project template to version 4.10.4
* Updated to wenet-common version 5.0.0-alpha

## Version 4.*

### 4.0.0

:boom: Breaking changes

* Updated the user profile and logging endpoints in order to use the updated scope list

:nail_care: Polish

* Better exception handling in the communication with the platform components

:house: Internal

* Updated to wenet-common version 4.0.0
* Updated to project template version 4.9.1 and enabled linter and ci release stage

## Version 3.*

### 3.0.3

:house: Internal 

* Updated project template to version 4.6.2
* Updated gunicorn configuration in order to allow a timout of 60 seconds for the workers

### 3.0.2

* Added the `SENTRY_SAMPLE_RATE` env variable in order to control the number of transaction stored in centry

### 3.0.1

* Updated common models to version `3.1.0` in order to fix the endpoint for the creation of a user

### 3.0.0

* Removed wenet-common-model submodule
* Added wenet-common library
* Update the query params of task list endpoint:
  * The deadlineFrom and deadlineTo parameters no longer exists
  * The startFrom and startFrom will be renamed in creationFrom and creationTo
  * The endFrom and endTo parameter will be renamed in closeFrom and closeTo
  * The updateFrom and updateTo parameter are missing
  * The order parameter is missing
* Updated the service api endpoint for updating the user profile in order to return the updated profile
* Added endpoints for supporting the update of the extended user profile

## Version 2.*

### 2.3.1

* Enabled flask sentry integration

### 2.3.0

* Added sentry integration

### 2.2.0

* Updated WeNetCommonModels to version 1.1.0

### 2.1.0

* Updated to the latest version of the wenet common models

### 2.0.0

* Added Oauth2 support
* Removed old application authentication
* Updated WeNetCommonModel to version 1.0.1
* Added support for logging component
* Detached hub database

## Version 1.*

### 1.0.0

* new endpoints for allowing 

    * managing user information (accounts, metadata, identity)
    * profile management (empty profile and CRUD operations)
    * creating a new task
    * collecting task transactions
    
* integration with task and profile manager
* setup authentication mechanism differentiated between applications and components
* using mysql database

## Version 0.*

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
