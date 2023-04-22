import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Replace these with your LinkedIn credentials
EMAIL = ""
PASSWORD = ""

# Set the path to the ChromeDriver executable
CHROME_DRIVER_PATH = "/opt/homebrew/bin/chromedriver"

# Define the search URL
SEARCH_URL = ""

def login(driver):
    driver.get("https://www.linkedin.com/login")

    email_input = driver.find_element_by_name("session_key")
    email_input.send_keys(EMAIL)
    password_input = driver.find_element_by_name("session_password")
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)

def search_and_send_requests(driver):
    page = 1

    while True:
        # Navigate to the search page with the people filter applied
        driver.get(f"{SEARCH_URL}&page={page}")

        # Wait for the search results to load
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "search-results-container")))
        except TimeoutException:
            print("No more pages found.")
            break

        # Locate the "Connect" buttons in the search results
        connect_buttons = driver.find_elements_by_xpath("//button[contains(@aria-label, 'to connect')]")

        # Send connection requests to the search results
        for connect_button in connect_buttons:
            try:
                connect_button.click()

                # Wait for the "Add a note" dialog to appear
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Send now']")))

                # Click the "Send now" button
                send_now_button = driver.find_element_by_xpath("//button[@aria-label='Send now']")
                send_now_button.click()

                time.sleep(5)  # Add a delay between requests to avoid overwhelming the website
            except Exception as e:
                print(f"Error sending request: {e}")
                continue

        # Locate the "Follow" buttons in the search results
        follow_buttons = driver.find_elements_by_xpath("//button[contains(@aria-label, 'Follow')]")

        # Follow people in the search results
        for follow_button in follow_buttons:
            try:
                follow_button.click()
                time.sleep(5)  # Add a delay between requests to avoid overwhelming the website
            except Exception as e:
                print(f"Error following: {e}")
                continue

        page += 1

    driver.quit()

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

# Log in to LinkedIn
login(driver)

# Wait for the homepage to load
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Search']")))

# Search for people and send connection requests
search_and_send_requests(driver)
