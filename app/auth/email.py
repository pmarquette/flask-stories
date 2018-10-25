from flask_mail import Message
from app import mail, app
from flask import render_template
from app.models import User
from threading import Thread

def send_email(subject, sender, recipients, text_body, html_body):
  msg = Message(subject, sender=sender, recipients = recipients)
  msg.body = text_body
  msg.html = html_body
  Thread(target=email_thread, args=(app, msg)).start()

def email_thread(app, msg):
  with app.app_context():
    mail.send(msg)

def reset_password_email(user):
  token = user.get_reset_token()
  send_email('Flask Stories - Password Reset', sender='pmuhflask@gmail.com', recipients=[user.email], text_body=render_template('email/password_reset.txt', user=user, token=token), html_body=render_template('email/password_reset.html', user=user, token=token))