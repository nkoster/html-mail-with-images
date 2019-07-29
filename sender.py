import os
import mimetypes
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email import encoders
mailing = open("./list1", "r")
for receiver in mailing:
    receiver = receiver.replace("\n", "")
    if receiver[0] == "#":
        continue
    else:
        dir = './images/'
        imageList = []
        cid = 0
        for filename in os.listdir(dir):
            imageList.append((filename, cid))
            cid += 1
        mailbody = './mailbody.html'
        html = ''
        with open(mailbody, 'r') as f:
            global html
            html = f.read()
        for image, cid in imageList:
            html = html.replace('images/' + image, 'cid:' + str(cid))
        msg = MIMEMultipart()
        msg['From'] = 'Info <info@patternsfestival.nl>'
        msg['To'] = receiver
        msg['Subject'] = Header('Patterns Festival', 'utf-8').encode()
        msg.attach(MIMEText(html, 'html', 'utf-8'))
        cid = 0
        for image in os.listdir(dir):
            with open(dir + image, 'rb') as f:
                mimeType = mimetypes.guess_type(dir + image,
                    strict=True)[0].replace('image/', '')
                mime = MIMEBase('image', mimeType, filename=image)
                mime.add_header('Content-Disposition', 'attachment', filename=image)
                mime.add_header('X-Attachment-Id', str(cid))
                mime.add_header('Content-ID', '<' + str(cid) + '>')
                mime.set_payload(f.read())
                encoders.encode_base64(mime)
                msg.attach(mime)
                cid += 1
            f.close()
        print(msg)
