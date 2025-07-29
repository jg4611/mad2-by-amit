from flask_mail import Mail, Message
from models import User
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
mail_settings = {
    'MAIL_SERVER': 'smtp.gmail.com',
    'MAIL_PORT': 587,
    'MAIL_USE_TLS': True,
    'MAIL_USERNAME': os.getenv('MAIL_USERNAME'),
    'MAIL_PASSWORD': os.getenv('MAIL_PASSWORD'),
    'MAIL_DEFAULT_SENDER': os.getenv('MAIL_DEFAULT_SENDER')
}

mail = None

def init_mail(app):
    global mail
    app.config.update(mail_settings)
    mail = Mail(app)

def send_registration_confirmation(user):
    """Send a confirmation email to newly registered user"""
    if not mail:
        print("Mail not initialized")
        return
        
    try:
        msg = Message(
            subject="Welcome to Quiz Master!",
            recipients=[user.email],
            body=f"""
            Hello {user.full_name},

            Welcome to Quiz Master! Your account has been successfully created.

            You can now:
            - Take quizzes
            - Track your progress
            - Learn new topics

            Start your learning journey today!

            Best regards,
            Quiz Master Team
            """
        )
        mail.send(msg)
        print(f"Registration confirmation email sent to {user.email}")
    except Exception as e:
        print(f"Failed to send registration email: {str(e)}")

def send_new_quiz_notification(quiz_title, quiz_subject):
    """Send notification to all non-admin users about a new quiz"""
    if not mail:
        print("Mail not initialized")
        return
        
    try:
        users = User.query.filter(User.role != 'admin').all()
        
        for user in users:
            msg = Message(
                subject=f"New Quiz Available: {quiz_title}",
                recipients=[user.email],
                body=f"""
                Hello {user.full_name},

                A new quiz has been added to Quiz Master!

                Quiz Details:
                - Title: {quiz_title}
                - Subject: {quiz_subject}

                Login to your account to take the quiz and test your knowledge!

                Best regards,
                Quiz Master Team
                """
            )
            mail.send(msg)
        print(f"New quiz notification sent to {len(users)} users")
    except Exception as e:
        print(f"Failed to send new quiz notification: {str(e)}")
