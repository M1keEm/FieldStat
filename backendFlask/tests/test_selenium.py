import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
service = Service("/opt/homebrew/bin/chromedriver")

class SeleniumTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get("http://localhost:3000")

    def tearDown(self):
        self.driver.quit()

    def test_title(self):
        print("Testing title...")
        print("Page title:", self.driver.title)
        self.assertIn("FieldStat", self.driver.title)

    def test_register(self):
        driver = self.driver
        driver.get("http://localhost:3000/register")
        time.sleep(1)
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        confirm_password_input = driver.find_element(By.NAME, "confirmPassword")
        username_input.send_keys("seleniumuser")
        password_input.send_keys("seleniumpass")
        confirm_password_input.send_keys("seleniumpass")
        password_input.send_keys(Keys.RETURN)
        time.sleep(2)
        body_text = driver.find_element(By.TAG_NAME, "body").text
        self.assertTrue("success" in body_text.lower() or "login" in body_text.lower())

    def test_login(self):
        driver = self.driver
        driver.get("http://localhost:3000/login")
        time.sleep(1)
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys("seleniumuser")
        password_input.send_keys("seleniumpass")
        password_input.send_keys(Keys.RETURN)
        time.sleep(2)
        body_text = driver.find_element(By.TAG_NAME, "body").text
        self.assertTrue("dashboard" in body_text.lower() or "welcome" in body_text.lower())

if __name__ == "__main__":
    unittest.main()
