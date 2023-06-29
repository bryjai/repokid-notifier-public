# Repokid Notifier - Opensource Version

This repository store the opensource code used on the AWS Lambda functions _Repoed Role Notifier_ and 
_Scheduled Roles Notifier_ described on the article 
[Achieving least-privilege at Bryj (former FollowAnalytics) with Repokid, Aardvark and ConsoleMe](https://medium.com/followanalytics/granting-least-privileges-at-followanalytics-with-repokid-aardvark-and-consoleme-895d8daf604a).


It also includes the AWS Proton template used to generate those AWS Lambda Functions and all necessary
resources.

The following resources are defined on the [AWS Proton](https://docs.aws.amazon.com/proton/latest/userguide/Welcome.html) 
templates (CloudFormation):
* Repokid DynamoDB table
* Bucket storing all Code Build artifacts
* Continuous integration and continuous Delivery CloudFormation pipelines templates
* All necessary IAM policies and roles
* Two AWS Lambda functions and their triggers

Repokid is launched using its CLI inside two jenkins cronjobs, however their definition
are not described on this repository.

### Contributing

If you want to help improving this project feel free to open a Pull Request or an issue.
