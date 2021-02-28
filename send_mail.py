import smtplib
import random
import datetime
import html
import mimetypes
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path
import os

SENDER_MAIL = os.environ['SENDER_MAIL']
SENDER_PASS = os.environ['SENDER_PASS']
SENDER_SMTP = "smtp.gmail.com"
PORT = 587
NUMBER_OF_SAVED_LETTERS = 3


def send_mail(recipent, message, composer_name, composer_mail):
    title = "Roommate Alert"
    path = Path('static/images/logo-old.png')

    msg = EmailMessage()
    msg['Subject'] = f"{composer_name} Wants to Get In Touch"
    msg['From'] = SENDER_MAIL
    msg['To'] = [recipent]
    msg.set_content('[image: {title}]'.format(title=title))  # text/plain
    cid = make_msgid()[1:-1]  # strip <>
    msg.add_alternative(  # text/html
        f'<h4>{message}<br>From:<br>{composer_name}<h4><br><h5>Feel Free to contact them back at<h5><br><h6>{composer_mail}</h6><br><em>Happy House Hunting<br>From Your Friends @PropertyGarden<em><img src="cid:{cid}"/>'
            .format(cid=cid, alt=html.escape(title, quote=True)),
        subtype='html')
    maintype, subtype = mimetypes.guess_type(str(path))[0].split('/', 1)
    msg.get_payload()[1].add_related(  # image/png
        path.read_bytes(), maintype, subtype, cid="<{cid}>".format(cid=cid))

    connection = smtplib.SMTP(SENDER_SMTP, PORT)
    connection.starttls()
    connection.login(user=SENDER_MAIL, password=SENDER_PASS)
    connection.sendmail(from_addr=SENDER_MAIL, to_addrs=recipent, msg=msg.as_string())
    print("sent")
    connection.close()


