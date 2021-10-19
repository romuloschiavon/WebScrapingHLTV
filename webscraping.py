import time
import requests
import string
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json

############################
#Instanciando o Firefox    #
############################
url = "https://www.hltv.org/stats/teams/map/31/8297/furia?startDate=2020-10-14&endDate=2021-10-14"

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
time.sleep(0.5)

#Status Crus

rawStats = driver.find_elements_by_xpath(f"//div[@class='stats-row']")
statTitle = []
statData = []
for stat in rawStats:
    titulo = stat.find_element_by_xpath("span[1]").get_attribute('innerHTML')
    dado = stat.find_element_by_xpath("span[2]").get_attribute('innerHTML')
    statTitle.append(titulo)
    statData.append(dado)

#Status Game Changer

gameChangerStats = driver.find_elements_by_xpath(f"//div[@class='col standard-box big-padding']")
gameChangerTitle = []
gameChangerData = []
for stat in gameChangerStats:
    titulo = stat.find_element_by_xpath("div[2]").get_attribute('innerHTML')
    dado = stat.find_element_by_xpath("div[1]").get_attribute('innerHTML')
    gameChangerTitle.append(titulo)
    gameChangerData.append(dado)

#Match History

element = driver.find_element_by_xpath(f"//div[@class='stats-section stats-team stats-team-map']")
conteudo = element.get_attribute('outerHTML')

#começar a parsear o conteudo html para transformar em uma tabela
soup = BeautifulSoup(conteudo, 'html.parser')

time.sleep(0.5)

matchHistory = soup.find("table", {"class": "stats-table"}) #historico no mapa

############################
#String Prettifying        #
############################

rawStatsTitle = []
rawStatsData = []
for substrings in statTitle:
    novoSplit = substrings.split('/')
    for split in novoSplit:
        rawStatsTitle.append(string.capwords(split))

for substrings in statData:
    novoSplit = substrings.split('/')
    for split in novoSplit:
        rawStatsData.append(split)

############################
#Estruturando o data frame #
############################

dataFrame = pd.read_html(str(matchHistory))[0]
dataFrame.columns = ['Data', 'Oponente', 'Evento', 'Resultado']

driver.quit()
