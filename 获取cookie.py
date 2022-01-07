import time
from selenium import webdriver

# 获取cookie用于自动登录

driver = webdriver.Chrome(executable_path='./chromedriver.exe')
driver.get('https://www.airbnb.cn/')
time.sleep(120)
print(driver.get_cookies())
driver.quit()
