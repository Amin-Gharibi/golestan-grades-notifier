import os
from dotenv import load_dotenv
from selenium import webdriver
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def load_env():
    try:
        load_dotenv()
        username = os.getenv('UID')
        password = os.getenv('PWD')
        semester_code = os.getenv('SEMESTER_CODE')
        uni_website = os.getenv('UNI_WEBSITE')
        golestan_website = os.getenv('GOLESTAN_WEBSITE')
        refresh_rate = os.getenv('REFRESH_RATE')
        sender_email = os.getenv('SENDER_EMAIL')
        receiver_email = os.getenv('RECEIVER_EMAIL')
        sender_password = os.getenv('SENDER_PASSWORD')

        if username and password and semester_code and uni_website and golestan_website and refresh_rate and sender_email and sender_password and receiver_email is not None:
            return username, password, semester_code, uni_website, golestan_website, int(refresh_rate), sender_email, sender_password, receiver_email
        else:
            raise ValueError
    except ValueError:
        print('Please Provide All The Environmental Variables In The .env File')


def set_up_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome()

    return driver


def send_email(course):
    *rest, sender_email, sender_password, receiver_email = load_env()
    subject = f'نمره درس {course["name"]} ثبت شد'
    html_message = f"""\
    <html>
      <body>
        <h1>سلام داشی 👋🏽</h1>
        <h2>اومدم بهت خبر بدم نمره درس {course['name']} که کدش {course["code"]} هست و یه درس {course["credits"]} واحدی هست اومده واست :))</h2>
        <h2>نمره ات شده: 8.75</h2>
        <h3>امیدوارم از نمره هشت و هفتاد و پنج صدمت راضی باشی 😂😂</h3>
        <p>شوخی کردم عزیز نمره اصلیت شده <h2>{course["score"]}</h2> . امیدوارم که از نمره ات راضی باشی و این رو در نظر بگیر که نمره هیچ تاثیری در اینده تو نداره 😶‍🌫️</p>
        <p>Best regards,<br>MohamadAmin Gharibi</p>
      </body>
    </html>
    """
    # Set up the MIME
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Attach the HTML message to the MIME
    html_message = MIMEText(html_message, 'html')
    message.attach(html_message)

    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # Use the appropriate SMTP server
    session.starttls()  # Enable security
    session.login(sender_email, sender_password)  # Login with sender email and password

    # Send the email
    text = message.as_string()
    session.sendmail(sender_email, receiver_email, text)

    # Quit the session
    session.quit()
