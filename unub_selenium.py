from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def get_unsubscribe_links():

    return ["https://www.nitrocollege.com/hs/manage-preferences/unsubscribe?d=Vnd69h8zMss2VKkvLs43WHm-W3zdVJy3_R592N1JxwY5WxCRsN17r7tjQtHw4W69pKrV5r2TpwVD96Lw4XJvkcW8_dXpq5-WS6-N7qXl2f1yf0NW302y_l69Rl-VN2nFK8xmRKt7n6h12W91H3&v=3&utm_campaign=eng1p_nit_u_co_wsbco_e2_11192021&utm_source=hs_automation&utm_medium=email&utm_content=184874763&_hsmi=184874763", "https://click.e.atlassian.com/?qs=ee06bfb7b6bee077492f973d17a77b7c96775d55e81e7f5a8987bdbab054d84ef82efdb9193fe4520da9a7b5f985387a535c3a7190185a5799adac57ed5ac0d8"]

def main():
    # Initialize the Safari WebDriver
    driver = webdriver.Safari()

    # Retrieve unsubscribe links from emails
    unsubscribe_links = get_unsubscribe_links()

    for link in unsubscribe_links:
        try:
            # Navigate to the unsubscribe link
            driver.get(link)
            time.sleep(2)  # Wait for the page to load (adjust as necessary)

            # Find and click the unsubscribe button
            # The specifics might vary, adjust as necessary
            unsubscribe_button = driver.find_element(By.XPATH, '//button[contains(text(), "Unsubscribe", "Unsubscribe Here", "Submit")]')
            unsubscribe_button.click()
            time.sleep(1)  # Wait for any potential redirect or confirmation

        except Exception as e:
            print(f"Error processing {link}: {e}")

    # Close the browser
    driver.quit()

if __name__ == "__main__":
    main()