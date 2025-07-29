# Quiz Reminder System Setup

## Prerequisites
- Redis server
- Python 3.9+
- virtualenv

## Installation

1. Install Redis (if not already installed):
   ```bash
   # macOS (using Homebrew)
   brew install redis

   # Ubuntu/Debian
   sudo apt-get install redis-server
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure Environment Variables:
   Edit the `.env` file in the backend directory and set your email credentials:
   ```
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-specific-password
   MAIL_DEFAULT_SENDER=your-email@gmail.com
   ```

   Note: For Gmail, you'll need to use an App Password instead of your regular password.
   To generate an App Password:
   1. Go to your Google Account settings
   2. Enable 2-Step Verification if not already enabled
   3. Go to Security → App passwords
   4. Generate a new app password for "Mail"

## Running the System

1. Start Redis server:
   ```bash
   redis-server
   ```

2. Start Celery worker (from the Quiz directory):
   ```bash
   celery -A backend.tasks.celery worker --loglevel=info
   ```

3. Start Celery beat for scheduled tasks:
   ```bash
   celery -A backend.tasks.celery beat --loglevel=info
   ```

4. Start the Flask application:
   ```bash
   flask run
   ```

## Configuration

The reminder system is configured to:
- Send email reminders daily
- Use Gmail SMTP server
- Run through Redis as message broker

You can modify the schedule in `celery_config.py` by adjusting the `beat_schedule` configuration.

## Troubleshooting

1. If emails are not being sent:
   - Check your email credentials in `.env`
   - Ensure you're using an App Password for Gmail
   - Check if less secure app access is enabled in your Gmail settings

2. If Celery workers are not starting:
   - Ensure Redis server is running
   - Check Redis connection URL in `.env`
   - Verify all dependencies are installed correctly
