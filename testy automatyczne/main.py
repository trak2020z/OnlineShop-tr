from selenium import webdriver
from selenium.webdriver.common.keys import Keys

URL = 'http://127.0.0.1:8000/accounts/login/'

name = 'admin'
passw = 'admin'

def login(username, password):
    driver = webdriver.Firefox(
        executable_path='drivers/geckodriver.exe')
    driver.get(URL)

    login = driver.find_element_by_id('id_username')
    password = driver.find_element_by_id('id_password')

    login.send_keys(username)
    password.send_keys(password)
    password.send_keys(Keys.RETURN)
    
    assert 'http://127.0.0.1:8000' in driver.current_url


login(name, passw)