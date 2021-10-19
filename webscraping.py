import time
import requests
import string
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json

############################
#Main Function of File     #
############################
def WebScraping(type):
    '''
    Função criada para realizar o webscraping do HLTV da FURIA, gerando 3 data frames e diversos arrays que podem ser acessados para analisar os dados dos mapas da furia nos seus ultimos confrontos
    dos ultimos 12 meses. WinRate, GameChanger Stats, no futuro serão adicionados quem foram os MVPS e quem teve o pior desempenho de cada mapa, para facilitar o treino individual em cada mapa.
    
    '''
    
    mapaID = mapas[type]['mapaID']

    #escolher qual o mapa você quer as estatisticas
    driver.find_element_by_xpath(f"//div[@class='stats-top-menu']/div[2]/a[{mapaID}]").click()
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
            rawStatsData.append(string.capwords(split))

    ############################
    #Estruturando o data frame #
    ############################

    rawStatsDataFrameData = {'Stats': rawStatsTitle, 'Results': rawStatsData}
    rawStatsDataFrame = pd.DataFrame(data=rawStatsDataFrameData)

    gameChangerDataFrameData = {'Stats': gameChangerTitle, 'Results': gameChangerData}
    gameChangerDataFrame = pd.DataFrame(data=gameChangerDataFrameData)

    matchHistoryDataFrame = pd.read_html(str(matchHistory))[0]
    matchHistoryDataFrame.columns = ['Date', 'Oponnent', 'Event', 'Result']

    ############################
    #Estruturando dicts        #
    ############################

    rawStatsDict = {}
    rawStatsDict = rawStatsDataFrame.to_dict('records')

    gameChangerDict = {}
    gameChangerDict = gameChangerDataFrame.to_dict('records')

    matchHistoryDict = {}
    matchHistoryDict = matchHistoryDataFrame.to_dict('records')

    return [rawStatsDict, gameChangerDict, matchHistoryDict]

############################
#Definindo mapas CS:GO     #
############################
mapas = {
    'ancient': {'mapaID': '1'},
    'dust2':{'mapaID': '2'},
    'inferno':{'mapaID': '3'},
    'mirage':{'mapaID': '4'},
    'nuke':{'mapaID': '5'},
    'overpass':{'mapaID': '6'},
    'train':{'mapaID': '7'},
    'vertigo':{'mapaID': '8'}
}

############################
#Instanciando o Firefox    #
############################
url = "https://www.hltv.org/stats/teams/maps/8297/furia?startDate=2020-10-14&endDate=2021-10-14"

option = Options()
#option.headless = True
driver = webdriver.Firefox()

driver.get(url)
driver.implicitly_wait(3)

#clicando no maldito negocio dos cookie que fez dar um trilhao de erros
driver.find_element_by_xpath("//a[@id='CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll']").click()
time.sleep(0.5) #delay pra nao da merda

firstDict = {}
secondDict = {}
thirdDict = {}

for mapa in mapas:
    dicionarios = WebScraping(mapa)
    firstDict[mapa] = dicionarios[0]
    secondDict[mapa] = dicionarios[1]
    thirdDict[mapa] = dicionarios[2]

driver.quit()

############################
#Criando arquivos JSON     #
############################

with open('rawStats.json', 'w', encoding='utf-8') as createRaw:
    rawStatsJSON = json.dumps(firstDict)
    createRaw.write(rawStatsJSON)

with open('gameChanger.json', 'w', encoding='utf-8') as createGameChanger:
    gameChangerJSON = json.dumps(secondDict)
    createGameChanger.write(gameChangerJSON)

with open('matchHistory.json', 'w', encoding='utf-8') as createMH:
    matchHistoryJSON = json.dumps(thirdDict)
    createMH.write(matchHistoryJSON)