import lxml.html as le
from lxml import etree
import re
import requests
import os
from time import sleep
import csv
from datetime import datetime

def RemoveNonAscii(text):
    res=''.join([i if ord(i) < 128 else ' ' for i in text]).strip()
    if(res==''):
        return '0'
    return res

nameRe="\"nom\":\"(.*?)\","
priceRe="\"prixPromo\":\"(.*?)\""



headerName='-----NAME-------'
headerPrice='--------PRICE---------'  



url_dict={
    "site_1_2_Url":"http://mobile.free.fr/",
    "site_1_1_Url":"https://www.free.fr/freebox/",
    "site_2_1_Url":"https://www.sfr.fr/offre-internet/box/#sfrintid=HS_MAIN_Offres-box_PAR",
    "site_2_2_Url":"https://www.sfr.fr/forfait-mobile/offres/forfait-mobile#sfrintid=HS_MAIN_Forfaits-mobile_PAR",
    "site_3_1_Url":"https://www.bouyguestelecom.fr/offres-internet",
    "site_3_2_Url":"https://www.bouyguestelecom.fr/bons-plans/serie-speciale-b-you",
    "site_4_1_Url":"https://boutique.orange.fr/internet/offres-fibre",
    "site_4_2_Url":"https://boutique.orange.fr/mobile/forfaits-orange"
}

xPathDict={"name":"//h5/div/div[@class='markdown-p']",\
    "w-div":"//div[@class='sc-hmXxxW fuYjca']/span[@class='sc-jTzLTM iXZCuB']",
    "b-div":"//div[@class='sc-hmXxxW jPKUCL']/span[@class='sc-jTzLTM iXZCuB']",
    "test":"//div[@class='sc-hmXxxW jPKUCL']/span[@class='sc-fjdhpX jZqwup']"
    }
currDir = os.path.dirname(os.path.realpath(__file__))
dataList=[]


def scrapeSite1():
    #part1
    print("1-1 Started")
    s=requests.session()
    html=s.get(url_dict['site_1_1_Url']).text
    tree=le.fromstring(html)
    names=tree.xpath(xPathDict['name'])
    wd=tree.xpath(xPathDict['w-div'])
    bd=tree.xpath(xPathDict['b-div'])
    prices_div=bd+wd
    prices=[]
    for p in prices_div:
        price=""
        left=p.findall("./span[@class='sc-kAzzGY hqcLUv']")
        right=p.findall("./span[@class='sc-fjdhpX jZqwup']/span[@class='sc-jzJRlG eLwrik']/span[@class='sc-kgoBCf kVSTZj']")
        if(len(left)==0):
            price="0.0"
        elif(len(left)!=0 and len(right)==0):
            price=left[0].text+".0"
        else:
            price=left[0].text+"."+right[0].text
        prices.append(price)
    if(len(names)==len(prices)):
        l=len(names)
        for i in range(l):
            data=dict()
            data[headerName]=names[i].text
            data[headerPrice]=prices[i]
            dataList.append(data)
    print("1-1 Completed")
    #Part 2 of site 1
    print("1-2 Started")
    s=requests.session()
    html=s.get(url_dict['site_1_2_Url']).text
    tree=le.fromstring(html)
    dataDivs=tree.xpath("//div[@class='grid-c cell-top forfait']")
    for div in dataDivs:
        name=div.xpath("./h1[@class='description']")
        name2=div.xpath("./h1[@class='description']/span[1]")
        left=div.xpath("./div[contains(@class,'prix-mensuel')]/span[@class='prix prix-red prix-main']")
        right=div.xpath("./div[contains(@class,'prix-mensuel')]/span[@class='prix-other red']/span[@class='prix prix-red prix-cent']")
        price=RemoveNonAscii(left[0].text.strip())+"."+RemoveNonAscii(right[0].text)
        #print(name[0].text+" "+name2[0].text+" "+price)
        data=dict()
        data[headerName]=str(name[0].text+" "+name2[0].text).strip()
        data[headerPrice]=price
        dataList.append(data)
    print("1-2 Completed")


