from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import logging
import os
import subprocess
from datetime import datetime
import pytz
import requests  # Added for ntfy notifications

# Set up logging to only show ERROR level messages
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# ntfy topic for push notifications (replace with your unique topic)
NTFY_TOPIC = "appointment-alerts"  # Customize this

def send_ntfy_notification(message):
    """Send a push notification via ntfy."""
    try:
        response = requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=message.encode("utf-8"),
            headers={"Title": "New Appointment Slots Available"}
        )
        if response.status_code == 200:
            return True
        else:
            logging.error(f"Failed to send ntfy notification: {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"Error sending ntfy notification: {str(e)}")
        return False

def scrape_appointments():
    # Primary path to ChromeDriver (direct executable path for ARM Mac)
    chromedriver_path = "/opt/homebrew/Caskroom/chromedriver/138.0.7204.92/chromedriver-mac-arm64/chromedriver"

    # Fallback to find ChromeDriver in PATH if the primary path doesn't exist
    if not os.path.exists(chromedriver_path):
        try:
            chromedriver_path = subprocess.check_output(["which", "chromedriver"]).decode().strip()
        except subprocess.CalledProcessError:
            logging.error("ChromeDriver not found in PATH. Please install ChromeDriver.")
            return

    # Verify ChromeDriver is not a directory
    if os.path.isdir(chromedriver_path):
        logging.error(f"{chromedriver_path} is a directory, not an executable. Please replace with the ChromeDriver executable.")
        return

    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-images")
    chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

    # Initialize ChromeDriver
    try:
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {str(e)}")
        return

    try:
        # Step 1: Navigate to the default page
        driver.get("https://bmvs.onlineappointmentscheduling.net.au/oasis/Default.aspx")
        time.sleep(5)  # Initial delay for page load

        # Click the "New Individual booking" button
        booking_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_btnInd"))
        )
        booking_button.click()
        time.sleep(5)  # Wait for navigation to location page

        # Step 2: Proceed with location page
        try:
            # Try ID-based selector first
            location_input = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_SelectLocation1_txtSuburb"))
            )
        except Exception as e:
            # Fallback to XPath selector
            location_input = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'txtSuburb')]"))
            )

        # Enter postcode 5000
        location_input.clear()
        location_input.send_keys("5000")

        # Click the search button
        search_button = driver.find_element(By.XPATH, "//input[@value='Search' and @class='blue-button']")
        driver.execute_script("SearchPostCode();")
        time.sleep(2)  # Wait for JavaScript to execute

        # Wait for the results table to load
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "trlocation"))
        )

        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = []

        # Find all location rows
        location_rows = soup.find_all('tr', class_='trlocation')

        for row in location_rows:
            # Get distance
            distance_cell = row.find('td', class_='td-distance')
            if distance_cell:
                distance_text = distance_cell.find('span').text.strip()
                try:
                    distance = int(distance_text.split()[0])  # Extract number from "X km"
                except ValueError:
                    continue

                # Check if distance is less than 50km
                if distance < 50:
                    # Check availability
                    availability_cell = row.find('td', class_='tdloc_availability')
                    availability = availability_cell.find('span').text.strip()

                    # Only include if slot is available
                    if availability != "No available slot":
                        # Get location name and address
                        name_cell = row.find('td', class_='tdloc_name')
                        location_name = name_cell.find('label', class_='tdlocNameTitle').text.strip()
                        address = name_cell.find('span').text.strip()

                        results.append({
                            'location': location_name,
                            'address': address,
                            'distance': distance_text,
                            'availability': availability
                        })

        # Print results and send notifications
        if results:
            acst = pytz.timezone('Australia/Adelaide')
            timestamp = datetime.now(acst).strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
            print(f"{timestamp} - INFO - Found available appointments")
            notification_message = f"Found available appointments at {timestamp}:\n"
            for result in results:
                print(f"Location: {result['location']}")
                print(f"Address: {result['address']}")
                print(f"Distance: {result['distance']}")
                print(f"Availability: {result['availability']}")
                print("-" * 50)
                # Add to notification message
                notification_message += (
                    f"Location: {result['location']}\n"
                    f"Address: {result['address']}\n"
                    f"Distance: {result['distance']}\n"
                    f"Availability: {result['availability']}\n"
                    f"{'-' * 50}\n"
                )
            # Send push notification
            send_ntfy_notification(notification_message)

    except Exception as e:
        logging.error(f"An error occurred during execution: {str(e)}")
        # Save page source for debugging
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_appointments()
