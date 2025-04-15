from selenium import webdriver
import time

def screenshot(url, filename):
    driver = webdriver.Chrome()  
    try:
        driver.get(url)
        time.sleep(5)  
        driver.save_screenshot(filename)
    finally:
        driver.quit()
