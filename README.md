# GOLESTAN GRADE-UPDATE NOTIFIER

## What Is It?
Have you experienced waiting for your teacher to enter your grade in GOLESTAN SYSTEM?
isn't it a bit hard to refresh website and wait for it to show up?
well this application has solved that problem 😄

## How Does It Work?
This application would log in to your Golestan account and goes to the semester-you-want's page and waits for any updates on your grades column :)

## How To Run It?
First off you need to install the requirements of this project.
<br>
in order to do such a thing you need to open your terminal in the folder of the project and run this command:
```
pip install -r requirements.txt
```
and when it's done you need to create a file named
```
.env
```
and in it, you should fill out such a form:
```
UID=<YOUR GOLESTAN LOGIN USERNAME>
PWD=<YOUR GOLESTAN LOGIN PASSWORD>
SEMESTER_CODE=<CODE OF THE TARGET SEMESTER>
GOLESTAN_WEBSITE=<YOUR UNIVERSITIES GOLESTAN WEBSITE LINK>
REFRESH_RATE=<WAITING TIME FOR EACH REFRESH ON GRADES PAGE PER SEC.>
SENDER_EMAIL=<THE EMAIL ADDRESS WHICH YOU WANT TO RECEIVE EMAIL OF UPDATES ON GRADE NOTIFICATION FROM>
SENDER_PASSWORD=<PASSWORD OF THE UPPER EMAIL>
RECEIVER_EMAIL=<THE EMAIL YOU WANT TO RECEIVE THE NOTIFICATION EMAIL IN IT>
```
if you are confused right now it's ok :)
<br>
an example of the upper form is:
```
UID='40212345678'
PWD='my_password'
SEMESTER_CODE='4022'
GOLESTAN_WEBSITE='https://edu.ilam.ac.ir'
REFRESH_RATE=10
SENDER_EMAIL='sender_email@gmail.com'
SENDER_PASSWORD='sender_email_password'
RECEIVER_EMAIL='receiver_email@gmail.com'
```
after filling out .env file you can simply open terminal in projects folder
and run this command:
```
python main.py
```

## Usage Note
- For running this application you need python 3 to be installed in your system, this application has been built on python 3.12 version, so we recommend you use python 3.12.x for running this program
- Unfortunately this application **WOULDN'T work** for the **FRESHMEN** guys because website would automatically log us out of system


## DISCLAIMER
This application doesn't store any of your data, any possible issues with your data is out of our responsibility