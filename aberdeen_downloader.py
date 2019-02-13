import requests
import numpy as np 
import lxml.html as lh

main_url='http://abri.une.edu.au/online/cgi-bin/i4.dll?1=3E37202F&2=2828&3=56&5=2B3C2B3C3A'
base_url='http://abri.une.edu.au/online/cgi-bin/'
xPathDict={"next_button":"//a[contains(text(),'Next')]",
           "membership_name":"//table[@id='MemberListing']/tr/td/a",
           "current_herd":"//strong[contains(text(),'Current Herd:')]/parent::*/parent::*/td[2]/a",
           "animal_listing":"//table[@id='AnimalListing']/tr/td/a"
           }



def extractDataFromAnimalListing(link):
    link=base_url+link
    while True:
        resp=requests.get(link)
        pageData=resp.text
        lxml_tree = lh.fromstring(pageData)
        anlimaList=lxml_tree.xpath(xPathDict['animal_listing'])
        print('len----'+str(len(anlimaList)))
        for animal in anlimaList:
            print('---->>'+animal.get('href'))
        nextBtn=lxml_tree.xpath(xPathDict['next_button'])
        if(len(nextBtn)==0):
            break
        else:
            link=base_url+nextBtn[0].get('href')

    
def extractDataFromMember(link):
    link=base_url+link
    resp=requests.get(link)
    pageData=resp.text
    lxml_tree = lh.fromstring(pageData)
    aTag=lxml_tree.xpath(xPathDict['current_herd'])[0]
    link=aTag.get('href')
    extractDataFromAnimalListing(link)



def main():
    resp=requests.get(main_url)
    pageData=resp.text
    while True:
        lxml_tree = lh.fromstring(pageData)
        members=lxml_tree.xpath(xPathDict['membership_name'])
        for member in members:
            href=member.get('href')
            extractDataFromMember(href)
        nextBtn=lxml_tree.xpath(xPathDict['next_button'])[0]
        if(len(nextBtn)==0):
            break
        else:
            nextPageLink=str(base_url)+str(nextBtn.get('href'))
            pageData=requests.get(nextPageLink).text


        
if __name__== '__main__':
    main()