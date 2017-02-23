# S3 Artifact Resource

[![Build Status](https://travis-ci.org/cosee-concourse/serverless-resource.svg?branch=master)](https://travis-ci.org/cosee-concourse/serverless-resource) [![Docker Repository on Quay](https://quay.io/repository/cosee-concourse/serverless-resource/status "Docker Repository on Quay")](https://quay.io/repository/cosee-concourse/serverless-resource)

Deploys updates and removes [Serverless](http://serverless.io) Stacks on AWS Lambda.

## Source Configuration

* `apiKey`: *Required.* The AWS access key to use when accessing the
  bucket.

* `secretKey`: *Required.* The AWS secret key to use when accessing
  the bucket.

* `regionName`: *Optional.* The region to deploy to. Defaults to eu-west-1

## Behavior

### `check`:

Checks if source configuration is done correct. Will check if AWS credentials are correct.

### `in`: 

* Saves a file with the name `stage` in the directory containing the name of the deployed stage. Calling `in` before calling `out` in the same pipeline can cause unexpected behavior.

#### Parameters

*None.*

### `out`: Upload artifacts as archive to the bucket.

_stage_ is available as environment variable _STAGE_. Use it as `($env:STAGE)` inside serverless.yml
Given a folder specified by `folderpath` (this must be available to the resource - for example created by a task that is run before the
put request), compresses folder contents and uploads compressed archive to the S3 bucket.
Reads semantic version created by the `semver` resource specified as filepath `version` to generate the versioned name.


#### Parameters
 
* `serverlessFile`: *Optional.* Filename or Path of serverless.yml
 
* `stageFile`: Path to folder that contains artifacts

* `stage`: Path to folder that contains artifacts

* `deploy`: If set to `true` deploys the stack.

* `remove`: If set to `true` removes the stack.

Either `stagefile` or `stage` has to be set.
Also either `deploy` or `remove` has to be set to true.

### Example Configuration