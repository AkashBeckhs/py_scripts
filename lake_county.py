import requests
import csv
import re
import lxml.html
from lxml import etree


homeUrl="https://www.winesnw.com/ormerch.html"
proxies={"http":"http://10.135.0.26:8080/","https":"http://10.135.0.26:8080/"}
dataList=[]

xpathDict={"div":"//center/table/tbody/tr[3]/td/table/tbody/tr[2]/td[1]/*"}

def writeToCsv():
  keys = dataList[0].keys()
  with open('C:\\Users\\aakash\\Desktop\\py workspace\\wineries\\data.csv', 'w') as output_file:
      dict_writer = csv.DictWriter(output_file, keys)
      dict_writer.writeheader()
      dict_writer.writerows(dataList)


def main():
  s=requests.session()
  resp=s.get(homeUrl,proxies=proxies)
  html=str(resp.text)
  tree=lxml.html.fromstring(html)
  divs=tree.xpath(xpathDict['div'])
  


  
if __name__=="__main__":
  main()