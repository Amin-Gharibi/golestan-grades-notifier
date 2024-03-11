from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import ActionChains
import utils
from time import sleep


class Gl(object):
    def __init__(self):
        """
        Initializes GOLESTAN LOGIC class
        it sets up the driver and loads the environmental variables and runs the application
        """
        self.driver = utils.set_up_browser()

        self.username, self.password, self.semester_code, self.golestan_website, self.refresh_rate, *rest = utils.load_env()

        # run app
        self.navigate_to_login_page()
        self.login()
        sleep(10)
        self.go_to_student_full_information_page()
        sleep(5)
        self.go_to_target_semester_page()
        sleep(5)
        self.base_courses = self.fetch_courses()
        self.wait_for_updates()

    def navigate_to_login_page(self):
        """
        navigate to golestan website and click on login link and switch to login page
        """
        self.driver.get(self.golestan_website)
        self.find_element_by_xpath('/html/body/div/div/table/tbody/tr[3]/td[5]').click()
        sleep(15)
        self.driver.switch_to.window(self.driver.window_handles[1])

    def login(self):
        """
        fill out login form and submit it
        NOTE THAT IF YOUR UNIVERSITY'S LOGIN FORM DOESN'T HAVE INPUTS WITH ID'S LIKE username AND password AND submit
        THIS APPLICATION DOESN'T WORK AND YOU NEED TO CHANGE THEIR ID'S HERE IN THIS FUNCTION!!!
        """
        self.find_element_by_id('username').send_keys(self.username)
        self.find_element_by_id('password').send_keys(self.password)
        self.find_element_by_id('submit').click()

    def switch_to_content_frame(self):
        """
        because golestan loads dynamically using iframe tags you can't access the elements in the page directly, and
        you need to go inside each iframe and frame tag step by step and wait for it to load, so I created
        such a function to do this each time I want to select an element from the page

        summary: this functions leads driver to the frame that contains all the main elements
        """
        iframe = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, "#FacArea > div:last-child > iframe")))
        self.driver.switch_to.frame(iframe)

        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, 'frameset')))

        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, "inFrmset")))

        master_frame = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.NAME, 'Master')))
        self.driver.switch_to.frame(master_frame)

        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "frameset")))

        form_body_frame = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.NAME, 'Form_Body')))
        self.driver.switch_to.frame(form_body_frame)

        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, 'body')))

    def switch_to_courses_frame(self):
        """
        because courses list are in another frame I needed to create this function to switch to that frame
        and then get courses list from that frame
        """
        self.switch_to_content_frame()
        frame_new_form = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, 'FrameNewForm')))
        self.driver.switch_to.frame(frame_new_form)

    def switch_back_to_main_frame(self):
        """
        each time I switch to different frames driver stays in that frame, so I would need to switch back to main frame
        in order to avoid having problems when finding elements and going to other pages
        """
        self.driver.switch_to.default_content()

    def go_to_student_full_information_page(self):
        """
        this function would select ETELAAT-E JAME-E DANESHJOO button and double-clicks on it
        """
        self.switch_to_content_frame()
        element = self.find_element_by_xpath('//*[@id="mendiv"]/table/tbody/tr[5]/td')
        self.double_click(element)
        self.switch_back_to_main_frame()

    def go_to_target_semester_page(self):
        """
        this function would select the target semester user wanted the grades from and double-clicks on it
        """
        self.switch_to_content_frame()
        element = self.find_element_by_css(f'td[title="{self.semester_code}"]')
        self.double_click(element)
        self.switch_back_to_main_frame()

    def fetch_courses(self):
        """
        this function would select all the courses rows and save data needed from each of them
        :return: list of courses including each courses detail
        """
        self.switch_to_courses_frame()

        rows = self.find_elements_by_xpath('//*[@id="T02"]/tbody/tr[@class="TableDataRow"]')

        user_semester_courses = []

        for row in rows:
            tds = row.find_elements(By.TAG_NAME, "td")
            course_code = ''
            for i in range(4, 0, -1):
                course_code += tds[i].get_attribute('title')
            course_name = tds[5].get_attribute('title')
            course_credits = tds[6].get_attribute('title')
            course_score_status = tds[9].get_attribute('title')
            course_score = tds[10].get_attribute('title')
            course = {
                'code': course_code,
                'name': course_name,
                'credits': course_credits,
                'score_status': course_score_status,
                'score': course_score
            }
            user_semester_courses.append(course)

        self.switch_back_to_main_frame()
        return user_semester_courses

    def wait_for_updates(self):
        """
        golestan would log me out if I'm not active and clicking on buttons, so I created a system that
        each time click on prev-semester button and then clicks on next-semester button, so it wouldn't
        log me out of system
        after checking for updates it waits for the amount of REFRESH_RATE entered in .env file
        and then repeats the same again and again
        """
        def switch_semester(css_selector):
            self.switch_to_courses_frame()
            self.find_element_by_css(css_selector).click()
            self.switch_back_to_main_frame()

        while True:
            courses = self.fetch_courses()
            for i in range(len(courses)):
                if courses[i] != self.base_courses[i]:
                    utils.send_email(courses[i])

            switch_semester('img[title="ترم قبلي"]')
            sleep(3)
            switch_semester('img[title="ترم بعدي"]')
            sleep(self.refresh_rate - 3)

    def find_element_by_xpath(self, xpath):
        """
        it would find ONE element based on it's xpath and returns it
        :param xpath: XPATH string
        :return: HTML ELEMENT
        """
        element = self.driver.find_element(By.XPATH, xpath)
        return element

    def find_elements_by_xpath(self, xpath):
        """
        it would find MULTIPLE elements based on their xpath and returns them
        :param xpath: XPATH string
        :return: LIST OF HTML ELEMENTS
        """
        elements = self.driver.find_elements(By.XPATH, xpath)
        return elements

    def find_element_by_css(self, css):
        """
        it would find ONE element based on the css selector provided in arguments and returns it
        :param css: CSS-SELECTOR string
        :return: HTML ELEMENT
        """
        element = self.driver.find_element(By.CSS_SELECTOR, css)
        return element

    def find_element_by_id(self, css_id):
        """
        it would find ONE element based on its id in html template and returns it
        :param css_id: ID ATTRIBUTE OF ELEMENT string
        :return: HTML ELEMENT
        """
        element = self.driver.find_element(By.ID, css_id)
        return element

    def double_click(self, element):
        """
        this function would simulate a double click on the element passed in as argument
        :param element: HTML ELEMENT
        """
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
