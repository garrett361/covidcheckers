# checker for wegman's covid site

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
site = 'https://www.weismarkets.com/pharmacy-services'

# email setup 
sender = emaildetails['sender']
pwd= emaildetails['pwd']
receivers = emaildetails['receivers']
emailbody = """
The Weis covid site changed: https://www.weismarkets.com/pharmacy-services
"""
msg = MIMEText(emailbody, 'html')
msg['Subject'] = 'Change to Weis Covid Site'
msg['From'] = sender
msg['To'] = ','.join(receivers)



def weischecker(urlstring):
    # browser setup
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    # text to find on page
    findstring = 'Appointments Full'
    attempts = 0
    while True:
        time.sleep(60)
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
                print('Website changed! Attempt:', attempts)
                s = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
                s.login(user=sender, password=pwd)
                s.sendmail(sender, receivers, msg.as_string())
                s.quit()
                return False

            driver.close()

        except TimeoutException:  # in case of timeout
            print('Timeout on attempt', attempts)
            
        except:
            print('Other error on attempt', attempts)


weischecker(site)
