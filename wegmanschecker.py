# checker for wegman's covid site

# CURRENTLY BROKEN DUE TO WEBSITE CHANGESs

import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

# sender, pwd, and recipient details in external file
from emaildetails import emaildetails
# simple email class
from simpleemail import SimpleEmail

# website to check
site = 'https://www.wegmans.com/covid-vaccine-registration/'

# email setup
sender = emaildetails['sender']
pwd = emaildetails['pwd']
recipients = emaildetails['recipients']

# trigger for emailing after many errors
stoptrigger = 50


def Wegmanschecker(urlstring):
    # set up browswer
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    # string to find on target website
    findstring = 'All available vaccine appointments are reserved at this time. Please check back later for available timeslots.'
    # attempts and errors counter
    attempts = 0
    errors = 0
    reportedchanges = 0
    while True:
        time.sleep(500)  # attempt rate
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
            print(foundstring)
            attempts += 1
            if findstring in foundstring:  # checking if the site is still unchanged
                print('No change to wegmans site. Attempt:', attempts)
            else:  # sending emails if site changes
                print('Website changed! Attempt:',
                      attempts, 'Changes:', reportedchanges)
                # email when site changes
                e = SimpleEmail(sender,
                                pwd,
                                recipients,
                                'Change to Wegman\'s Covid Site',
                                f'The Wegman\'s covid site changed: {site}')
                e.send()
                reportedchanges += 1

            driver.close()

        except TimeoutException:  # in case of timeout
            print('Timeout on attempt', attempts)
            errors += 1
            if not errors % stoptrigger:
                e = SimpleEmail(sender,
                                pwd,
                                recipients,
                                'Wegman\'s Checker Errors',
                                f'Another {stoptrigger} errors have occurred in the Wegman\'s site checker: {site}')
                e.send()

        except Exception as e:
            print('Error:', e, 'On attempt:', attempts)
            errors += 1

        if errors > stoptrigger or reportedchanges > stoptrigger:  # limiting run length
            e = SimpleEmail(sender,
                            pwd,
                            recipients,
                            'Wegman\'s Checker Stopped',
                            f'There have been {stoptrigger} errors or changes reported by the Wegman\'s Checker. Stopping now. {site}')
            e.send()
            return False


Wegmanschecker(site)
