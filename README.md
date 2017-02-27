# Serverless Resource

[![Build Status](https://travis-ci.org/cosee-concourse/serverless-resource.svg?branch=master)](https://travis-ci.org/cosee-concourse/serverless-resource) [![Docker Repository on Quay](https://quay.io/repository/cosee-concourse/serverless-resource/status "Docker Repository on Quay")](https://quay.io/repository/cosee-concourse/serverless-resource)

Deploys updates and removes [Serverless](http://serverless.io) Stacks on AWS Cloudformation.

## Source Configuration

* `access_key_id`: *Required.* The AWS access key to use when accessing the
  bucket.

* `secret_access_key`: *Required.* The AWS secret key to use when accessing
  the bucket.

* `region_name`: *Optional.* The region to deploy to. Defaults to eu-west-1

## Behavior

### `check`: Checks configuration

Checks for correct source configuration and AWS credentials.

### `in`: Saves stage as file

* Saves a file with the name `stage` in the directory containing the name of the deployed stage. Calling `in` before calling `out` in the same pipeline can cause unexpected behavior.

#### Parameters

*None.*

### `out`: Deploys or removes Serverless stack.

_stage_ is available as environment variable _STAGE_. Use it as `($env:STAGE)` inside serverless.yml
Uses `serverless_file` and artifacts in `artifact_folder` to deploy stack.

#### Parameters
 
* `serverless_file`: Folder path that contains serverless.yml. 

* `artifact_folder`: Path to artifacts that are used in the serverless.yml. 
Make sure the artifact references in the serverless.yml is in this folder.
 
* `stage_file`: Path to a file that contains the stage name of the stack

* `stage`: Stage name for the stack

* `deploy`: If set to `true` deploys the stack.

* `remove`: If set to `true` removes the stack.

Either `stagefile` or `stage` has to be set.
Also either `deploy` or `remove` has to be set to true.


## Example Configuration

### Resource Type
``` yaml
- name: serverless
  type: docker-image
  source:
    repository: quay.io/cosee-concourse/serverless-resource
```
### Resource

``` yaml
- name: deploy
  type: serverless
  source:
    access_key_id: ACCESS-KEY
    secret_access_key: SECRET
    region_name: eu-west-1
```

### Plan

``` yaml
- get: deploy
```

#### Deploy with fixed stage name

``` yaml
- put: deploy
  params:
    deploy: true
    stage: release
    artifact_folder: artifacts/
    serverless_file: source/ci
```

#### Deploy with stage name from file

``` yaml
- put: deploy
  params:
    deploy: true
    stage_file: naming/name
    artifact_folder: artifacts/
    serverless_file: source/ci
```
#### Remove with fixed stage name

``` yaml
- put: deploy
  params:
    remove: true
    stage: release
    serverless_file: source/ci
```

#### Remove with stage name from file

``` yaml
- put: deploy
  params:
    remove: true
    stage_file: naming/name
    serverless_file: source/ci
```
