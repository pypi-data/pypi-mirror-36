AWS PyPackager
===============
Provides a quick command line utility for packaging and uploading Python
AWS Lambda Functions.

### Motivation
For those familiar with lambda-uploader, you will notice it works very similarly and
even uses the underlying code to package Python lambda solutions. Lambda Uploader
was written when I was still new to packaging and using AWS Lambda for Python.
Once I started building larger projects and services the lambda-uploader didn't fit
into the workflow for anything other than packaging.

The AWS PyPackager is the next iteration of my personal workflow and is meant to be
really focus on packaging Python Lambda functions. Letting other tools and other frameworks
handle the deployment strategy etc.

### Commands
#### Package
Packages a Python based lambda function by building a Virtualenv and installing
all necessary dependencies.

```shell
pypackager package <python_package>
```
#### Upload
Packages and uploads a Python lambda artifact to an S3 bucket. Essentially
the package command + ```aws s3 cp```. :)

```shell
pypackager upload --bucket-name my-project-bucket <python_package>
```
