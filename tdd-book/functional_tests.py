from selenium import webdriver

# First functional test

"""
	1. set the browser to open the chrome driver given the executable's PATH
	2. open the browser to the local server url
	3. check if 'Django' is in the browser title
"""
browser = webdriver.Chrome('/Users/justindodson/Desktop/WebDevelopment/obeyTheTestingGoat/tdd-book/chromedriver')
browser.get('http://localhost:8000')

assert 'Django' in browser.title