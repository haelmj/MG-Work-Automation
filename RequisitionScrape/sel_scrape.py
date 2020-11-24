from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import csv
import time

PATH = "C:/Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get('https://mcndealers.com/users/sign_in')
stock_window = driver.window_handles[0]
LOGIN_NAME = os.environ.get('MCN_USERNAME')
LOGIN_PW = os.environ.get('MCN_PASS')
FOLDER = 'C:/projects/webscraping/Requisitions'

def login():
    username = driver.find_element_by_id('login_name')
    username.clear()
    username.send_keys(LOGIN_NAME)

    password = driver.find_element_by_id('login_pw')
    password.clear()
    password.send_keys(LOGIN_PW)

    enter = driver.find_element_by_name('login_btn')
    enter.send_keys(Keys.RETURN)
    return

def getColumnNames(id):
    element = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.ID, id))
            )
    columns = element.find_elements_by_tag_name('th')
    column_name = [th.get_attribute('textContent') for th in columns]
    return element, column_name

def getRows(element):
    row_group = element.find_element_by_tag_name('tbody')
    rows = row_group.find_elements_by_tag_name('tr')
    return rows

def rowContent(tr):
    row_list = tr.find_elements_by_tag_name('td')
    row_content = [td.get_attribute('textContent') for td in row_list]
    return row_content

try:
    login()
    
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'Stock Requisitions'))
    ).click()
    time.sleep(5)

    with open('mcn_scrape.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        element, column_name = getColumnNames('DataTables_Table_0') 
        csv_writer.writerow(column_name)
        rows = getRows(element)
        
        for tr in rows:
            view = tr.find_element_by_tag_name('a')
            view_link =view.get_attribute('href')
            
            row_content = rowContent(tr)
            row_content.pop()
            r_id = row_content[0]
            row_content.append(f'=HYPERLINK("{FOLDER}/{r_id}.csv",  "view")')
            if row_content[2] == 'Received':
                csv_writer.writerow(row_content)
                
                driver.execute_script(f"window.open('{view_link}')")
                view_window = driver.window_handles[1]
                driver.switch_to_window(view_window)
                
                with open(f'Requisitions/{r_id}.csv', 'w', newline='', encoding='utf-8') as r_file:
                    r_writer = csv.writer(r_file)
                    element, column_name = getColumnNames('content')
                    r_writer.writerow(column_name)
                    
                    r_rows = getRows(element)
                    for t in r_rows:
                        content = rowContent(t)
                        r_writer.writerow(content)
                
                driver.close()
                driver.switch_to_window(stock_window)
                time.sleep(5)    

            
            
except Exception as e:
    print(e)
    driver.close()
finally:
    driver.close()