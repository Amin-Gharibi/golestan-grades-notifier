from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import ActionChains


class FindElemInGolestan(object):
    def __init__(self, driver):
        self.driver = driver
        driver.switch_to.default_content()

        iframe = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, "#FacArea > div:last-child > iframe")))
        driver.switch_to.frame(iframe)

        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, 'frameset')))

        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, "inFrmset")))

        master_frame = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.NAME, 'Master')))
        driver.switch_to.frame(master_frame)

        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "frameset")))

        form_body_frame = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.NAME, 'Form_Body')))
        driver.switch_to.frame(form_body_frame)

        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, 'body')))

    def locate_driver_in_courses_page(self):
        frame_new_form = WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, 'FrameNewForm')))
        self.driver.switch_to.frame(frame_new_form)

    def fetch_courses(self):
        self.locate_driver_in_courses_page()

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

        return user_semester_courses

    def find_by_xpath(self, xpath):
        element = self.driver.find_element(By.XPATH, xpath)
        return element

    def find_by_css(self, css):
        element = self.driver.find_element(By.CSS_SELECTOR, css)
        return element

    def find_elements_by_xpath(self, xpath):
        elements = self.driver.find_elements(By.XPATH, xpath)
        return elements

    def find_elements_by_css(self, css):
        elements = self.driver.find_elements(By.CSS_SELECTOR, css)
        return elements

    def find_elements_by_tag_name(self, tag_name):
        elements = self.driver.find_elements(By.TAG_NAME, tag_name)
        return elements

    def double_click(self, btn):
        actions = ActionChains(self.driver)
        actions.double_click(btn).perform()
