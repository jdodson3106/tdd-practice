from selenium import webdriver

browser = webdriver.Chrome('/Users/justindodson/Desktop/WebDevelopment/obeyTheTestingGoat/tdd-book/chromedriver')
browser.get('http://localhost:8000')

assert 'Django' in browser.title