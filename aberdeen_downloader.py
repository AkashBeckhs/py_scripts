import requests
import numpy as np 
import lxml.html as lh

main_url='http://abri.une.edu.au/online/cgi-bin/i4.dll?1=3E37202F&2=2828&3=56&5=2B3C2B3C3A'
base_url='http://abri.une.edu.au/online/cgi-bin/'
xPathDict={"next_button":"//a[contains(text(),'Next')]",
           "membership_name":"//table[@id='MemberListing']/tr/td/a",
           "current_herd":"//strong[contains(text(),'Current Herd:')]/parent::*/parent::*/td[2]/a",
           "animal_listing":"//table[@id='AnimalListing']/tr/td/a",
           "index_values":"//a[contains(text(),'Show Index Values')]",
           "type_head":"//table[@class='AnimalDetails']/tr/td/strong[contains(text(),'%s')]/parent::*/parent::*/td[2]",
           "ebv1":"//table[@class='TablesEBVBox'][1]/tr[3]/td",
           "acc":"//table[@class='TablesEBVBox'][1]/tr[4]/td",
           "ebv2":"//table[@class='TablesEBVBox'][1]/tr[3]/td",
           "t_index":"//table[@class='TablesEBVBox'][2]/tr[3]/td",
           "s_index":"//table[@class='TablesEBVBox'][2]/tr[4]/td",
           "second_table":"//table[@class='TablesEBVBox'][2]"
           }

type_list=['Identifier',
            'Sex',
            'Birth Date',
            'Registration Status',
            'Breeder',
            'Current Owner',
            'HerdBook Volume No.',
            'National ID']        

bp_list=['Calving_Ease_DIR',
            'Calving_Ease_DTRS',
            'Gestation_Length',
            'Birth_Wt',
            'Day_Wt_200',
            'Day_Wt_400',
            'Day_Wt_600',
            'Mat_Cow_Wt',
            'Milk',
            'Scrotal_Size',
            'Carcase_Wt',
            'Eye_Muscle_Area',
            'Fat_Depth',
            'Retail_Beef_Yield',
            'IMF']

index_list=['Index_Value','Breed_average']

def saveToDB(dataDict):
    columns=''
    values=''
    for key, value in dataDict.items():
        columns=columns+key+","
        values =values+"'"+value+"',"
    columns=columns[:-1]
    values=values[:-1]
    sql="insert into animals ("+columns+") values("+values+")"
    print(sql)


    

def extractValues(link):
    dataDict=dict()
    link=base_url+link
    resp=requests.get(link)
    pageData=resp.text
    lxml_tree = lh.fromstring(pageData)
    for e in type_list:
        xPath=xPathDict['type_head'] %e
        element=lxml_tree.xpath(xPath)
        if(element!=None and len(element)>0):
            element=element[0]
            key=e.replace(" ","_")
            val=element.text_content().strip()
            dataDict[key]=val    
    for i in range(1,16):
        ebv1_list=lxml_tree.xpath(xPathDict['ebv1'])
        acc_list=lxml_tree.xpath(xPathDict['acc'])
        ebv2_list=lxml_tree.xpath(xPathDict['ebv2'])
        eb1_key='ebv1_'+bp_list[i-1]
        eb2_key='ebv2_'+bp_list[i-1]
        acc_key='acc_'+bp_list[i-1]
        try:
            ebv1_val=ebv1_list[i].text_content().strip()  
        except:
            ebv1_val='-'
        try:
            ebv2_val=ebv2_list[i].text_content().strip()
        except:
            ebv2_val='-'
        try:
            acc_val=acc_list[i].text_content().strip()
        except:
            acc_val='-'
        dataDict[eb1_key]=ebv1_val
        dataDict[eb2_key]=ebv2_val
        dataDict[acc_key]=acc_val
    st=lxml_tree.xpath(xPathDict['second_table'])
    if(len(st)>0):
        for j in range(1,3):
            t_index_list=lxml_tree.xpath(xPathDict['t_index'])
            s_index_list=lxml_tree.xpath(xPathDict['s_index'])
            ti_key='TI_'+index_list[j-1]
            si_key='SI_'+index_list[j-1]
            try:
                ti_val=t_index_list[j].text_content().strip()
            except:
                ti_val='-'
            try:
                si_val=s_index_list[j].text_content().strip()
            except:
                si_val='-'
            dataDict[ti_key]=ti_val
            dataDict[si_key]=si_val
    saveToDB(dataDict)
        
def showIndexValues(link):
    link=base_url+link
    resp=requests.get(link)
    pageData=resp.text
    lxml_tree = lh.fromstring(pageData)
    print(link)
    a_tag=lxml_tree.xpath(xPathDict["index_values"])[0]
    link=a_tag.get('href')
    extractValues(link)

    

def iterateAnimalListing(link):
    link=base_url+link
    while True:
        resp=requests.get(link)
        pageData=resp.text
        lxml_tree = lh.fromstring(pageData)
        anlimaList=lxml_tree.xpath(xPathDict['animal_listing'])
        for animal in anlimaList:
            link=animal.get('href')
            showIndexValues(link)
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
    iterateAnimalListing(link)



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