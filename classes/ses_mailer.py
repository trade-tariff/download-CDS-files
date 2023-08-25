import boto3
import datetime
import os

from dotenv import load_dotenv
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()


class SesMailer(object):
    SUBJECT = "CDS data load {edition}"
    EMAIL_CONTENT = open("resources/email_template.html", "r").read()

    @classmethod
    def build_for_test(cls):
        return SesMailer("Testing", "<p>Hello, World</p>", ["test.csv"])

    @classmethod
    def build_for_cds_upload(cls, excel):
        produced_date = excel.file_date
        loaded_date = (
            datetime.datetime.strptime(produced_date, "%Y-%m-%d")
            + datetime.timedelta(days=1)
        ).strftime("%Y-%m-%d")
        subject = SesMailer.SUBJECT.format(edition=produced_date)
        content = SesMailer.EMAIL_CONTENT.format(
            produced_date=produced_date, loaded_date=loaded_date
        )

        return SesMailer(subject, content, [excel.excel_filename])

    def __init__(self, subject, content, attachments=[]):
        self._subject = subject
        self._attachments = attachments
        self._client = boto3.client("ses", region_name=os.getenv("AWS_REGION"))
        self._to_emails = os.getenv("TO_EMAILS", default="")
        self._from_email = os.getenv("FROM_EMAIL", default="")
        self._content = content

    def send(self):
        message = MIMEMultipart()
        message["Subject"] = self._subject
        message["From"] = self._from_email
        message["To"] = self._to_emails
        body = MIMEText(self._content, "html")
        message.attach(body)

        if self._attachments:
            for filename in self._attachments:
                attachment = self.create_attachment(filename)

                message.attach(attachment)

        return self._client.send_raw_email(
            Source=self._from_email,
            Destinations=self._to_emails.split(","),
            RawMessage={"Data": message.as_string()},
        )

    def create_attachment(self, filename):
        with open(filename, "rb") as attachment:
            part = MIMEApplication(attachment.read())
            part.add_header(
                "Content-Disposition", "attachment", filename=os.path.basename(filename)
            )

            return part
