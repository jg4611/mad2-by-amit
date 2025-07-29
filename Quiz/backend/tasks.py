from flask_mail import Message
from backend import create_app
from backend.celery_config import init_celery, mail_settings
from backend.models import User
from flask_mail import Mail

app = create_app()
app.config.update(mail_settings)
mail = Mail(app)
celery = init_celery(app)

@celery.task
def send_daily_quiz_reminder():
    """
    Send daily quiz reminder to all users via email
    """
    with app.app_context():
        users = User.query.all()
        for user in users:
            try:
                msg = Message(
                    subject="Daily Quiz Reminder",
                    recipients=[user.email],
                    body=f"""
                    Hello {user.username},

                    Don't forget to take your daily quiz today! Keep learning and improving.

                    Best regards,
                    Quiz Master Team
                    """
                )
                mail.send(msg)
            except Exception as e:
                print(f"Failed to send email to {user.email}: {str(e)}")
                continue

# You can add more tasks here for different notification methods (SMS, G-chat)
