# Importing the required Modules
import random
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import re
import csv
# Note: With the help of selenium we are importing web drivers. We have used Chrome web driver
browser = webdriver.Chrome('Your_path_location_to_chrome_web_driver/chromedriver.exe')
# Getting the linkedin Sign in page
browser.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
browser.maximize_window()

# Enter login info
elementID = browser.find_element_by_id('username')
elementID.send_keys('Your_EmailId')

elementID = browser.find_element_by_id('password')
elementID.send_keys('Your_Password')
# Note: replace the keys "username" and "password" with your LinkedIn login info

# Note: submit() behaves like enter button of keyboard
elementID.submit()

row = browser.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')

total_height = browser.execute_script("return document.documentElement.scrollHeight")
while True:
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(random.uniform(2.5, 4.9))
    # Calculate new scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    break

page = bs(browser.page_source, features="html.parser")
content = page.find_all('a', {'class': "mn-connection-card__link ember-view"})
# To get all connections and then to access them we are keeping that in a List
my_network = []
for contact in content:
    my_network.append(contact.get('href'))
print("Total connections:", len(my_network))
my_network_details = []
k = 1
# Looping through linkedin connections
for i in my_network:
    print('Connection', k, ':', end=' ')
    k += 1
    a = 'https://www.linkedin.com' + i + 'detail/contact-info/'
    print(i[4:-1])

    # Handling exception if any
    try:
        row = browser.get(a)
        # Using beautiful soup to parse in linkedin webpage
        page = bs(browser.page_source, features="html.parser")
        # Through inspect we got our class name and with the help of Regular Expression we are compiling it
        matches = page.find_all('a', class_=re.compile("pv-contact-info__contact-link"))
        # Details are printed out
        for contact in matches:
            if 'linkedin' in contact.get('href')[:]:
                print('Profile:', contact.get('href')[:])
            elif '@' in contact.get('href')[:]:
                print('Email:', contact.get('href')[:])
            elif 'twitter' in contact.get('href')[:]:
                print('Twitter:', contact.get('href')[:])
            elif 'maps' in contact.get('href')[:]:
                print('Address:', contact.get('href')[:])
            else:
                print('Website:', contact.get('href')[:])
            my_network_details.append(contact.get('href')[:])
        print()

    except Exception as e:
        print("Oops!", e, "occurred.")

# Getting our LinkedIn details in a csv file
with open(f'my_network_details.csv', 'w', encoding="utf-8") as f:
    writer = csv.writer(f)
    for details in my_network_details:
        writer.writerow([details])
print('Completed')
