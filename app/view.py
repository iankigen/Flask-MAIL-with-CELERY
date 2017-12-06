from app import app
from celery import Celery
from flask import request, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

mail = Mail(app=app)
sender = 'Admin'

recepients = []

s = URLSafeTimedSerializer(app.config['SECRET_KEY'])


def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return 'Confirm Email <br/><br/><br/>' \
               '<form action="/" method="post">' \
               '<input name="email" placeholder="email address">' \
               '<input type="submit" value="submit">' \
               '</form>'
    elif request.method == "POST":
        email = request.form['email'] or 'default value'
        token = s.dumps(email, salt='email-confirm')
        recepients.append(email)
        _link = url_for('confirm_email', token=token, _external=True)

        email_notification.delay('Confirm email', recepients, _link)

        return " Email sent to : {} <br/>".format(email)


@celery.task()
def email_notification(subject, recipients, _link):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = "Confirm Email: {}".format(_link)
    with app.app_context():
        mail.send(msg)
    return "\n\nEmail sent successfully\n\n"


@app.route('/confirm-email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=60 * 60 * 24)  # 24hrs
        return "Email confirmed. {} can now login".format(email)
    except Exception as e:
        return 'Invalid or Expired token!! Confirm Email <br/><br/><br/>' \
               '<form action="/" method="post">' \
               '<input name="email" placeholder="email address">' \
               '<input type="submit" value="submit">' \
               '</form>'
