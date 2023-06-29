from typing import List

import boto3


class MailSender:
    def __init__(self, region, ses_arn):
        self.client = boto3.client("ses", region_name=region)
        self.ses_arn = ses_arn

    def send_email(
        self,
        to_addresses: List[str],
        subject: str,
        body: str,
        sender: str,
        charset: str = "UTF-8",
    ) -> None:
        # Handle non-list recipients
        if not isinstance(to_addresses, list):
            to_addresses = [to_addresses]
        try:
            response = self.client.send_email(
                Destination={"ToAddresses": to_addresses},  # This should be a list
                Message={
                    "Body": {
                        "Html": {"Charset": charset, "Data": body},
                        "Text": {"Charset": charset, "Data": body},
                    },
                    "Subject": {"Charset": charset, "Data": subject},
                },
                Source=sender,
                SourceArn=self.ses_arn,
            )
        # Display an error if something goes wrong.
        except Exception as err:
            print("ERROR: %s" % str(err))
        else:
            print("Email sent successfully to %s" % str(",".join(to_addresses)))
