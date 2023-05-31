
import os
import re
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create file object and write header to store property information
file = open('properties.csv', mode='a', newline='')
writer = csv.writer(file)
if os.stat('properties.csv').st_size == 0:
    print('The file is empty, writing header.')
    writer.writerow(['Address', 'Price', 'Beds', 'Baths', 'Type', 'Date', 'Views'])


options = Options()
options.headless = False

driver = webdriver.Chrome("/usr/bin/chromedriver", options=options)
driver.get("https://www.daft.ie/property-for-rent/ireland?location=dublin-2-dublin&location=dublin-4-dublin&location=dublin-6-dublin&location=dublin-6w-dublin&location=dublin-14-dublin&rentalPrice_to=2500&sort=publishDateDesc")
name = "personal name"
username =""
password = ""
message = """ Message """

time.sleep(1)
# Accept cookies
try:
    accept_cookies_button = driver.find_element(By.XPATH, '//button[@onclick="CookieConsent.acceptAll();"]')
    accept_cookies_button.click()
except:
    print("Error, could not accept cookies.")
time.sleep(1)

# Sign into the account
try:
    signin_button = driver.find_element(By.XPATH, '//li[@data-testid="nav-item-signin"]')
    signin_button.click()
except:
    print("Error, could not sign in.")
time.sleep(1)

# Set username and password
driver.find_element(By.ID, "username").send_keys(username)
driver.find_element(By.ID, "password").send_keys(password)
driver.find_element("name", "login").click()
time.sleep(2)



sent_emails = set()
# Setup wait for later
wait = WebDriverWait(driver, 10)



while True:

    # Find the non-agency ad cards 
    title_blocks = driver.find_elements(By.XPATH, '//li[@class="SearchPage__Result-gg133s-2 djuMQD"]')
    print("Length of title blocks: ", len(title_blocks))

    # Store the ID of the original window
    original_window = driver.current_window_handle

    # Check we don't have other windows open already
    assert len(driver.window_handles) == 1

    # for count, title_block in enumerate(title_blocks):
    for i in range(len(title_blocks)):
        
        print("Loop Count: ", i+1)
        title_block = title_blocks[i]
        
        try:
            title_block.find_element(By.XPATH, './a/div[@data-testid="agent-branding-top"]')
            print("Agent Branding Found")
        except:

            if title_block.is_enabled():
                time.sleep(3)

                try:
                    # Navigate to the property ad
                    link = title_block.find_element(By.XPATH, './a')
                    href = link.get_attribute('href')
                except: 
                    print("Link not found..!")

                print("link: ", href)

                # Open a new tab
                driver.execute_script("window.open('about:blank', '_blank');")
                # Switch to the new tab
                driver.switch_to.window(driver.window_handles[-1])
                # Open link in new tab
                driver.get(href)
                
                time.sleep(3)
                
                # Find property information
                property_info = driver.find_element(By.XPATH, '//div[@data-testid="title-block"]')
                # Find property stats
                property_stats = driver.find_element(By.XPATH, '//div[@class="Statistics__MainContainer-sc-15tgae4-4 gNBtdx"]')
                try:
                    add = property_info.find_element(By.XPATH, '//h1[@data-testid="address"]').text
                except:
                    add = ""
                try:
                    price = "- " + property_info.find_element(By.XPATH, './div[1][@data-testid="price"]').text
                except:
                    price = ""
                try:
                    beds = "- " + property_info.find_element(By.XPATH, './div[2]/p[1]').text
                except:
                    beds = ""
                try:
                    baths = "- " + property_info.find_element(By.XPATH, './div[2]/p[2]').text
                except:
                    baths = ""
                try:
                    property_type = "- " + property_info.find_element(By.XPATH, './div[2]/p[3]').text
                except:
                    property_type = ""
                try:
                    date = "- " + property_stats.find_element(By.XPATH, './div[1]/div/p').text
                except:
                    date = ""
                try:
                    views = "- " + property_stats.find_element(By.XPATH, './div[2]/div/p').text
                except:
                    views = ""

                if int(''.join(re.findall(r'\d+', price))) > 1900 and int(re.findall(r'\d+', beds)[0]) < 2:
                    print("Skipping property due to High price.")
                    # Close the current tab and switch back to the original tab
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    continue

                property_identifier = f"{add} {price} {beds} {baths} {property_type} {date} {views}"
                if property_identifier in sent_emails:
                    print(f"Property '{property_identifier}' has already been processed. Skipping...")
                    # Close the current tab and switch back to the original tab
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    continue
                

                sent_emails.add(property_identifier)
                print(f"Count: {i+1}, Perperty: {property_identifier}")

                # Click on email button and switch to the form window
                driver.find_element(By.XPATH, '//button[@aria-label="Email"]').click()
                time.sleep(3)
                driver.switch_to.window(driver.window_handles[-1])

                try:
                    driver.find_element(By.XPATH, '//span[@class="IconWithContentAndLabel__StyledIconWithContent-sc-1pv1vxd-2 czNtBM"]')
                    print("Already Applied, skipping...")
                    # Close the current tab and switch back to the original tab
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    continue
                except:
                    print("Did not apply before")
            
                # Fill up the form to send to the advertiser
                driver.find_element(By.ID, "keyword1").send_keys(name) # Name
                driver.find_element(By.ID, "keyword2").send_keys(username) # Email
                driver.find_element(By.ID, "keyword3").send_keys("") # Phone Number
                driver.find_element(By.ID, "message").send_keys(message) # Message
                
                try:
                    driver.find_element(By.XPATH, '//button[@aria-label="Send"]').click()
                    print("Email sent successfully to.")
                    time.sleep(3)
                except:
                    print("Error while sending Email to :", property_identifier)

                # writer.writerow([add, price, beds, baths, property_type, date, views])
                # Close the current tab and switch back to the original tab
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            else:
                print("Element is not enabled and cannot be clicked.")

    time.sleep(10)

    driver.refresh()
    time.sleep(5)


driver.quit()
