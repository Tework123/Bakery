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


# this func must get whole request about email
def send_email(subject, sender, recipients, body, attachments=None):
    msg = Message(subject, sender=sender, recipients=recipients, body=body)

    # if attachments is not None:
    #     attach_photo = attachments.split('/')[-1]
    #     with current_app.open_resource(attachments) as fp:
    #         msg.attach(attach_photo, 'image/png', fp.read())

    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


def send_email_authentication(email, code):
    body = render_template('email/login.html', email=email, code=code)
    send_email('email_authentication', CONFIG.MAIL_USERNAME, [email], body)


@celery.task
def celery_task_send_email_authentication(email, code):
    # time.sleep(7)
    body = render_template('email/login.html', email=email, code=code)
    msg = Message('email_authentication', sender=CONFIG.MAIL_USERNAME, recipients=[email], body=body)
    mail.send(msg)
