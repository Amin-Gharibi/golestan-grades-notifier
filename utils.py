import os
from dotenv import load_dotenv
from selenium import webdriver
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def load_env():
    """
    this function would load all the environment variables and returns them in a dictionary
    if one of the variables was missing it would terminate application and raises an error
    :return: DICTIONARY OF ENVIRONMENTAL VARIABLES
    """
    try:
        load_dotenv()
        username = os.getenv('UID')
        password = os.getenv('PWD')
        semester_code = os.getenv('SEMESTER_CODE')
        golestan_website = os.getenv('GOLESTAN_WEBSITE')
        refresh_rate = os.getenv('REFRESH_RATE')
        sender_email = os.getenv('SENDER_EMAIL')
        receiver_email = os.getenv('RECEIVER_EMAIL')
        sender_password = os.getenv('SENDER_PASSWORD')

        if username and password and semester_code and golestan_website and refresh_rate and sender_email and sender_password and receiver_email is not None:
            return username, password, semester_code, golestan_website, int(refresh_rate), sender_email, sender_password, receiver_email
        else:
            raise ValueError
    except ValueError:
        print('Please Provide All The Environmental Variables In The .env File')


def set_up_browser():
    """
    this function would set up browser using selenium
    :return: driver instance
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options)

    return driver


def send_email(course):
    """
    this function handles sending email operation
    IF YOU WANT TO CHANGE THE HTML TEMPLATE OF THE EMAIL YOU CAN CHANGE THE html_message VARIABLE
    :param course: this is the target course you are trying to send it's updated grade to user's email
    """
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
