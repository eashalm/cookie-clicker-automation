from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import time, math

# Specify SPEND_FREQUENCY such that the bot spends cookies (on upgrades & products) every SPEND_FREQUENCY seconds.
SPEND_FREQUENCY = 30
START_TIME = time.time()
PATH = "C:\Program Files (x86)\chromedriver.exe"

# Initialize the webdriver.
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(PATH, options=options)

# HELPER FUNCTIONS
def click_big_cookie():
    driver.find_element(By.ID, "bigCookie").click()

def buy_upgrades():
    if driver.find_elements(By.CSS_SELECTOR, "div.crate.upgrade.enabled"):
        for _ in range(len(driver.find_elements(By.CSS_SELECTOR, "div.crate.upgrade.enabled"))):
            try:
                driver.execute_script("arguments[0].click();", driver.find_element(By.ID, "upgrade0"))
            except StaleElementReferenceException:
                driver.execute_script("arguments[0].click();", driver.find_element(By.ID, "upgrade0"))

def buy_products():
    if driver.find_elements(By.CSS_SELECTOR, "div.product.unlocked.enabled"):
        num_available_products = len(driver.find_elements(By.CSS_SELECTOR, "div.product.unlocked.enabled"))
        for i in range(num_available_products - 1, -1, -1):
            product = driver.find_element(By.ID, f"product{i}")
            while "enabled" in product.get_attribute("class").split():
                driver.execute_script("arguments[0].click();", product)

def click_golden_cookie():
    driver.execute_script("setInterval(function() {for (var i in Game.shimmers) { Game.shimmers[i].pop(); }}, 1000);")
# END OF HELPER FUNCTIONS

# Main game logic.
def main():
    # Start the Cookie Clicker game.
    driver.get("https://orteil.dashnet.org/cookieclicker")

    # Select language & close distractions.
    driver.implicitly_wait(5)
    driver.find_element(By.LINK_TEXT, "Got it!").click()
    driver.find_element(By.ID, "langSelect-EN").click()
    driver.find_element(By.LINK_TEXT, "Don't show this again").click()

    # Game loop.
    while True:
        # Click the Big Cookie!
        click_big_cookie()

        # Spend cookies (on upgrades & products) every SPEND_FREQUENCY seconds, IF available.
        if math.floor(time.time() - START_TIME) % SPEND_FREQUENCY == 0:

            # Spend cookies on upgrades, IF available.
            buy_upgrades()

            # Spend cookies on products, IF available.
            buy_products()
        
        # Click the Golden Cookie, if available. 
        click_golden_cookie()

if __name__ == '__main__':
    main()
