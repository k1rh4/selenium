from selenium import webdriver

driver_path = "/mnt/c/Users/k1rha/Desktop/Tools/chromedriver.exe"
driver = webdriver.Chrome(driver_path)
driver.implicitly_wait(3)
driver.get('https://google.com')

