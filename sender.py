import os
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email import encoders

dir = 'images/'
mailbody = 'mailbody.html'
html = ''

msg = MIMEMultipart()
msg['From'] = 'Info <info@w3b.net>'
msg['To'] = 'Niels <niels@w3b.net>'
msg['Subject'] = Header('Hello dude', 'utf-8').encode()

with open(mailbody, 'r') as f:
    global html
    html = f.read()

msg.attach(MIMEText(html, 'html', 'utf-8'))

cid = 0

for image in os.listdir(dir):
    with open(dir + image, 'rb') as f:

        mime = MIMEBase('image', 'png', filename=image)
        mime.add_header('Content-Disposition', 'attachment', filename=image)
        mime.add_header('X-Attachment-Id', str(cid))
        mime.add_header('Content-ID', '<' + str(cid) + '>')
        mime.set_payload(f.read())
        encoders.encode_base64(mime)
        msg.attach(mime)
        cid += 1

print(msg)
