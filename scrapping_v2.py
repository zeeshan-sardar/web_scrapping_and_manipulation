from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys

options = Options()

options.headless = False

driver = webdriver.Chrome("/usr/bin/chromedriver", options=options)
driver.get("https://www.daft.ie/property-for-rent/ireland?location=dublin-2-dublin&location=dublin-4-dublin&location=dublin-6-dublin&location=dublin-6w-dublin&location=dublin-14-dublin")

username ="m.zeeshan1923@gmail.com"
password = "Zeeshan@123"
message = """Hi,

My name is Zeeshan and I am writing to you in regards to your ad for the accommodation. My wife and I are a young couple working as Researchers at UCD and we are very interested in your property.

A little about us:
- We are non-smokers and non-drinkers.
- We have no children and no pets.
- We do not own a car.
- We can provide Irish references.

We are looking to move in from the mid of June and we are willing to sign a long-term lease if that is what you prefer.

We are both very clean and tidy people and we would take great care of your property. 

We would love to arrange a viewing at your earliest convenience. Please feel free to contact me on my mobile number (+353870572566) or my WhatsApp number (+923216991923) if you have any questions or would like to arrange a viewing.

We look forward to hearing from you soon.

Yours sincerely,

Zeeshan"""

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
                
                
                property_identifier = f"{add} {price} {beds} {baths} {property_type}"
                if property_identifier in sent_emails:
                    print(f"Property '{property_identifier}' has already been processed. Skipping...")
                    continue
                sent_emails.add(property_identifier)
                print(f"Count: {i+1}, Perperty: {property_identifier}")

                driver.find_element(By.XPATH, '//button[@aria-label="Email"]').click()
                time.sleep(3)
                driver.switch_to.window(driver.window_handles[-1])
            
                driver.find_element(By.ID, "keyword1").send_keys("dfds")
                driver.find_element(By.ID, "keyword2").send_keys("dfsdfds@gmail.com")
                driver.find_element(By.ID, "keyword3").send_keys("")
                driver.find_element(By.ID, "message").send_keys('message') 
                driver.find_element(By.XPATH, '//button[@aria-label="Send"]').click()
                
                time.sleep(3)
                try:
                    driver.find_element('//div[@class="Alert__Message-sc-3b1i0x-1 gaOCVC"]')
                    print("Email sent successfully to :", property_identifier)
                except:
                    print("Error while sending Email to :", property_identifier)

                # Close the current tab and switch back to the original tab
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            else:
                print("Element is not enabled and cannot be clicked.")

    time.sleep(60)

    driver.refresh()
    time.sleep(5)


driver.quit()
