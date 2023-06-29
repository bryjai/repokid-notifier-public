from __future__ import print_function

import os

import boto3
from typing import List
from datetime import datetime, timedelta
from notifier.mail_sender import MailSender

aws_region = "eu-west-1"
ses_arn = os.environ.get("SES_ARN")
dynamo_table = os.environ.get("DYNAMO_TABLE")
sender = "sender@email.com"
to_addresses = ["destination@email.com"]


def scan_roles(
    timestamp_from: datetime, timestamp_to: datetime, dynamodb=None
) -> List[dict]:

    role_list = []
    table = dynamodb.Table(dynamo_table)

    response = table.scan()
    scan_result = response["Items"]
    for role in scan_result:
        repo_scheduled_datetime = datetime.fromtimestamp(role["RepoScheduled"])
        if timestamp_from <= repo_scheduled_datetime < timestamp_to:
            role_list.append(role)
    return role_list


def generate_sre_email_body(
    timestamp_from: datetime, timestamp_to: datetime, roles: List[dict]
) -> str:
    html_role_list = ""
    for role in roles:
        html_role_list += "<li>" + str(role["RoleName"]) + ":"
        html_role_list += (
            "<ul>"
            + "<li>ARN: "
            + str(role["Arn"])
            + "</li>"
            + "<li>Schedule: "
            + str(
                datetime.fromtimestamp(role["RepoScheduled"]).strftime(
                    "%d %b %Y %H:%M:%S"
                )
            )
            + "</li>"
            + "</ul>"
        )
        html_role_list += "</li>"

    body = f"""<html>
            <head>
            <meta http-equiv="content-type" content="text/html; charset=UTF-8">
            <title>Scheduled Roles</title>
            </head>
            <body>
            <h3>Scheduled Roles from {str(timestamp_from.strftime("%d %b %Y %H:%M:%S"))} to 
            {str(timestamp_to.strftime("%d %b %Y %H:%M:%S"))}</h3> 
            <br>
            The list of scheduled Roles:
            <ul>{html_role_list}</ul>
            <br>For more details please check <a href="<ConsoleMe URL>">ConsoleMe</a>.
            <meta http-equiv="content-type" content="text/html; charset=UTF-8">
            </body>
            </html>"""
    return body


def generate_users_email_body(role: dict) -> str:
    body = f"""<html>
            <head>
            <meta http-equiv="content-type" content="text/html; charset=UTF-8">
            <title>Role's policy deletion</title>
            </head>
            <body>
            <h3>Role's policy deletion</h3> 
            <br>
            One or more policies of the Role <strong>{str(role['Arn'])}</strong> will be deleted on {str(datetime.fromtimestamp(role['RepoScheduled']).strftime("%d %b %Y %H:%M:%S"))}
            <br><br>For more details please check <a href="<ConsoleMe URL>">ConsoleMe</a>.
            <meta http-equiv="content-type" content="text/html; charset=UTF-8">
            </body>
            </html>"""
    return body


def get_user_email(role: dict) -> str:
    for tag in role["Tags"]:
        if tag["Key"] == "consoleme-authorized":
            return tag["Value"]
    return ""


def lambda_handler(event: dict, context: dict) -> None:
    now = datetime.now()
    one_week_from_now = now + timedelta(days=7)
    dynamodb = boto3.resource("dynamodb", aws_region)

    roles = scan_roles(now, one_week_from_now, dynamodb)

    mail_sender = MailSender(aws_region, ses_arn)
    for role in roles:
        mail_sender.send_email(
            [get_user_email(role)],
            "[Repokid] Role's policy deletion",
            generate_users_email_body(role),
            sender,
            "UTF-8",
        )

    mail_sender.send_email(
        to_addresses,
        "[Repokid] AWS Scheduled Roles " + str(now.strftime("%d %b %Y")),
        generate_sre_email_body(now, one_week_from_now, roles),
        sender,
        "UTF-8",
    )
