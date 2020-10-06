from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import csv

PATH = "C:/Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get('https://mcndealers.com/users/sign_in')
LOGIN_NAME = os.environ.get('MCN_USERNAME')
LOGIN_PW = os.environ.get('MCN_PASS')

try:
    username = driver.find_element_by_id('login_name')
    username.clear()
    username.send_keys(LOGIN_NAME)

    password = driver.find_element_by_id('login_pw')
    password.clear()
    password.send_keys(LOGIN_PW)

    enter = driver.find_element_by_name('login_btn')
    enter.send_keys(Keys.RETURN)
    
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'Stock Requisitions'))
    )
    element.click()

    element = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, 'DataTables_Table_0'))
    )
    columns = element.find_elements_by_tag_name('th')
    
    with open('mcn_scrape.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        column_name = [th.get_attribute('aria-label').split(':')[0] for th in columns]
        csv_writer.writerow(column_name)
        
        row_group = element.find_element_by_tag_name('tbody')
        rows = row_group.find_elements_by_tag_name('tr')
        for tr in rows:
            row_content = tr.find_elements_by_tag_name('td')
            row_list = [td.get_attribute('textContent') for td in row_content]
            csv_writer.writerow(row_list)
            
except Exception as e:
    print(e)
    # driver.close()
finally:
    driver.close()