import ssl
from classes.sendgrid_mailer import SendgridMailer
from classes.ses_mailer import SesMailer

<<<<<<< Updated upstream

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
=======
# mailer = SesMailer('Testing').send('', '')

mailer = SesMailer.build_for_test()

print(mailer._subject)
print(mailer._attachments)
print(mailer._client)
print(mailer._to_emails)
print(mailer._from_email)
print(mailer._content)
# ssl._create_default_https_context = ssl._create_unverified_context
# html_content = """
#     <p>Dear all,</p>
#     <p>Please find attached the latest CDS updates in Excel format</p>
#     <p>Thanks,</p>
#     <p>The Online Tariff Team.</p>
# """
# filename = "resources/xlsx/CDS updates 2021-01-01.xlsx"
# subject = "CDS data load test"
# attachment_list = [filename]
# s = SendgridMailer(subject, html_content, attachment_list)
# s.send()

# import ssl
# from classes.sendgrid_mailer import SendgridMailer

# print("hello")

# ssl._create_default_https_context = ssl._create_unverified_context
# html_content = """
#     <p>Dear all,</p>
#     <p>Please find attached the latest CDS updates in Excel format</p>
#     <p>Thanks,</p>
#     <p>The Online Tariff Team.</p>
# """
# filename = "resources/xlsx/CDS updates 2021-01-01.xlsx"
# subject = "CDS data load test"
# attachment_list = [filename]
# s = SendgridMailer(subject, html_content, attachment_list)
# s.send()
>>>>>>> Stashed changes
