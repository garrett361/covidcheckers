# checker for weis covid site

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
site = 'https://www.weismarkets.com/pharmacy-services'

# email setup
sender = emaildetails['sender']
pwd = emaildetails['pwd']
recipients = emaildetails['recipients']

# trigger for emailing/stoppping after many errors
stoptrigger=50

def Weischecker(urlstring):
    # browser setup
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    # text to find on page
    findstring = 'Please Check Back Later Today'
    # attempts and errors counter
    attempts = 0
    errors = 0
    reportedchanges = 0
    while True:
        time.sleep(500)  # attempt rate
        try:  # loading website and navigating to appropriate page
            driver = webdriver.Chrome(options=options)
            driver.get(urlstring)
            # navigating to the link for shots in PA
            button = driver.find_element_by_xpath(
                '//*[@id="main-content"]/article/div/div/div/div[2]/ul[1]/li[2]/a')
            button.click()
            foundstring = driver.find_element_by_xpath('/html/body/h1').text
            attempts += 1
            if findstring in foundstring:  # checking if the site is still unchanged
                print('No change to weis site. Attempt:', attempts)
            else:  # sending emails if site changes
                print('Website changed! Attempt:', attempts, 'Changes:', reportedchanges)
                # email when site changes
                e = SimpleEmail(sender,
                                    pwd,
                                    recipients,
                                    'Change to Weis Covid Site',
                                    f'The Weis covid site changed: {site}')
                e.send()
                reportedchanges+=1

            driver.close()

        except TimeoutException:  # in case of timeout
            print('Timeout on attempt', attempts)
            errors += 1


        except Exception as e:
            print('Error:', e, 'On attempt:', attempts)
            errors += 1

        if errors > stoptrigger or reportedchanges > stoptrigger:  # limiting run length
            e = SimpleEmail(sender,
                                    pwd,
                                    recipients,
                                    'Weis Checker Stopped',
                                    f'There have been {stoptrigger} errors or changes reported by the Weis Checker. Stopping now. {site}')
            e.send()
            return False


Weischecker(site)
