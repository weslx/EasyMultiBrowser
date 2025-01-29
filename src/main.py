import os
import random
import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

PREDEFINED_URLS = ["https://www.youtube.com", "https://github.com/weslx"]
NUM_BROWSERS = 3

def ask_profile():
    while True:
        profile = input("Select profile: ").strip()
        if profile:
            return profile
        print("Profile name cannot be empty!")

def human_interaction(driver):
    try:
        action = ActionChains(driver)
        for _ in range(random.randint(2, 5)):
            action.move_by_offset(
                random.randint(-10, 10),
                random.randint(-10, 10)
            ).perform()
            time.sleep(random.uniform(0.1, 0.3))
        
        scroll_amount = random.randint(200, 800)
        driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
        time.sleep(random.uniform(0.5, 1.5))
        
    except Exception as e:
        pass

def create_driver(profile, instance_id, drivers):
    profile_path = os.path.abspath(f'profiles/{profile}/instance_{instance_id}')
    os.makedirs(profile_path, exist_ok=True)

    options = webdriver.ChromeOptions()
    

    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument(f"--profile-directory=Profile_{instance_id}")
    

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--mute-audio")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=pt-BR")
    

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")
    
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        

        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['pt-BR', 'pt', 'en-US', 'en']});
            window.chrome = {runtime: {}};
            """
        })

        for index, url in enumerate(PREDEFINED_URLS):
            if index == 0:
                driver.get(url)
            else:
                driver.switch_to.new_window('tab')
                driver.get(url)
            time.sleep(random.uniform(1, 3))
            human_interaction(driver)

        drivers.append(driver)

    except Exception as e:
        print(f"Error creating browser: {e}")
        if 'driver' in locals():
            driver.quit()

def manage_profile(profile):
    drivers = []
    threads = []

    for i in range(1, NUM_BROWSERS + 1):
        t = threading.Thread(target=create_driver, args=(profile, i, drivers))
        threads.append(t)
        t.start()
        time.sleep(1)

    for t in threads:
        t.join()

    input("\nPress Enter to close browsers...")
    for driver in drivers:
        try:
            driver.quit()
        except:
            pass

def main():
    profile = ask_profile()
    manage_profile(profile)

if __name__ == "__main__":
    main()