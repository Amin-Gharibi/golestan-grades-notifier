from utils import *

# load environmental variables
username, password, semester_code, uni_website, golestan_website = load_env()

# set up browser
driver = set_up_browser()

driver.get(uni_website)

# submit login form
login(driver, username, password)

sleep(2)

driver.find_element(By.CSS_SELECTOR, f'a[href^="{golestan_website}"]').click()
driver.switch_to.window(driver.window_handles[1])

sleep(10)
go_to_full_information_page(driver)

sleep(5)
go_to_target_semester(driver, semester_code)

sleep(5)
base_courses = get_semester_courses(driver)

wait_for_updates(driver, base_courses)
