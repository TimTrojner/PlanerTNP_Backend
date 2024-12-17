from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os

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
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")  # Recommended for compatibility
chrome_options.add_argument("--no-sandbox")  # Necessary for some servers
chrome_options.add_argument("--disable-dev-shm-usage")  # Prevent crashes in Docker environments

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)


try:
    # 1. Open the website
    url = "https://www.wise-tt.com/wtt_um_feri/"  # Replace with your website URL
    driver.get(url)
    
    # Wait for the page to load
    wait = WebDriverWait(driver, 10)
    
    # Program
    ## 2. Click the button with ID "form:j_idt175" 
    button1 = wait.until(EC.element_to_be_clickable((By.ID, "form:j_idt175")))
    button1.click()
    print("Clicked button for selecting school program")
    time.sleep(2)  # Wait for dropdown to load
    
    # 3. Show contents of the <ul> with ID "form:j_idt175_items" in the console
    ul_element = wait.until(EC.presence_of_element_located((By.ID, "form:j_idt175_items")))
    ul_items = ul_element.find_elements(By.TAG_NAME, "li")
    
    print("\nContents of the <ul> element:")
    for index, item in enumerate(ul_items):
        if index == 0: continue
        print(f"{index}. {item.text}")

    # 4. Prompt the user to choose an index
    while True:
      try:
        target_index = int(input("\nEnter the number corresponding to your desired option: "))
        if 1 <= target_index <= len(ul_items):
          break
        else:
          print(f"Please enter a number between 1 and {len(ul_items)}")
      except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Click the selected item
    ul_items[target_index].click()
    print(f"Clicked on item {target_index}: {ul_items[target_index - 1].text}")
    time.sleep(1)
    ###### program selected ##########

    # year
    button1 = wait.until(EC.element_to_be_clickable((By.ID, "form:j_idt179")))
    button1.click()
    print("Clicked button year select")
    time.sleep(2)  # Wait for dropdown to load
    
    ul_element = wait.until(EC.presence_of_element_located((By.ID, "form:j_idt179_items")))
    ul_items = ul_element.find_elements(By.TAG_NAME, "li")
    
    print("\nContents of the <ul> element:")
    for index, item in enumerate(ul_items):
        if index == 0: continue
        print(f"{index}. {item.text}")

    # 4. Prompt the user to choose an index
    while True:
      try:
        target_index = int(input("\nEnter the number corresponding to your desired option: "))
        if 1 <= target_index <= len(ul_items):
          break
        else:
          print(f"Please enter a number between 1 and {len(ul_items)}")
      except ValueError:
            print("Invalid input. Please enter a number.")

    # Click the selected item
    ul_items[target_index].click()
    print(f"Clicked on item {target_index}: {ul_items[target_index - 1].text}")
    time.sleep(1)
    ###### year selected #########

    # orientation
    button1 = wait.until(EC.element_to_be_clickable((By.ID, "form:j_idt183")))
    button1.click()
    print("Clicked button orientation select")
    time.sleep(2)  # Wait for dropdown to load
    
    ul_element = wait.until(EC.presence_of_element_located((By.ID, "form:j_idt183_items")))
    ul_items = ul_element.find_elements(By.TAG_NAME, "li")
    
    print("\nContents of the <ul> element:")
    for index, item in enumerate(ul_items):
        if index == 0: continue
        print(f"{index}. {item.text}")

    # 4. Prompt the user to choose an index
    while True:
      try:
        target_index = int(input("\nEnter the number corresponding to your desired option: "))
        if 1 <= target_index <= len(ul_items):
          break
        else:
          print(f"Please enter a number between 1 and {len(ul_items)}")
      except ValueError:
            print("Invalid input. Please enter a number.")

    # Click the selected item
    ul_items[target_index].click()
    print(f"Clicked on item {target_index}: {ul_items[target_index - 1].text}")
    time.sleep(1)
    ###### orientation selected #########

    # 5. Click the button with ID "form:j_idt255"
    button2 = wait.until(EC.element_to_be_clickable((By.ID, "form:j_idt255")))
    button2.click()
    print("Clicked button with ID: form:j_idt255")
    time.sleep(1)
    
    # 6. Click the button with ID "reporstForm:j_idt763"
    button3 = wait.until(EC.element_to_be_clickable((By.ID, "reporstForm:j_idt763")))
    button3.click()
    print("Clicked button with ID: reporstForm:j_idt763")

    # Wait for the download to complete by checking the download folder
    print("Waiting for the file to download...")
    time.sleep(5)  # Adjust based on file size and network speed

    # Verify the file has been downloaded
    downloaded_files = os.listdir(download_dir)
    print("Downloaded files:", downloaded_files)
    
finally:
    # Close the browser
    driver.quit()
