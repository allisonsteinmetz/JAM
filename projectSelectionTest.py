from selenium import webdriver
from selenium.webdriver.common.keys import Keys

real_user = 'juicearific'
real_pass = 'demopw123'

browser = webdriver.Chrome("/Users/allisonsteinmetz/Downloads/chromedriver")

browser.get('http://localhost:5000/')

username = browser.find_element_by_name('username')  # Find the username box
username.send_keys(real_user)
password = browser.find_element_by_name('pwd') # Find the password box
password.send_keys(real_pass + Keys.RETURN)

searchbar = browser.find_element_by_name('searchKey')
searchbar.send_keys('allisonsteinmetz/JAM')
browser.find_element_by_id('searchButton').click()

browser.implicitly_wait(20)
elem = browser.find_element_by_id('allisonsteinmetz/JAM')
elem.click()
