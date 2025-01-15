import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set download directory
download_dir = os.path.abspath("./downloads")
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)
# Add headless mode for running without a display
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")  # Recommended for compatibility
chrome_options.add_argument("--no-sandbox")  # Necessary for some servers
chrome_options.add_argument("--disable-dev-shm-usage")  # Prevent crashes in Docker environments

def init_driver():
    """Initialize the WebDriver and WebDriverWait."""
    driver = webdriver.Chrome(options=chrome_options)
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
    select_element, options_text = get_select_options(wait, div_index)
    select_element.find_elements(By.TAG_NAME, "option")[option_index].click()
    return options_text[option_index - 1]

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
