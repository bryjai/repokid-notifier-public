from __future__ import print_function

import os
from datetime import datetime

from notifier.mail_sender import MailSender

aws_region = "eu-west-1"
ses_arn = os.environ.get("SES_ARN")
sender = "sender@email.com"


def get_user_email(new_image: dict) -> str:
    for tag in new_image["Tags"]["L"]:
        if tag["M"]["Key"]["S"] == "consoleme-authorized":
            return tag["M"]["Value"]["S"]


def lambda_handler(event: dict, context: dict) -> None:
    for record in event["Records"]:
        if record["eventName"] == "MODIFY":
            # Check for RepoScheduled field transition from non-zero to zero
            # Meaning a Repo action happened
            if (
                record["dynamodb"]["NewImage"]["RepoScheduled"]["N"] == "0"
                and record["dynamodb"]["OldImage"]["RepoScheduled"]["N"] != "0"
            ):
                mail_sender = MailSender(aws_region, ses_arn)
                to_addresses = get_user_email(record["dynamodb"]["NewImage"])
                subject = "AWS Role Policies deletion"
                body = f"""<html>
                    <head>
                    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
                    <title>Unused AWS IAM Role Cleanup</title>
                    </head>
                    <body>
                    Hi,<br>
                    The unused policies of the AWS Role <b>{record['dynamodb']['NewImage']['Arn']['S']}</b> 
                    were deleted in {str(datetime.strptime(record['dynamodb']['NewImage']['Refreshed']['S'], '%Y-%m-%dT%H:%M:%S.%f').strftime("%d %b %Y %H:%M:%S"))}.
                    <br>For more details please check <a href="<ConsoleMe URL>">ConsoleMe</a>.
                    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
                    </body>
                    </html>"""
                mail_sender.send_email(to_addresses, subject, body, sender, "UTF-8")

                print(
                    "Role has been repoed. Role: %s "
                    % str(record["dynamodb"]["NewImage"]["RoleName"]["S"])
                )
