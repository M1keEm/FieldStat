import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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


if __name__ == "__main__":
    unittest.main()
