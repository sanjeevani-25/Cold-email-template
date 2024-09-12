import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from celery import Celery
# from tasks import tasks
from celery import shared_task


import logging

logger = logging.getLogger(__name__)


# Initialize Celery instance
app = Celery('email_sender', broker='redis://localhost:6379/0')

# Optional: Configure result backend
app.conf.result_backend = 'redis://localhost:6379/0'

# Optional: Task serialization and content settings
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
)

print("Celery app started")

@app.task(name='send_email_task')
def send_email_task(subject, to_email, email_content, MY_EMAIL, MY_EMAIL_APP_PASSWORD):
    logger.info("Task started")
    from_email = MY_EMAIL
    app_password = MY_EMAIL_APP_PASSWORD

    # Create a MIME object
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach HTML content to the email
    msg.attach(MIMEText(email_content, 'html'))
    logger.info("Sending email ...")

    # Send the email via SMTP
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, app_password)
            logger.info("Login successful")

            server.sendmail(from_email, to_email, msg.as_string())

            logger.info(f"Email sent to {to_email} successfully!")
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")


# <p>With hands-on experience in full-stack development and UI/UX design, I&apos;ve successfully engineered applications that combine efficiency with user-friendly interfaces. For example, during my internship at Anveshak Technology and Knowledge Solutions, I developed a Health Quiz App integrating real-time communication and automated task management, which improved processing time by 50% and throughput by 3x. Additionally, I spearheaded the UI/UX design for Zeitgeist IIT Ropar&apos;s Cultural Fest website, boosting visitor traffic by 33% through enhanced user engagement.</p>

# <p>I would love the opportunity to discuss how I can bring value to your team. Please find my resume attached for more details. Looking forward to connecting!</p>
