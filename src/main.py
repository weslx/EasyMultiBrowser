import os
import random
import time
import threading
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc  # use undetected chromedriver
from selenium_stealth import stealth

PREDEFINED_URLS = ["https://www.youtube.com", "https://github.com/weslx"]
NUM_BROWSERS = 5

# Create a lock to ensure that only one thread initializes Chrome at a time.
chrome_init_lock = threading.Lock()

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
    except Exception:
        pass

def create_driver(profile, instance_id, drivers):
    profile_path = os.path.abspath(f'profiles/{profile}/instance_{instance_id}')
    os.makedirs(profile_path, exist_ok=True)

    options = uc.ChromeOptions()

    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument(f"--profile-directory=Profile_{instance_id}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--mute-audio")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=pt-BR")

    user_agent = "Mozilla/5.0 (Windows; Windows NT 10.2; WOW64; en-US) AppleWebKit/603.25 (KHTML, like Gecko) Chrome/53.0.1118.293 Safari/603.6 Edge/8.81572"
    options.add_argument(f"user-agent={user_agent}")

    try:
        # Ensure only one thread creates a driver at a time.
        with chrome_init_lock:
            driver = uc.Chrome(options=options, version_main=131)

        # Apply selenium-stealth to help mask fingerprinting details
        stealth(driver,
                languages=["pt-BR", "pt", "en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        # Override geolocation (example: San Francisco)
        driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
            "latitude": 37.7749,
            "longitude": -122.4194,
            "accuracy": 100
        })

        # Inject custom scripts to modify navigator properties:
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
        time.sleep(4)
        driver.get("https://hailuoaifree.com/image-to-video")
        drivers.append(driver)
        driver.switch_to.new_window('tab')
        driver.get("https://hailuoaifree.com/image-to-video")
        
    except Exception as e:
        print(f"Error creating browser: {e}")
        try:
            driver.quit()
        except:
            pass

def manage_profile(profile):
    drivers = []
    threads = []

    for i in range(1, NUM_BROWSERS + 1):
        t = threading.Thread(target=create_driver, args=(profile, i, drivers))
        threads.append(t)
        t.start()

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