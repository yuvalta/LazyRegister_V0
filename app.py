import os

from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def go_to_course_signin(signin_url, web_driver, wanted_course_name):
    web_driver.get(signin_url)
    # wait for URL to change with 60 seconds timeout - user need to insert his ID and password
    try:
        WebDriverWait(web_driver, 60).until(EC.url_changes(signin_url))
    except TimeoutException:
        web_driver.close()

    while 1:
        # press רישום in top bar
        elem1 = WebDriverWait(web_driver, 180).until(
            EC.presence_of_element_located((By.XPATH, "//*[@title='רישום']")))
        elem1.click()

        # press רישום in right side bar
        elem1 = WebDriverWait(web_driver, 180).until(
            EC.presence_of_element_located((By.ID, "L1N1")))
        elem1.click()

        # loop until registration is available
        while 1:
            elem1 = WebDriverWait(web_driver, 1).until(
                EC.presence_of_element_located((By.ID, "L1N1")))
            elem1.click()

            # resetiFrames(web_driver)
            #
            # first_time_button = WebDriverWait(web_driver, 180).until(
            #     EC.element_to_be_clickable((By.ID, "aaaa.ProgramView.SaveButton.0")))
            # first_time_button.click()

            resetiFrames(web_driver)

            try:
                elem1 = WebDriverWait(web_driver, 5).until(
                    EC.presence_of_element_located(
                        (By.ID, "aaaa.ProgramView.BookingButton.0")))
                break

            except TimeoutException:
                print("מנסה שוב  - זמן")
                web_driver.switch_to.default_content()
                continue
            except NoSuchElementException:
                print("מנסה שוב - לא נמצא")
                web_driver.switch_to.default_content()
                continue

        print(datetime.now().time())  # timestamp of start
        elem1.click()  # press המשך לרישום

        resetiFrames(web_driver)

        try:
            element_name = "aaaa.ModuleBasketView.stext_smInp";
            elem1 = WebDriverWait(web_driver, 180).until(  # course name textbox
                EC.presence_of_element_located((By.ID, element_name)))
            elem1.click()

            elem1.send_keys(wanted_course_name)  # enter the course name in the textbox

            elem1.send_keys(Keys.RETURN)  # press ENTER

            # table of sorted courses appears, choose the first
            element_name = "aaaa.ModuleBasketView.Choose.0";
            elem1 = WebDriverWait(web_driver, 180).until(
                EC.visibility_of_element_located((By.ID, element_name)))
            elem1.click()

            resetiFrames(web_driver)

            # press next
            element_name = "aaaa.ModuleBasketView.NextButton"
            elem1 = WebDriverWait(web_driver, 180).until(
                EC.element_to_be_clickable((By.ID, element_name)))
            elem1.click()

            print(datetime.now().time())
            # press save
            element_name = "aaaa.EventPackageSelectionView.bookingButton"
            elem1 = WebDriverWait(web_driver, 180).until(
                EC.element_to_be_clickable((By.ID, element_name)))

            elem1.click()
            print(datetime.now().time())

        except StaleElementReferenceException:
            print(element_name)
            elem1 = WebDriverWait(web_driver, 180).until(
                EC.element_to_be_clickable((By.ID, element_name)))
            elem1.click()


def resetiFrames(web_driver):
    web_driver.switch_to.default_content()

    elem1 = WebDriverWait(web_driver, 180).until(
        EC.presence_of_element_located((By.NAME, "contentAreaFrame")))
    web_driver.switch_to.frame(elem1)

    # time.sleep(0.5)

    elem1 = WebDriverWait(web_driver, 180).until(
        EC.presence_of_element_located((By.NAME, "isolatedWorkArea")))
    web_driver.switch_to.frame(elem1)


wanted_course_name = "עיבוד תמונה"

if os.name == 'nt':
    web_driver = webdriver.Chrome(executable_path="webDrivers/chromedriver_win.exe")
else:
    web_driver = webdriver.Chrome(executable_path="webDrivers/chromedriver_macOS")

signin_url = "https://huids.haifa.ac.il/nidp/idff/sso?id=334&sid=0&option=credential&sid=0&target=https://stud.haifa.ac.il/irj/portal"

go_to_course_signin(signin_url, web_driver, wanted_course_name)
