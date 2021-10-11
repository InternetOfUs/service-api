# WeNet -  Service APIs

## Introduction

The Service APIs component is the one responsible for allowing WeNet applications to integrate with the WeNet platform.

It exposes dedicated endpoints allowing to manage:

* applications;
* users;
* user profiles;
* logging;
* tasks (and associated transactions).

The APIs defined in this component are meant to be used by:

* other components of the WeNet platform;
* WeNet applications.


## Setup and configuration

### Installation

The service APIs required Python version 3.5 or higher.

All required Python packages can be installed using the command

```bash
pip install -r requirements.txt
```


### Requirements

The service APIs require a MySQL database to manage their contents.
The structures and migration of the database are included in the repository dedicated to the WeNet HUB: the two components are sharing the same database.


### Docker support

A dedicated Docker image for this component can be build by taking advantage of the repository Docker support.
The command:

```bash
./build_docker_image.sh
```

will:

* run the tests on the checked-out version of the service APIs;
* build the docker image for the service APIs (the naming is the following `registry.u-hopper.com/`)

## Usage

In order to run the component, simply run 

```bash
pyhton3 -m wenet_service_api.api.main
```

### Required env variables

The following environmental variables are required for the component to run properly.

- `APIKEY`: apikey required for authenticating the incoming requests
- `COMP_AUTH_KEY`: apikey required in order to authenticate on kong, this is required in order to forward the requests to the internal components
- `COMP_AUTH_KEY_HEADER`: the header name used in combination with `COMP_AUTH_KEY`, the default value is `x-wenet-component-apikey`
- `PLATFORM_BASE_URL`: base url for the wenet platform (ex. `https://wenet.u-hopper.com/dev`)
- `DEBUG`: if set put the ws in "DEBUG" mode, the debug mode consist in:
    - use dummy endpoint for profile and task manager instead of the production one
- `SENTRY_DSN`: The data source name for sentry, if not set the project will not create any event
- `SENTRY_RELEASE`: If set, sentry will associate the events to the given release
- `SENTRY_ENVIRONMENT`: If set, sentry will associate the events to the given environment (ex. `production`, `staging`)


## Documentation

The APIs documentation is available [here](http://swagger.u-hopper.com/?url=https://bitbucket.org/wenet/wenet-components-documentation/raw/master/sources/wenet-service_api-openapi.yaml#/).


## Instances

The staging instance of the Service APIs is available:
* [https://wenet.u-hopper.com/dev/service](https://wenet.u-hopper.com/dev/service) for Apikey authentication;
* [https://wenet.u-hopper.com/dev/api/service](https://wenet.u-hopper.com/dev/api/service) for Oauth2 authentication.

The production instance of the Service APIs is available:
* [https://internetofus.u-hopper.com/prod/service](https://internetofus.u-hopper.com/prod/service) for Apikey authentication;
* [https://internetofus.u-hopper.com/prod/api/service](https://internetofus.u-hopper.com/prod/api/service) for Oauth2 authentication.

## CI/CD

This project includes the support for Gitlab CI pipelines.

In order to take advantage of the CI integration, the following CI/CD variables should be setup in the repository configuration.

* `DEPLOYMENT_SERVER_IP` - the ip of the server hosting the deployment instances
* `DEPLOYMENT_TEST_DIR` - the directly with the docker configuration of the test instance
* `GITLAB_SSH_KEY` - the ssh key allowing the connection to the server
* `REGISTRY_USERNAME` - the username used for authorizing with the registry
* `REGISTRY_PASSWORD` - the password used for authorizing with the registry


## Maintainers

- Carlo Caprini (carlo.caprini@u-hopper.com)
- Stefano Tavonatti (stefano.tavonatti@u-hopper.com)
