# checker for weis covid site

import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

# sender and recipient details in external file
from emaildetails import emaildetails
# simple email class
from simpleemail import SimpleEmail

# website to check
site = 'https://www.weismarkets.com/pharmacy-services'

# email setup
sender = emaildetails['sender']
pwd = emaildetails['pwd']
recipients = emaildetails['recipients']

# trigger for emailing after many errors
erroremailfrequency = 10

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
<<<<<<< HEAD
        time.sleep(5)  # attempt rate
=======
        time.sleep(400)  # attempt rate
>>>>>>> 5bc86baa44f769924c826afec6ebea6cfeaf6e88
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
            if not errors % erroremailfrequency:
                e = SimpleEmail(sender,
                                    pwd,
                                    recipients,
                                    'Weis Checker Errors',
                                    f'Another {erroremailfrequency} errors have occurred in the Weis site checker: {site}')
                e.send()

        except Exception as e:
            print('Error:', e, 'On attempt:', attempts)
            errors += 1
            if not errors % erroremailfrequency:
                e = SimpleEmail(sender,
                                    pwd,
                                    recipients,
                                    'Weis Checker Errors',
                                    f'Another {erroremailfrequency} errors have occurred in the Weis site checker: {site}')
                e.send()

        except:
            print('Other error on attempt:', attempts)
            errors += 1
            if not errors % erroremailfrequency:
                e = SimpleEmail(sender,
                                    pwd,
                                    recipients,
                                    'Weis Checker Errors',
                                    f'There have been {erroremailfrequency} errors in the Weis site checker: {site}')
                e.send()

        if errors > 50 or reportedchanges > 50:  # limiting run length
            return False


Weischecker(site)
