# Changelog

## Version 2.*

### 2.4.0

* Removed wenet-common-model submodule
* Added wenet-common library

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