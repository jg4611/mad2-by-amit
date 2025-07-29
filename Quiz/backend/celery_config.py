from celery import Celery
from flask import Flask
from flask_mail import Mail

def init_celery(app: Flask):
    celery = Celery(
        app.import_name,
        broker='redis://localhost:6379/0',
        backend='redis://localhost:6379/0'
    )
    celery.conf.update(
        enable_utc=True,
        timezone='UTC',
        beat_schedule={
            'send-daily-quiz-reminder': {
                'task': 'backend.tasks.send_daily_quiz_reminder',
                'schedule': 3600.0,  # Run every hour (adjust as needed)
            },
        }
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

# Mail configuration
mail_settings = {
    'MAIL_SERVER': 'smtp.gmail.com',
    'MAIL_PORT': 587,
    'MAIL_USE_TLS': True,
    'MAIL_USE_SSL': False,
    'MAIL_USERNAME': '',  # Set this in .env
    'MAIL_PASSWORD': '',  # Set this in .env
    'MAIL_DEFAULT_SENDER': ''  # Set this in .env
}
