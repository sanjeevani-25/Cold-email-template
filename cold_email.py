# ? TODO:
# ? 1. Load the email template from a file
# ? 2. Load the data from an Excel file
# ? 3. Send an email to each recipient with the template
# ? 4. Use celery to send emails concurrently
# ? 5. Add a delay between sending emails
# ? 6. Add logging to track the progress
# ? 7. Add error handling to catch exceptions


import pandas as pd
# Importing the Celery task for sending emails
from celery_app import send_email_task
# Importing the function to generate dynamic content for emails
from backend import genai_generate_content
from celery.result import AsyncResult
import os
from dotenv import load_dotenv  # To load environment variables from a .env file

# Load environment variables from the .env file
load_dotenv()

# Sender email details, loaded from environment variables for security
MY_EMAIL = os.getenv("SENDER_EMAIL")
MY_EMAIL_APP_PASSWORD = os.getenv("SENDER_EMAIL_APP_PASSWORD")
MY_NAME = os.getenv("SENDER_NAME")

# File paths and default values
EMAIL_TEMPLATE_PATH = './email_template.html'  # Path to the email template file
# Path to the Excel file containing email data
EXCEL_DATA_PATH = './email_companies_data.xlsx'
# Default skillset to be used if not provided in Excel
MY_DEFAULT_SKILLS = os.getenv("DEFAULT_SKILLS")


def load_template(template_path, context):
    """
    Load the email template from a file and replace placeholders with actual content.

    Args:
        template_path (str): The path to the HTML email template.
        context (dict): A dictionary containing the variables to replace in the template.

    Returns:
        str: The formatted email content.
    """
    with open(template_path, 'r') as template_file:
        template = template_file.read()
        return template.format(**context)


def load_data(excel_path):
    """
    Load email-related data from an Excel file.

    Args:
        excel_path (str): The path to the Excel file containing data.

    Returns:
        DataFrame: Pandas DataFrame containing the email data.
    """
    return pd.read_excel(excel_path)


if __name__ == "__main__":
    # Define the template path
    template_path = EMAIL_TEMPLATE_PATH

    # Load data from the Excel file containing details about hiring managers, company info, etc.
    excel_path = EXCEL_DATA_PATH
    data = load_data(excel_path)

    # Iterate over each row in the DataFrame, processing one email at a time
    for index, row in data.iterrows():
        # Prepare the context with data from the Excel sheet for the email template
        context = {
            'HIRING_MANAGER': row['HIRING_MANAGER'],
            'COMPANY_NAME': row['COMPANY_NAME'],
            'COMPANY_VALUES': row['COMPANY_VALUES'],
            'COMPANY_SUMMARY': row['COMPANY_SUMMARY'],
            'JOB_TITLE': row['JOB_TITLE'],
            # Use skills from the row if available, otherwise fallback to default skills
            'MY_SKILLS': row['MY_SKILLS'] if pd.notna(row['MY_SKILLS']) else MY_DEFAULT_SKILLS,
            'NAME': MY_NAME  # Sender's name, loaded from environment variables
        }

        # Create a personalized email subject based on the company name
        subject = f'Bringing Innovation and Dedication to {context["COMPANY_NAME"]}'

        # Ensure the Excel file contains an 'EMAIL' column for the recipient's email address
        to_email = row['EMAIL']

        # Generate custom content for the email body using AI (from the backend service)
        context['COMPANY_PRAISE'] = genai_generate_content(str(context))

        # Load the HTML email template and replace the placeholders with actual content
        email_content = load_template(template_path, context)

        # Log the email recipient for tracking purposes
        print("Sending email to:", to_email)

        # Use Celery to send the email asynchronously, so the main process is not blocked
        result = send_email_task.delay(
            subject, to_email, email_content, MY_EMAIL, MY_EMAIL_APP_PASSWORD)

        # Log the completion and the Celery task ID for tracking
        print("Email sending initiated.")
        print(result)
