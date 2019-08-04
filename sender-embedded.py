import os
import sys
import base64
import smtplib
import dns.resolver
import mimetypes
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email import encoders
sender = "Info <info@patternsfestival.com>"
mailing = open("./list1", "r")
for receiver in mailing:
    receiver = receiver.replace("\n", "")
    if receiver[0] == "#":
        continue
    else:
        dir = './images/'
        imageList = []
        for filename in os.listdir(dir):
            with open(dir + filename, "rb") as f:
                imageList.append((filename, base64.b64encode(f.read())))
        mailbody = './mailbody.html'
        html = ''
        with open(mailbody, 'r') as f:
            html = f.read()
        for image, b64 in imageList:
            mimeType = mimetypes.guess_type(dir + image,
                strict=True)[0].replace('image/', '')
            html = html.replace('<img src="images/' + image,
                '<img src="data:image/' + mimeType + ';base64,' + b64)
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = Header('Patterns Festival', 'utf-8').encode()
        msg.attach(MIMEText(html, 'html', 'utf-8'))

        with open('/tmp/email', 'w') as f:
            f.write(str(msg))
            f.close()
        os.system('cat /tmp/email | tail + 2 | sendmail -t')
        print(receiver)
