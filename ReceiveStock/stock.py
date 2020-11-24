from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

PATH = "C:/Program Files (x86)/chromedriver.exe"
LOGIN_NAME = os.environ.get('MCN_USERNAME')
LOGIN_PW = os.environ.get('MCN_PASS')
    

class ReceiveStock():
    def __init__(self):
        self.driver = webdriver.Chrome(PATH)
        self.driver.get('https://mcndealers.com/users/sign_in')
        self.stock_window = self.driver.window_handles[0]
    def login(self):
        username = self.driver.find_element_by_id('login_name')
        username.clear()
        username.send_keys(LOGIN_NAME)

        password = self.driver.find_element_by_id('login_pw')
        password.clear()
        password.send_keys(LOGIN_PW)

        enter = self.driver.find_element_by_name('login_btn')
        enter.send_keys(Keys.RETURN)
