import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json

#Instanciando o Opera
url = "https://www.hltv.org/stats/teams/maps/8297/furia?startDate=2020-10-14&endDate=2021-10-14&rankingFilter=Top20"

option = Options()
option.headless = True
driver = webdriver.Firefox()

driver.get(url)
time.sleep(5)

driver.find_element_by_xpath("")



driver.quit()
