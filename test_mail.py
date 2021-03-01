import sys
from classes.sendgrid_mailer import SendgridMailer

html_content = """
        <p>Dear all,</p>
        <p>Please find attached the latest CDS updates in Excel format</p>
        <p>Thanks,</p>
        <p>The Online Tariff Team.</p>"""
filename = "test.xlsx"
subject = "CDS data load - 21-03-01g"

s = SendgridMailer(subject, html_content, filename)
s.send()
