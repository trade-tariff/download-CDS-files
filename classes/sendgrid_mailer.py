# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
import base64
import platform
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
)
from dotenv import load_dotenv


class SendgridMailer(object):
    def __init__(self, subject, html_content, attachment_list=None):
        load_dotenv(".env")
        self.send_mail = int(os.getenv("SEND_MAIL"))
        self.SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
        if self.send_mail == 0:
            return

        self.attachment_list = attachment_list
        self.subject = subject
        self.html_content = html_content
        self.from_email = os.getenv("FROM_EMAIL")
        self.to_email_string = os.getenv("TO_EMAILS")
        self.parse_origin_email()
        self.parse_destination_emails()

    def parse_origin_email(self):
        tmp = self.from_email.split("|")
        self.from_email = (tmp[0], tmp[1])

    def send(self):
        if self.send_mail == 0:
            return

        if len(self.to_emails) > 1:
            is_multiple = True
        else:
            is_multiple = False

        message = Mail(
            from_email=self.from_email,
            to_emails=self.to_emails,
            subject=self.subject,
            html_content=self.html_content,
            is_multiple=is_multiple,
        )

        if self.attachment_list is not None:
            for attachment in self.attachment_list:
                file = self.create_attachment(attachment)
                message.add_attachment(file)

        try:
            sg = SendGridAPIClient(self.SENDGRID_API_KEY)
            sg.send(message)

        except Exception as e:
            print(e)

    def create_attachment(self, file):
        encoded_file = None
        with open(file, "rb") as f:
            data = f.read()
            f.close()

        encoded_file = base64.b64encode(data).decode()

        if platform.system() == "Windows":
            divider = "\\"
        else:
            divider = "/"
        parts = file.split(divider)
        actual_filename = parts[len(parts) - 1]
        attachment = Attachment(
            FileContent(encoded_file),
            FileName(actual_filename),
            FileType(
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ),
            Disposition("attachment"),
        )
        return attachment

    def parse_destination_emails(self):
        self.to_emails = []
        names = self.to_email_string.split(",")
        for name in names:
            item = name.split("|")
            item_tuple = (item[0], item[1] + " " + item[2])
            self.to_emails.append(item_tuple)
