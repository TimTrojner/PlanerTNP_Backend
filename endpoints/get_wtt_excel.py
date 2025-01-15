from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os

def get_select_options(wait, div_index):
    """
    Retrieve options from a <select> element inside a specified div.

    Parameters:
        wait: WebDriverWait instance
        div_index: Index of the div element containing the <select>

    Returns:
        A tuple containing the <select> element and a list of option texts.
    """
    # Locate all matching div elements
    div_elements = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "div.ui-selectonemenu.ui-widget.ui-state-default.ui-corner-all")
    ))

    # Get the specified div
    target_div = div_elements[div_index]

    # Find the <select> element within the div
    select_element = target_div.find_element(By.TAG_NAME, "select")

    # Retrieve all <option> tags within the <select>
    options = select_element.find_elements(By.TAG_NAME, "option")

    # Extract and return the text of all options
    options_text = [option.text for option in options]
    options_text.pop(0)
    return select_element, options_text


def select_select_option(wait, div_index, option_index):
    """
    Select an option by index from a <select> element inside a specified div.

    Parameters:
        wait: WebDriverWait instance
        div_index: Index of the div element containing the <select>
        option_index: Index of the desired option (0-based)

    Returns:
        The text of the selected option.
    """
    # Get the <select> element and its options
    select_element, options_text = get_select_options(wait, div_index)

    # Validate the option index
    if 0 <= option_index < len(options_text) + 1:
        # Click the desired option
        select_element.find_elements(By.TAG_NAME, "option")[option_index].click()
        return options_text[option_index - 1]
    else:
        raise ValueError(f"Index out of range. Please provide a number between 0 and {len(options_text) - 1}.")


def download_exel():
    # Download exel
    span_elements = wait.until(EC.presence_of_all_elements_located(
      (By.CSS_SELECTOR, "button.ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")
    ))
    span_elements[0].click()
    time.sleep(1)

    span_elements = wait.until(EC.presence_of_all_elements_located(
      (By.CSS_SELECTOR, "button.ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")
    ))

    span_elements[12].click()

    # Wait for the download to complete by checking the download folder
    print("Waiting for the file to download...")
    time.sleep(2)  # Adjust based on file size and network speed

    # Verify the file has been downloaded
    downloaded_files = os.listdir(download_dir)
    print("Downloaded files:", downloaded_files)



download_dir = os.path.abspath("../downloads")
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)
# Add headless mode for running without a display
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")  # Recommended for compatibility
chrome_options.add_argument("--no-sandbox")  # Necessary for some servers
chrome_options.add_argument("--disable-dev-shm-usage")  # Prevent crashes in Docker environments
# Initialize the WebDriver
print("Initializing driver")
driver = webdriver.Chrome(options=chrome_options)
print("Initializing complete")


try:
    # 1. Open the website
    url = "https://www.wise-tt.com/wtt_um_feri/"  # Replace with your website URL
    driver.get(url)
    
    # Wait for the page to load
    wait = WebDriverWait(driver, 5)

    # get and select program
    _, options = get_select_options(wait, div_index=2)
    print("Options in the selected div's <select>:")
    for index, option in enumerate(options):
        print(f"{index + 1}. {option}")
    # Select an option by index
    selected_text = select_select_option(wait, div_index=2, option_index=15)
    print(f"You selected: {selected_text}")

    time.sleep(1)
    
    
    # get and select year
    _, options = get_select_options(wait, div_index=3)
    print("Options in the selected div's <select>:")
    for index, option in enumerate(options):
        print(f"{index + 1}. {option}")
    # Select an option by index
    selected_text = select_select_option(wait, div_index=3, option_index=1)
    print(f"You selected: {selected_text}")

    time.sleep(1)

    # get and select module
    _, options = get_select_options(wait, div_index=4)
    print("Options in the selected div's <select>:")
    for index, option in enumerate(options):
        print(f"{index + 1}. {option}")
    # Select an option by index
    selected_text = select_select_option(wait, div_index=4, option_index=1)
    print(f"You selected: {selected_text}")
    
    download_exel()
    
finally:
    # Close the browser
    driver.quit()


