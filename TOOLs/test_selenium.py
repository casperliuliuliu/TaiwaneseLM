#Simple assignment
import time
from selenium.webdriver import Chrome
driver = Chrome()
url ='https://www.google.com.tw'
driver.get(url)
time.sleep(2)
driver.close()