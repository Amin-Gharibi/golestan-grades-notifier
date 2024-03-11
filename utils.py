import os
from dotenv import load_dotenv
from selenium import webdriver
from time import sleep
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from gl import *


def load_env():
    load_dotenv()
    username = os.getenv('UID')
    password = os.getenv('PWD')
    semester_code = os.getenv('SEMESTER_CODE')
    uni_website = os.getenv('UNI_WEBSITE')
    golestan_website = os.getenv('GOLESTAN_WEBSITE')

    return username, password, semester_code, uni_website, golestan_website


def set_up_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome()

    return driver


def login(driver, username, password):
    driver.find_element(By.ID, 'username').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'submit').click()


# switch to etelaat-e jame-e daneshjoo
def go_to_full_information_page(driver):
    finder = FindElemInGolestan(driver)
    student_full_information_btn = finder.find_by_xpath('//*[@id="mendiv"]/table/tbody/tr[5]/td')
    finder.double_click(student_full_information_btn)


# switch to the semester user wants
def go_to_target_semester(driver, semester_code):
    finder = FindElemInGolestan(driver)
    target_semester_btn = finder.find_by_css(f"td[title='{semester_code}']")
    finder.double_click(target_semester_btn)


def get_semester_courses(driver):
    finder = FindElemInGolestan(driver)
    courses = finder.fetch_courses()
    return courses


def wait_for_updates(driver, base_courses):
    def init_finder():
        finder = FindElemInGolestan(driver)
        finder.locate_driver_in_courses_page()
        return finder

    refresh_rate = int(os.getenv('REFRESH_RATE'))

    while True:
        finder = init_finder()
        prev_semester = finder.find_by_css('img[title="ترم قبلي"]')
        finder.double_click(prev_semester)
        sleep(3)
        finder = init_finder()
        current_semester = finder.find_by_css('img[title="ترم بعدي"')
        finder.double_click(current_semester)
        sleep(3)

        courses = get_semester_courses(driver)
        if base_courses != courses:
            for i in range(len(courses)):
                if courses[i].score != base_courses[i].score:
                    send_email(courses[i])
                    wait_for_updates(driver, courses)

        sleep(refresh_rate)


def send_email(course):
    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    subject = f'نمره درس {course["name"]} ثبت شد'
    html_message = f"""\
    <html>
      <body>
        <h1>سلام داشی 👋🏽</h1>
        <h2>اومدم بهت خبر بدم نمره درس {course['name']} که کدش {course["code"]} هست و یه درس {course["credits"]} واحدی هست اومده واست :))</h2>
        <h2>نمره ات شده: 8.75</h2>
        <h3>امیدوارم از نمره هشت و هفتاد و پنج صدمت راضی باشی 😂😂</h3>
        <p>شوخی کردم عزیز نمره اصلیت شده {course["score"]} . امیدوارم که از نمره ات راضی باشی و این رو در نظر بگیر که نمره هیچ تاثیری در اینده تو نداره 😶‍🌫️</p>
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
