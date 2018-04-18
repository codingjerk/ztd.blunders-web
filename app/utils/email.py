import httplib2
import os
import oauth2client
from oauth2client import client, tools
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery

from validate_email import validate_email

from app.utils import const

class GMailAPIValidation():
    __credentials = None

    def __init__(self):
        self.__sender = const.email_validation.sender_email
        self.__credential_path = const.email_validation.credential_path

        store = oauth2client.file.Storage(self.__credential_path)
        self.__credentials = store.get()

        if not self.__credentials or self.__credentials.invalid:
            raise Exception("Cannot load GMail API credentials")

    def __create_message(self, sender, to, subject, msg_html, msg_plain):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = to
        msg.attach(MIMEText(msg_plain, 'plain'))
        msg.attach(MIMEText(msg_html, 'html'))
        raw = base64.urlsafe_b64encode(msg.as_bytes())
        raw = raw.decode()
        body = {'raw': raw}
        return body

    def __send_internal(self, service, user_id, message):
        try:
            message = (service.users().messages().send(userId=user_id, body=message).execute())
            print('Message Id: %s' % message['id'])
            return message
        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    def __send(self, sender, to, subject, msg_html, msg_plain):
        http = self.__credentials.authorize(
            httplib2.Http()
        )

        service = discovery.build('gmail', 'v1',
            http=http
        )

        message1 = self.__create_message(sender, to, subject, msg_html, msg_plain)
        self.__send_internal(service, "me", message1)

    def send(self, user_name, user_email, validation_code):
        subject = "chessblunders.org - validating your account"
        msg_html = \
            'Dear %s,<br>' \
            'Your validation code is <b>%s</b><br>' \
            'Use this code to validate your account in the mobile client.' % (
                user_name,
                validation_code
            )

        print(msg_html)
        msg_plain = \
            'Dear %s,\n' \
            'Your validation code is %s\n' \
            'Use this code to validate your account in the mobile client.' % (
                user_name,
                validation_code
            )

        self.__send(
            sender = self.__sender,
            to = user_email,
            subject = subject,
            msg_html = msg_html,
            msg_plain = msg_plain
        )

def MXDomainValidation(email):
    status = validate_email(email, check_mx=True)

    if status is not None and status == True:
        return True

    return False