def scrapeSite2():
    print("2-1 Started")
    s=requests.session()
    html=s.get(url_dict['site_2_1_Url']).text
    tree=le.fromstring(html)
    divs=tree.xpath("//div[@class='overviewCol__inner']")
    for div in divs:
        name=div.findall(".//h2[@class='title600']")
        left=div.findall(".//div[@class='prix__valeur']")
        right=div.findall(".//span[@class='prix__devise']")
        price=RemoveNonAscii(left[0].text.strip())+"."+RemoveNonAscii(right[0].text)
        #print(name[0].text+" "+price)
        data=dict()
        data[headerName]=name[0].text
        data[headerPrice]=price
        dataList.append(data)
    print("2-1 Completed")
    
    #part 2 
    print("2-2 Started")
    s=requests.session()
    html=s.get(url_dict['site_2_2_Url']).text
    tree=le.fromstring(html)
    divs=tree.xpath("//div[@class='overviewCol__inner']")
    for div in divs:
        name=div.findall(".//h2[@class='title600']")
        left=div.findall(".//div[@class='prix__valeur']")
        right=div.findall(".//span[@class='prix__devise']")
        price=RemoveNonAscii(left[0].text.strip())+"."+RemoveNonAscii(right[0].text)
        #print("2-2-Mob-  "+name[0].text+" "+price)
        data=dict()
        data[headerName]=name[0].text
        data[headerPrice]=price
        dataList.append(data)
    print("2-2 Completed")
    

def scrapeSite3():
    #PART 1
    print("3-1 Started")
    s=requests.session()
    html=s.get(url_dict['site_3_1_Url']).text
    tree=le.fromstring(html)
    divs=tree.xpath("//div[contains(@class,'column is-half-tablet is-3-desktop')]")
    for div in divs:
        name=div.findall(".//title")
        if(len(name)==0):
            img=div.findall(".//div/header/h2/img")
            name=str(img[0].get('alt'))
        left=div.findall(".//p[@class='main']")
        right=div.findall(".//span[@class='centimes']")
        try:
         price=RemoveNonAscii(left[0].text.strip())+"."+RemoveNonAscii(right[0].text)
        except:
         price="0.0"
        if(isinstance(name,str)):
          #print(name+" "+price)
          data=dict()
          data[headerName]=name
          data[headerPrice]=price
          dataList.append(data)
        else:
           #print(name[0].text+" "+price)
           data=dict()
           data[headerName]=name[0].text
           data[headerPrice]=price
           dataList.append(data) 
    print("3-1 Completed")
    #PART 2
    print("3-2 Started")
    s=requests.session()
    html=s.get(url_dict['site_3_2_Url']).text
    tree=le.fromstring(html)
    divs=tree.xpath("//div[contains(@class,'offers')]/div[contains(@class,'offer')]")
    for div in divs:
        name=div.xpath(".//div[@class='head']/div[@class='head_container']/h2[contains(@class,'head_title')]")
        name=str(le.tostring(name[0],method="text").strip())[4:-1]
        left=div.findall(".//th[@class='big']")
        right=div.findall(".//th[@class='sup']")
        price=str(left[0].text)+"."+RemoveNonAscii(str(right[0].text_content()))
        data=dict()
        data[headerName]=name
        data[headerPrice]=price
        dataList.append(data)
    print("3-2 Completed")
    


def scrapeSite4():
    print("4-1 Started")
    s=requests.session()
    html=s.get(url_dict['site_4_1_Url']).text
    tree=le.fromstring(html)
    divs=tree.xpath("//div[@class='template header-crem']")
    for div in divs:
        name=div.findall(".//h3/span")
        left=div.findall(".//span[@class='integer']")
        right=div.findall(".//div[@class='price text-primary']/sup")
        price=RemoveNonAscii(left[0].text.strip())+"."+RemoveNonAscii(right[0].text).replace(",",'')
       # print(name[0].text+"   "+price)
        data=dict()
        data[headerName]=name[0].text
        data[headerPrice]=price
        dataList.append(data)
    print("4-1 Completed")
    #PART 2
    print("4-2 Started")
    s=requests.session()
    html=s.get(url_dict['site_4_2_Url']).text
    names=re.findall(nameRe,html)
    prices=re.findall(priceRe,html)
    if(len(names)==len(prices)):
        for i in range(len(names)):
            #print(names[i]+"--->"+prices[i])
            data=dict()
            data[headerName]=names[i]
            data[headerPrice]=prices[i].replace(',','.')
            dataList.append(data)
    print("4-2 Completed")
      
def init():
    try:
        dat=datetime.date(datetime.now())
        di={headerName:dat,headerPrice:"----"}
        dataList.append(di)
        di=currDir+"/data"
        os.mkdir(di)
    except:
        print("Folder already exist")

def writeListToCsv(toCSV):
    oldData=[]
    keys = toCSV[0].keys()
    fileName=currDir+"/data/data.csv"
    xists = os.path.isfile(fileName)
    if(xists):
        with open(fileName, "r") as f:
            reader = csv.DictReader(f)
            oldData=list(reader)
    #appending old data with new Data
    toCSV=toCSV+oldData        
    with open(fileName, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(toCSV)

def main():
    init()
    scrapeSite1()
    scrapeSite2()
    scrapeSite3()
    scrapeSite4()
    writeListToCsv(dataList)
    
    


if __name__ == "__main__":
    main()