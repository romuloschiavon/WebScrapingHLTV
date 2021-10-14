import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json

############################
#Instanciando o Opera      #
############################
url = "https://www.hltv.org/stats/teams/maps/8297/furia?startDate=2020-10-14&endDate=2021-10-14&rankingFilter=Top20"

option = Options()
option.headless = True
driver = webdriver.Firefox(options=option)

driver.get(url)
time.sleep(3)

#clicando no maldito negocio dos cookie que fez dar um trilhao de erros
driver.find_element_by_xpath("//a[@id='CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll']").click()
time.sleep(0.5) #delay pra nao da merda

#escolher qual o mapa você quer as estatisticas
driver.find_element_by_xpath(f"//div[@class='stats-top-menu']/div[2]/a[1]").click()

#recuperar os dados
element = driver.find_element_by_xpath(f"//div[@class='stats-section stats-team stats-team-map']")
conteudo = element.get_attribute('innerHTML')

#começar a parsear o conteudo html para transformar em uma tabela
soup = BeautifulSoup(conteudo, 'html.parser')

time.sleep(0.5)

rawStats = soup.find_all("div", {"class": "stats-rows"}) #status cru
gameChanger = soup.find_all("div", {"class": "col standard-box big-padding"}) #status que ganham jogos
matchHistory = soup.find("table", {"class": "stats-table"}) #historico no mapa

############################
#Estruturando o data frame #
############################


dataFrame = pd.read_html(str(matchHistory))[0]
dataFrame.columns = ['Data', 'Oponente', 'Evento', 'Resultado']

print(dataFrame)


driver.quit()
