import time
import os
import json

import selenium_stealth
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv


load_dotenv("env.env")
LOGIN = os.environ.get("LOGIN")
PASS = os.environ.get("PASS")
TARGET_ACCOUNT = "comicpopofficial"
COOKIE_FILE_NAME = "instacookies.txt"

url = "https://www.instagram.com"
options = Options()
prefs = {"credentials_enable_service": False,
     "profile.password_manager_enabled": False}
options.add_experimental_option("prefs", prefs)
options.add_experimental_option("detach", True)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)


class InstaFollower:
    def __init__(self):
        self.driver = webdriver.Chrome(options)
        selenium_stealth.stealth(self.driver,
                                 user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                                 languages=["en", "en-US"],
                                 platform="web",
                                 )
        self.driver.set_window_position(450, 9)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


    def load_cookies(self):
        with open(COOKIE_FILE_NAME) as file:
            cookies = file.readlines()
            for cookie in cookies:
                self.driver.add_cookie(json.loads(cookie))
    def login(self):
        self.driver.get("https://instagram.com")
        self.load_cookies()
        self.driver.get(f"{url}/accounts/login")
        time.sleep(1)
        if self.driver.find_elements(By.NAME, "username"):
            username_entry_element = self.driver.find_element(By.NAME, "username")
            username_entry_element.send_keys(LOGIN)
            password_entry_element = self.driver.find_element(By.NAME, "password")
            password_entry_element.send_keys(PASS)
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
        time.sleep(6)
        self.driver.find_element(By.XPATH, "//button[text()='Not Now']").click()


    def find_followers(self):
        self.driver.get(f"{url}/{TARGET_ACCOUNT}")
        time.sleep(5)
        follower_count_elmnt = self.driver.find_element(By.CSS_SELECTOR, 'a[href="/comicpopofficial/followers/"] span span')
        fc = int(follower_count_elmnt.text.replace(",",""))
        print(f"{fc=}")
        target_index  = fc - 1
        followers_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, "followers")
        followers_link.click()
        time.sleep(2)
        popup_elmnt = self.driver.find_element(By.CSS_SELECTOR, "div[role='dialog']")
        current_length = 0
        while current_length < target_index:
            follow_buttons = popup_elmnt.find_elements(By.XPATH, "//*[text()='Follow']")
            ActionChains(self.driver).scroll_to_element(follow_buttons[-1]).perform()
            print(len(follow_buttons))
            current_length = follow_buttons.index(follow_buttons[-1])
            print(f"{current_length=}")
            # time.sleep(0.5)



    def follow(self):
        pass

    def get_cookies(self):
        cookies = self.driver.get_cookies()
        with open(COOKIE_FILE_NAME, "w") as file:
            for cookie in cookies:
                json.dump(cookie, file)
                file.write("\n")

insta_follower = InstaFollower()
insta_follower.login()
insta_follower.get_cookies()
insta_follower.find_followers()
insta_follower.follow()
