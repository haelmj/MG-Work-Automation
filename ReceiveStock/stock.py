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
        """Handles Website login"""
        username = self.driver.find_element_by_id('login_name')
        username.clear()
        username.send_keys(LOGIN_NAME)

        password = self.driver.find_element_by_id('login_pw')
        password.clear()
        password.send_keys(LOGIN_PW)

        enter = self.driver.find_element_by_name('login_btn')
        enter.send_keys(Keys.RETURN)
    
    def getRows(self, element):
        row_group = element.find_element_by_tag_name('tbody')
        rows = row_group.find_elements_by_tag_name('tr')
        return rows
    
    def rowContent(self, tr):
        row_list = tr.find_elements_by_tag_name('td')
        row_content = [td.get_attribute('textContent') for td in row_list]
        return row_content

    def find_issued_stock(self):
        """Navigate to Request Stock Tab, and find stock columns that are issued"""
        self.login()
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Request Stock'))).click()
        time.sleep(5)
        rows = self.getRows(element)
        
        for tr in rows:
            view = tr.find_element_by_tag_name('a')
            view_link =view.get_attribute('href')
            
            row_content = self.rowContent(tr)
            row_content.pop()

