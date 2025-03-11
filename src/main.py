import os
import threading
from seleniumbase import Driver
from helpers import automation_flow  # Import the automation flow function

PREDEFINED_URLS = []
NUM_BROWSERS = 6

# Default screen resolution (fallback)
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Create a lock to ensure that only one thread initializes Chrome at a time.
chrome_init_lock = threading.Lock()

def ask_profile():
    while True:
        profile = input("Select profile: ").strip()
        if profile:
            return profile
        print("Profile name cannot be empty!")

def calculate_browser_dimensions():
    """Calculate dimensions for browsers that ALWAYS use full screen height"""
    # Always use the full screen height
    height = SCREEN_HEIGHT
    
    # Divide the screen width by the number of browsers
    width = SCREEN_WIDTH // NUM_BROWSERS
    
    return width, height

def calculate_browser_position(instance_id):
    """Calculate position for each browser in a side-by-side arrangement"""
    width, height = calculate_browser_dimensions()
    
    # Place each browser side by side
    x = (instance_id - 1) * width
    
    # Start from the top of the screen
    y = 0
    
    return x, y, width, height




def create_driver(profile, instance_id, drivers):
    profile_path = os.path.abspath(f'profiles/{profile}/instance_{instance_id}')
    os.makedirs(profile_path, exist_ok=True)
    try:
        # Calculate position and size
        x, y, width, height = calculate_browser_position(instance_id)
        
        
        # Ensure only one thread creates a driver at a time
        with chrome_init_lock:
            # Create driver using SeleniumBase with download preferences
            driver = Driver(
                uc_cdp=True,  # Use undetected mode
                user_data_dir=profile_path,
                dark_mode=True,
                headless=False,
                incognito=False,
                ad_block_on=True, 
            )

            # Set window size and position - FULL HEIGHT
            driver.set_window_size(width, height)
            driver.set_window_position(x, y)


        # Open all URLs in separate tabs
        for index, url in enumerate(PREDEFINED_URLS):
            if index == 0:
                driver.get(url)
            else:
                driver.switch_to.new_window('tab')
                driver.get(url)

        drivers.append(driver)
        
    except Exception as e:
        print(f"Error creating browser {instance_id}: {e}")
        try:
            driver.quit()
        except:
            pass

def run_automation_in_all(drivers):
    """Run the automation flow in all browsers simultaneously"""
    threads = []
    results = []
    
    def run_automation(driver, idx):
        try:
            print(f"Starting automation in browser {idx+1}...")
            automation_flow(driver)
            results.append(f"Browser {idx+1}: Automation completed")
        except Exception as e:
            results.append(f"Browser {idx+1}: Error - {str(e)}")
    
    # Start automation in all browsers simultaneously
    for i, driver in enumerate(drivers):
        t = threading.Thread(target=run_automation, args=(driver, i))
        threads.append(t)
        t.start()
    
    # Wait for all automation processes to complete
    for t in threads:
        t.join()
        
    # Print results
    print("\n----- Automation Results -----")
    for result in results:
        print(result)
    print("-----------------------------")

def manage_profile(profile):
    print(f"Opening {NUM_BROWSERS} browsers with profile '{profile}'...")
    drivers = []
    threads = []

    # Start all browser threads simultaneously
    for i in range(1, NUM_BROWSERS + 1):
        t = threading.Thread(target=create_driver, args=(profile, i, drivers))
        threads.append(t)
        t.start()

    # Wait for all browsers to open
    for t in threads:
        t.join()
    
    print(f"\nAll {len(drivers)} browsers are now open!")
    print("You can now use the browsers normally.")
    print("Press Enter to start automation in all browsers, or type 'exit' to close all browsers...")
    
    # Wait for user input
    while True:
        user_input = input().strip().lower()
        
        if user_input == 'exit':
            break
        elif user_input == '':
            # Run automation in all browsers
            run_automation_in_all(drivers)
            print("\nAutomation completed!")
            print("Press Enter to run automation again, or type 'exit' to close all browsers...")
        # Adicionar ao main.py na função manage_profile
        elif user_input == '1':
            # Importar a função
            from sendImg import send_to_all_browsers
            # Enviar vídeos para todos os navegadores
            send_to_all_browsers(drivers)
            print("\nEnvio de vídeo completado!")
            print("Press Enter to run automation again, type 'sendvideo' to send videos, or type 'exit' to close browsers...")
        else:
            print("Invalid command. Press Enter to start automation or type 'exit' to close browsers...")
    
    # Close all browsers quickly
    close_threads = []
    for driver in drivers:
        t = threading.Thread(target=lambda d: d.quit(), args=(driver,))
        close_threads.append(t)
        t.start()
    
    for t in close_threads:
        t.join()
    
    print("All browsers closed.")

def main():
    profile = ask_profile()
    manage_profile(profile)

if __name__ == "__main__":
    main()