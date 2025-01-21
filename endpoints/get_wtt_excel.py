import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

# Set the download directory
download_dir = os.path.abspath("./downloads")  # Define the download directory
os.makedirs(download_dir, exist_ok=True)  # Ensure the directory exists

# Set download directory
firefox_profile_path = webdriver.FirefoxProfile()
firefox_profile_path.set_preference("browser.download.folderList", 2)  # Use custom download directory
firefox_profile_path.set_preference("browser.download.dir", download_dir)
firefox_profile_path.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.ms-excel")
firefox_profile_path.set_preference("browser.download.manager.showWhenStarting", False)

# gecko_service = Service("/usr/bin/geckodriver")
gecko_service = Service("/Users/timtr/geckodriver")

# Configure Firefox options
firefox_options = Options()
firefox_options.profile = firefox_profile_path  # Assign profile to options
# firefox_options.add_argument("--headless")
# firefox_options.add_argument("--disable-gpu")
# firefox_options.add_argument("--no-sandbox")

def init_driver():
    """Initialize the WebDriver and WebDriverWait."""
    driver = webdriver.Firefox(service=gecko_service, options=firefox_options)
    wait = WebDriverWait(driver, 10)
    return driver, wait

def get_select_options(wait, div_index):
    """Retrieve options from a <select> element inside a specified div."""
    div_elements = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "div.ui-selectonemenu.ui-widget.ui-state-default.ui-corner-all")
    ))
    target_div = div_elements[div_index]
    select_element = target_div.find_element(By.TAG_NAME, "select")
    options = select_element.find_elements(By.TAG_NAME, "option")
    options_text = [option.text for option in options]
    options_text.pop(0)
    return select_element, options_text

def select_option(wait, div_index, option_index):
    """Select an option by index."""
    div_elements = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "div.ui-selectonemenu.ui-widget.ui-state-default.ui-corner-all")
    ))
    
    dropdown_element = div_elements[div_index]
    dropdown_element.click()
    
    ul_elements = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "ul.ui-selectonemenu-items.ui-selectonemenu-list.ui-widget-content.ui-widget.ui-corner-all.ui-helper-reset")
    ))
    
    li_items = ul_elements[2].find_elements(By.TAG_NAME, "li")
    
    option_element = li_items[option_index]
    option_element.click()

    return option_element.text

def download_excel(driver, wait, program_index, year_index, module_index):
    """Select program, year, module and download the Excel file."""
    # Open the website
    url = "https://www.wise-tt.com/wtt_um_feri/"
    driver.get(url)

    # Select options
    select_option(wait, div_index=2, option_index=program_index)
    old_content = driver.find_element(By.CSS_SELECTOR, "tbody").get_attribute("innerHTML")
    wait.until(lambda driver: driver.find_element(By.CSS_SELECTOR, "tbody").get_attribute("innerHTML") != old_content)
    select_option(wait, div_index=3, option_index=year_index)
    old_content = driver.find_element(By.CSS_SELECTOR, "tbody").get_attribute("innerHTML")
    wait.until(lambda driver: driver.find_element(By.CSS_SELECTOR, "tbody").get_attribute("innerHTML") != old_content)
    select_option(wait, div_index=4, option_index=module_index)

    # Click download buttons
    buttons = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "button.ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")
    ))
    buttons[0].click()
    time.sleep(1)
    buttons = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "button.ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")
    ))
    buttons[12].click()

    # Wait for download
    time.sleep(2)
    downloaded_files = os.listdir(download_dir)
    return downloaded_files
