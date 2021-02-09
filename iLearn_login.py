"""
filename: login.py
abstract: this python script logs a student into their iLearn 
		  account and takes them to their dashboard page by:
		  	1. Start at the iLearn landing page
		  	2. Select the log in option, then go to the log in page
		  	3. Enter and submit the login form, then go to security questionnaire page
		  	4. Enter an submit the security question form, then go to the user dashboard page
miscellaneous:
	In order to use the Chrome browser with Selenium a web driver is required and can be downloaded from:
	https://sites.google.com/a/chromium.org/chromedriver/downloads 
		NOTE: For this script to perform its task the web driver must be place in the same directory as this file
"""
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load environment variables
load_dotenv()

USERNAME = os.getenv("ILEARN_USERNAME")
PASSWORD = os.getenv("ILEARN_PASSWORD")

ANSWER = os.getenv("ILEARN_ANSWER")


# Define web driver options to hide the automation notification
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)

# Navigate to iLearn web page
driver.get("https://ilearn.csumb.edu")

# Navigate to log in page
login_btn = driver.find_element_by_class_name("login").find_element_by_tag_name("a")
login_btn.click()

# Fill out and submit log in form
username_field = driver.find_element_by_id("okta-signin-username")
username_field.click()
username_field.send_keys(USERNAME)

password_field = driver.find_element_by_id("okta-signin-password")
password_field.click()
password_field.send_keys(PASSWORD)

sign_in_button = driver.find_element_by_id("okta-signin-submit")
sign_in_button.click()

# Answer the security question, then go to dashboard page

# The security questionnaire loads slower than other pages (for me),
# so I used explicit waits to gather the elements 

try:
	security_field = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.ID, "input10"))
		)
except:
	print("Could not find input field for security questionnaire on page!")
	driver.quit()

try:
	verify_btn = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.XPATH, "//*[@id='form8']/div[2]/input"))
		)
except:
	print("Could not find submit button for security questionnaire on page!")
	driver.quit()

security_field.click()
security_field.send_keys(ANSWER)

verify_btn.click()