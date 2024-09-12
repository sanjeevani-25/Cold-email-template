
---

# Cold Email Automation Project

This project automates sending cold emails based on data from an Excel sheet, utilizing an email template and content generation from an API. It uses Celery to handle background tasks such as sending emails.

## Step-by-Step Instructions

### 1. Create a Virtual Environment and Activate It

First, create a virtual environment to isolate your project dependencies.

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment (for Windows)
venv\Scripts\activate

# Activate the virtual environment (for macOS/Linux)
source venv/bin/activate
```

### Install requirements.txt

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

### 2. Get Gemini API Key and Add It to `.env` File

- Go to the Gemini API platform and generate an API key for content generation. 
- Create a `.env` file in the project root and add the following:

```bash
API_KEY=<your-gemini-api-key>
```

Replace `<your-gemini-api-key>` with your actual API key.

### 3. Add Other Details to `.env`

You will also need to add other environment variables to the `.env` file, such as email credentials and personal information.

```bash
SENDER_EMAIL=<your-email-address>
SENDER_EMAIL_APP_PASSWORD=<your-email-app-password>
SENDER_NAME=<your-name>
DEFAULT_SKILLS=<your-default-skills>
PROMPT=<your-prompt-for-generating-content>
```

- **SENDER_EMAIL**: Your email address that will be used to send emails.
- **SENDER_EMAIL_APP_PASSWORD**: Your app-specific password for logging in (e.g., for Gmail). Watch [this YouTube video](https://www.youtube.com/watch?v=HtC_wLpR-fA) to learn how to generate an app password for Gmail.
- **SENDER_NAME**: Your name as the sender.
- **DEFAULT_SKILLS**: Your default skills to be added in the email template.
- **PROMPT**: The default prompt for generating content from the Excel data.

### 4. Make the Excel Sheet

Create an Excel file (`email_companies_data.xlsx`) with the following columns:

- **HIRING_MANAGER**: Name of the hiring manager.
- **COMPANY_NAME**: Name of the company.
- **COMPANY_VALUES**: Core values of the company.
- **COMPANY_SUMMARY**: Brief company description.
- **JOB_TITLE**: The job title you're applying for.
- **MY_SKILLS**: Your skills (use default skills if not provided).
- **EMAIL**: Email address of the hiring manager.

Example:

| HIRING_MANAGER | COMPANY_NAME | COMPANY_VALUES | COMPANY_SUMMARY | JOB_TITLE           | MY_SKILLS                | EMAIL               |
|----------------|--------------|----------------|-----------------|---------------------|--------------------------|---------------------|
| John Doe       | ABC Corp     | Innovation     | Tech leadership | Software Engineer    | Python, Django, ReactJS   | john.doe@abccorp.com|
| Jane Smith     | XYZ Inc      | Integrity      | Service excellence| Backend Developer    | Java, Spring, SQL         | jane.smith@xyz.com  |

### 5. Make the Email Template

Create an HTML file (`email_template.html`) for your email template. Use placeholders that match the columns in your Excel sheet. The content generated using the API will be added dynamically.

```html
<html>
<body>
    <p>Dear {HIRING_MANAGER},</p>
    <p>I am excited to apply for the {JOB_TITLE} role at {COMPANY_NAME}. I admire your company's values of {COMPANY_VALUES} and its commitment to {COMPANY_SUMMARY}.</p>
    <p>With my skills in {MY_SKILLS}, I believe I can contribute to your team and drive innovation.</p>
    <p>Best regards,</p>
    <p>{NAME}</p>
</body>
</html>
```

Make sure the column names in your Excel file match the placeholders in the template. The dynamic content will be inserted accordingly.

### 6. Run the Project

#### To Send Emails:

Run the script that sends emails:

```bash
python cold_email.py
```

This will load the data from the Excel sheet, generate the email content, and send emails to the recipients.

Here’s a refined version that covers the Celery and Redis setup for both macOS and Windows, with Redis details hidden under a toggle section for easy access.

### 6. Running Celery with Redis

Celery is used to manage background tasks (in this case, sending emails) asynchronously. In this project, Celery works alongside Redis, which serves as the message broker.

#### Step 1: Install Redis


<details>
  <summary><strong>Click to view Redis Installation Details</strong></summary>

**macOS:**

1. Install Homebrew:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Install Redis:
   ```bash
   brew install redis
   ```
3. Start Redis:
   ```bash
   brew services start redis
   ```

**Windows:**

1. Download Redis for Windows [here](https://github.com/tporadowski/redis/releases).
2. Install Redis by following the setup instructions.
3. Start the Redis server using the following command:
   ```bash
   redis-server
   ```

</details>

#### Step 2: Running Redis Server

Once Redis is installed, you need to start the Redis server before running Celery.

- **macOS:**
  Redis can be started with:
  ```bash
  brew services start redis
  ```

- **Windows:**
  Start the Redis server by running the following in your command prompt:
  ```bash
  redis-server
  ```

#### Step 3: Running Celery

With Redis running in the background, you can now launch Celery workers to process the background tasks.

```bash
celery -A celery_app worker --concurrency=10 --loglevel=info
```

In this command:
- `--concurrency=10` indicates that Celery will use 10 workers (you can adjust this based on your system resources).
- `--loglevel=info` controls the verbosity of Celery's output logs.

> **Note**: Make sure Redis is running in the background before executing this command, as Celery relies on Redis to manage tasks.

---

### 7. About Celery

Celery is a distributed task queue used for handling long-running or time-consuming tasks in the background. It enables task management without blocking your main process.

In this project:

- **Celery** is used to send emails asynchronously as background tasks.
- **Redis** is the message broker that Celery uses to store and distribute the tasks.

You can scale the system by adjusting the number of worker threads (`--concurrency`) to process tasks concurrently. Task status can be monitored using Celery’s logs.

---

---

<center>Happy coding! 😊</center>

---

---
