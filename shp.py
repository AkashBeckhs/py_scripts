import requests
import csv
import re
import lxml.html
from lxml import etree


baseUrl="https://www.sonomacounty.com/activities/wineries-wine"
home="https://www.sonomacounty.com/"
sub="/activities/wineries-wine?&page=%s"
proxies={"http":"http://10.135.0.26:8080/","https":"http://10.135.0.26:8080/"}
dataList=[]

xpathDict={
          "shopLink":"//div[@class='node__content']/div[@class='field field--name-field-display-title field--type-string field--label-hidden field__item']/h4/a[contains(@href,'wineries')]",
          "address":"//div[@class='middle']/div[@class='col profile-location profile-info-col']/p",
          "company":"//div[@class='top']/div[@class='field field--name-field-display-title field--type-string field--label-hidden field__item']/h2",
          "phone":"//a[@data-action='outbound_full--local-phone']",
          "email":"//div[@class='col profile-contact profile-info-col']/p[2]/a",
          "website":"//a[@data-action='outbound_full--website']"}

def writeToCsv():
  keys = dataList[0].keys()
  with open('C:\\Users\\aakash\\Desktop\\py workspace\\wineries\\data.csv', 'w') as output_file:
      dict_writer = csv.DictWriter(output_file, keys)
      dict_writer.writeheader()
      dict_writer.writerows(dataList)

def decodeEmail(encodedString):
 r = int(encodedString[:2],16)
 email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
 return email

def getData(href,s):
    dataDict=dict()
    url=home+href
    resp= s.get(url,proxies=proxies)
    html=str(resp.text)
    #print(html)
    tree=lxml.html.fromstring(html)
    try:
      dataDict['company']=tree.xpath(xpathDict['company'])[0].text
    except:
      dataDict['company']="N/A"
    try:
     dataDict['website']=tree.xpath(xpathDict['website'])[0].get('href')
    except:
      dataDict['website']="N/A"
    try:
      #decoding email
      encoded=str(tree.xpath(xpathDict['email'])[0].get('href')).split("#",1)[1]
      dataDict['email']=decodeEmail(encoded)
    except:
      dataDict['email']="N/A"
    try:
     add=str(etree.tostring(tree.xpath(xpathDict['address'])[0], method='text',pretty_print=True))
     dataDict['address']=add[2:-1]
    except:
      dataDict['address']="N/A"
    try:
      dataDict['phone']=tree.xpath(xpathDict['phone'])[0].text
    except:
      dataDict['phone']="N/A"
    dataDict['area']="N/A"
    dataDict['first']="N/A"
    dataDict['last']="N/A"
    dataDict['title']="N/A"
    print(dataDict)
    dataList.append(dataDict)



def main():
  s=requests.session()
  flag=True
  counter=1
  url=home+sub %str(counter)
  while(flag):
    print(url)
    resp= s.get(url,proxies=proxies)
    html=str(resp.text)
    #print(html)
    parser = etree.HTMLParser()
    tree=etree.fromstring(html,parser=parser)
    #when no links are found , assuming no more data
    emp=tree.xpath("//div[@class='view-empty']/h2")
    if(len(emp)>0):
      writeToCsv()
      break
    shopLinks=tree.xpath(xpathDict['shopLink'])
    for link in shopLinks[1:]:
      href=link.get('href')
      getData(href,s)
    counter=counter+1
    url=home+sub %str(counter)
    
      
    
    


if __name__=="__main__":
  main()