from django.test import LiveServerTestCase
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

from .models import Food, Portion, Intake, Measurement, Diary, Personal

class OpenHomeWithoutLoggedInTestCase(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        # super(AccountTestCase, self).setUp()

    def tearDown(self):
        self.driver.quit()
        # super(AccountTestCase, self).tearDown()

    def test_index(self):
        """
        Try to open 'Home' page without logging in.
        """

        driver = self.driver

        # Open the link I want to test
        driver.get('http://127.0.0.1:8000')

        # Find form elemets
        title = driver.title
        username_field = driver.find_element_by_id("usernameInput")
        password_field = driver.find_element_by_id("passwordInput")
        login_button = driver.find_element_by_id("login_button")

        print(page_title)

        # Check the title(s) of the loaded page
        self.assertEqual(title, "Login")

        # Enter login data and press Login button
        username_field.send_keys("varger")
        password_field.send_keys("VarBu622")

        login_button.click()

        # Find form elemets (after page reloads)
        title = driver.title
        page_title = driver.find_element_by_id("page_title")

        self.assertEqual(title, "Home")
