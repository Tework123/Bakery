import time
from threading import Thread

from flask import current_app, render_template
from flask_mail import Message

from application import mail, celery
# from application.auth.auth import create_token
from start_app import CONFIG


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


# попробовать все операции гит не от root, а то он блокирует все

# this func must get whole request about email
def send_email(subject, sender, recipients, body, attachments=None):
    msg = Message(subject, sender=sender, recipients=recipients, body=body)

    # if attachments is not None:
    #     attach_photo = attachments.split('/')[-1]
    #     with current_app.open_resource(attachments) as fp:
    #         msg.attach(attach_photo, 'image/png', fp.read())

    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


def send_email_authentication(email, code, token='token'):
    body = render_template('email/login.html', token=token, email=email, code=code)
    send_email('email_authentication', CONFIG.MAIL_USERNAME, [email], body)


def send_email_register(email, token):
    body = render_template('email/register.html', token=token, email=email)
    send_email('email_register', CONFIG.MAIL_USERNAME, [email], body)


@celery.task
def celery_task():
    time.sleep(5)
    print(111111111111)
    email = 'potsanovik@mail.ru'
    msg = Message('email_register', sender=CONFIG.MAIL_USERNAME, recipients=[email], body='123')
    mail.send(msg)
