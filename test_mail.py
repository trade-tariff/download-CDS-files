import ssl
from classes.sendgrid_mailer import SendgridMailer


ssl._create_default_https_context = ssl._create_unverified_context
html_content = """
    <p>Dear all,</p>
    <p>Please find attached the latest CDS updates in Excel format</p>
    <p>Thanks,</p>
    <p>The Online Tariff Team.</p>
"""
filename = "resources/xlsx/CDS updates 2021-01-01.xlsx"
subject = "CDS data load test"
attachment_list = [
    filename
]
s = SendgridMailer(subject, html_content, attachment_list)
s.send()
