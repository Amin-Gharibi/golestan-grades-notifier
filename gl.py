"""
fetch courses page
frame_new_form = WebDriverWait(self.gl.driver, 10).until(ec.presence_of_element_located((By.ID, 'FrameNewForm')))
self.gl.driver.switch_to.frame(frame_new_form)
"""


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import ActionChains
import utils
import os
from time import sleep


class Gl(object):
    def __init__(self):
        self.driver = utils.set_up_browser()

        self.username, self.password, self.semester_code, self.uni_website, self.golestan_website = utils.load_env()

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

    def navigate_to_login_page(self):
        self.driver.get(self.uni_website)

    def login(self):
        self.find_element_by_id('username').send_keys(self.username)
        self.find_element_by_id('password').send_keys(self.password)
        self.find_element_by_id('submit').click()

    def navigate_to_golestan_page(self):
        self.find_element_by_css(f"a[href^='{self.golestan_website}']").click()
        self.driver.switch_to.window(self.driver.window_handles[1])

    def navigate_to_content_frame(self):
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

    def switch_back_to_main_frame(self):
        self.driver.switch_to.default_content()

    def go_to_student_full_information_page(self):
        self.navigate_to_content_frame()
        element = self.find_element_by_xpath('//*[@id="mendiv"]/table/tbody/tr[5]/td')
        self.double_click(element)
        self.switch_back_to_main_frame()

    def go_to_target_semester_page(self):
        self.navigate_to_content_frame()
        element = self.find_element_by_css(f'td[title="{self.semester_code}"]')
        self.double_click(element)
        self.switch_back_to_main_frame()

    def fetch_courses(self):


    def find_element_by_xpath(self, xpath):
        element = self.driver.find_element(By.XPATH, xpath)
        return element

    def find_element_by_css(self, css):
        element = self.driver.find_element(By.CSS_SELECTOR, css)
        return element

    def find_element_by_id(self, css_id):
        element = self.driver.find_element(By.ID, css_id)
        return element

    def double_click(self, element):
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
