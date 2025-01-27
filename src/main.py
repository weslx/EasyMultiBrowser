import os
import pickle
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

PREDEFINED_URLS = ["https://www.youtube.com", "https://github.com/weslx"]
NUM_BROWSERS = 3

def ask_profile():
    return input("Select profile: ").strip()

def create_driver(profile, instance_id, drivers):
    cookie_path = f'profiles/{profile}/cookies_{instance_id}.pkl'
    os.makedirs(os.path.dirname(cookie_path), exist_ok=True)

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        if os.path.exists(cookie_path):
            with open(cookie_path, 'rb') as f:
                cookies = pickle.load(f)
            for index, url in enumerate(PREDEFINED_URLS):
                if index == 0:
                    driver.get(url)
                else:
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[-1])
                    driver.get(url)
            for window_handle in driver.window_handles:
                driver.switch_to.window(window_handle)
                for cookie in cookies:
                    try:
                        driver.add_cookie(cookie)
                    except:
                        pass
                driver.refresh()
        else:
            for index, url in enumerate(PREDEFINED_URLS):
                if index == 0:
                    driver.get(url)
                else:
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[-1])
                    driver.get(url)
    except Exception as e:
        print(f"Error loading cookies: {e}")
        for index, url in enumerate(PREDEFINED_URLS):
            if index == 0:
                driver.get(url)
            else:
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[-1])
                driver.get(url)

    drivers.append((driver, cookie_path))

def manage_profile(profile):
    drivers = []
    threads = []

    for i in range(1, NUM_BROWSERS + 1):
        t = threading.Thread(target=create_driver, args=(profile, i, drivers))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    input("\nPress Enter to save cookies and close browsers...")

    for driver, cookie_path in drivers:
        try:
            all_cookies = []
            for window_handle in driver.window_handles:
                driver.switch_to.window(window_handle)
                all_cookies.extend(driver.get_cookies())
            with open(cookie_path, 'wb') as f:
                pickle.dump(all_cookies, f)
        except Exception as e:
            print(f"Error saving cookies: {e}")
        finally:
            driver.quit()

def main():
    profile = ask_profile()
    manage_profile(profile)

if __name__ == "__main__":
    main()