# Repokid Notifier - Opensource Version

This repository store the opensource code used on the AWS Lambda functions _Repoed Role Notifier_ and _Scheduled Roles Notifier_ described in the article [Achieving least-privilege at Bryj (former FollowAnalytics) with Repokid, Aardvark and ConsoleMe](https://medium.com/followanalytics/granting-least-privileges-at-followanalytics-with-repokid-aardvark-and-consoleme-895d8daf604a).

It also includes the [AWS Proton](https://docs.aws.amazon.com/proton/latest/userguide/Welcome.html) templates (CloudFormation templates) used to generate those AWS Lambda Functions and all necessary resources.

The following resources are defined on the [AWS Proton](https://docs.aws.amazon.com/proton/latest/userguide/Welcome.html) templates (CloudFormation templates):
* Repokid DynamoDB table
* Bucket used to store all Code Build artifacts
* Continuous integration and continuous delivery CloudFormation pipelines templates
* All necessary IAM policies and roles
* Two AWS Lambda functions and their triggers

Repokid is launched using its CLI inside two Jenkins cronjobs. However, their definition is not described in this repository.

### Contributing

If you want to help improve this project, feel free to open a Pull Request or an issue.
