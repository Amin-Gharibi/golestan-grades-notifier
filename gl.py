from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import ActionChains
import utils
from time import sleep


class Gl(object):
    def __init__(self):
        self.driver = utils.set_up_browser()

        self.username, self.password, self.semester_code, self.uni_website, self.golestan_website, self.refresh_rate, *rest = utils.load_env()

        # run app
        self.navigate_to_login_page()
        self.login()
        sleep(2)
        self.navigate_to_golestan_page()
        sleep(10)
        self.go_to_student_full_information_page()
        sleep(5)
        self.go_to_target_semester_page()
        sleep(5)
        self.base_courses = self.fetch_courses()
        self.wait_for_updates()

    def navigate_to_login_page(self):
        self.driver.get(self.uni_website)

    def login(self):
        self.find_element_by_id('username').send_keys(self.username)
        self.find_element_by_id('password').send_keys(self.password)
        self.find_element_by_id('submit').click()

    def navigate_to_golestan_page(self):
        self.find_element_by_css(f"a[href^='{self.golestan_website}']").click()
        self.driver.switch_to.window(self.driver.window_handles[1])

    def switch_to_content_frame(self):
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
        self.switch_to_content_frame()
        frame_new_form = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, 'FrameNewForm')))
        self.driver.switch_to.frame(frame_new_form)

    def switch_back_to_main_frame(self):
        self.driver.switch_to.default_content()

    def go_to_student_full_information_page(self):
        self.switch_to_content_frame()
        element = self.find_element_by_xpath('//*[@id="mendiv"]/table/tbody/tr[5]/td')
        self.double_click(element)
        self.switch_back_to_main_frame()

    def go_to_target_semester_page(self):
        self.switch_to_content_frame()
        element = self.find_element_by_css(f'td[title="{self.semester_code}"]')
        self.double_click(element)
        self.switch_back_to_main_frame()

    def fetch_courses(self):
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
        element = self.driver.find_element(By.XPATH, xpath)
        return element

    def find_elements_by_xpath(self, xpath):
        elements = self.driver.find_elements(By.XPATH, xpath)
        return elements

    def find_element_by_css(self, css):
        element = self.driver.find_element(By.CSS_SELECTOR, css)
        return element

    def find_element_by_id(self, css_id):
        element = self.driver.find_element(By.ID, css_id)
        return element

    def double_click(self, element):
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
