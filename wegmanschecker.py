# Checks whether wegman's covid site's website has changed

import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import smtplib
import ssl
from email.mime.text import MIMEText
# sender and recipient details in external file
from covidemails import emaildetails

# website to check
site = 'https://www.wegmans.com/covid-vaccine-registration/'

# email setup
sender = emaildetails['sender']
pwd = emaildetails['pwd']
receivers = emaildetails['receivers']
emailbody = """
The Wegman\'s covid site changed: https://www.wegmans.com/covid-vaccine-registration/
"""
msg = MIMEText(emailbody, 'html')
msg['Subject'] = 'Change to Wegman\'s Covid Site'
msg['From'] = sender
msg['To'] = ','.join(receivers)


def wegmanschecker(urlstring):
    # set up browswer
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    # string to find on target website
    findstring = 'All available vaccine appointments are reserved at this time. Please check back later for available timeslots.'
    # attempt counter
    attempts = 0
    while True:
        time.sleep(500) # attempt rate
        try:  # loading website and navigating to appropriate iframe
            driver = webdriver.Chrome(options=options)
            driver.get(urlstring)
            # waits up to 1 minute before timeout, needed to get iframe to load
            wait = WebDriverWait(driver, 60)
            wait.until(ec.visibility_of_element_located(
                (By.TAG_NAME, 'iframe')))
            driver.switch_to.frame(0)
            wait.until(ec.visibility_of_element_located(
                (By.CLASS_NAME, 'message_content')))
            # sleep needed for find_element_by_class_name below to return a non-blank str. Not sure why; timing issue
            time.sleep(1)
            foundstring = driver.find_element_by_class_name(
                'message_content').text
            attempts += 1
            if findstring in foundstring:  # checking if the site is still unchanged
                print('No change to wegmans site. Attempt:', attempts)
            else:  # sending emails if site changes
                print('Website changed! Attempt:', attempts)
                s = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
                s.login(user=sender, password=pwd)
                s.sendmail(sender, receivers, msg.as_string())
                s.quit()
                return False  # stop if changed

            driver.close()

        except TimeoutException:  # in case of timeout
            print('Timeout on attempt', attempts)
            
        except:
            print('Other error on attempt', attempts)


wegmanschecker(site)
