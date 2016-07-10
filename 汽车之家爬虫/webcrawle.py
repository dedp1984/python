#汽车之家各种车辆指导价爬虫程序
#作者：萤火虫

from bs4 import BeautifulSoup
from urllib import request
import re
import uuid
import os
#获取品牌地址列表
def getCarMainUrl():
    fp=open("d:\\brandAddr.txt","w")
    bsBrands=BeautifulSoup(open("d:\\brandAddress.html"),"html5lib").find_all('a');
    for brand in bsBrands:
        fp.write("http://car.autohome.com.cn"+brand['href'])
        fp.write("\n")
    fp.close()
#读取品牌地址列表
def startDownLoadPage(filePath):
    fp=open(filePath,"r")
    lines=fp.readlines()
    for line in lines:
        filename=str(uuid.uuid1())
        downloadHtmlPage(line,filename,"d:\\qczj")
        downloadChildHtmlPages("d:\\qczj\\"+filename+".html")
        #查找停售的页面下载地址
        bsBrand=BeautifulSoup(open("d:\\qczj\\"+filename+".html"),"html5lib")
        statusLinks=bsBrand.find(class_=re.compile("^tab-nav")).find_all("li")
        for i in range(1,len(statusLinks)):
            filename1=str(uuid.uuid1())
            if statusLinks[i]['class'][0]=='disabled':
                continue
            
            downloadHtmlPage("http://car.autohome.com.cn"+statusLinks[i].find('a')['href'],filename1,"d:\\qczj")
            downloadChildHtmlPages("d:\\qczj\\"+filename1+".html")
    fp.close()


#根据网页地址下载品牌主网页
def downloadHtmlPage(url,name,savePath):
    print(url)
    resp=request.urlopen(url)
    fp=open(savePath+"\\"+name+".html","w+")
    fp.write(resp.read().decode(encoding='gbk'))
    fp.flush()
    fp.close()

#下载品牌子页面
def downloadChildHtmlPages(htmlFilePath):
    bsBrand=BeautifulSoup(open(htmlFilePath),"html5lib")
    pages=bsBrand.find(id="brandtab-1").find(class_="price-page")
    if not pages:
        pass
    else:
        links=pages.find_all('a')
        if(len(links)<=3):
            pass
        else:
            print(links)
            for i in range(2,len(links)-1):
                #print(links[i]['href'])
                #print(links[i].text)
                downloadHtmlPage("http://car.autohome.com.cn"+links[i]['href'],str(uuid.uuid1()),"d:\\qczj")
               
              
    

#分析网页中的车辆信息
def analysisHtml(htmlPath,file):
    bsBrand=BeautifulSoup(open(htmlPath),"html5lib")
    #查找所有子品牌
    allCarBrand=bsBrand.find(id="brandtab-1").find_all(class_=re.compile("list-cont|brand-title|^intervalcont"),recursive=False)
    isStopSale=bsBrand.find(class_=re.compile("^tab-nav")).find("li",class_='current').text=='停售'
    isSale=bsBrand.find(class_=re.compile("^tab-nav")).find("li",class_='current').text=='在售'
    isWillSale=bsBrand.find(class_=re.compile("^tab-nav")).find("li",class_='current').text=='即将销售'
    subCompany=''
    carSeries=''
    carPz=''
    for i,brand in enumerate(allCarBrand) :
        #取得车辆子公司
        if brand['class'][0]=='brand-title':
            subCompany=brand.find('h3').string
        #取得车辆系列
        elif brand['class'][0]=='list-cont':
            carSeries=brand.find(class_='main-title').find('a').string
        #获取车辆配置信息
        else:
            #获取车辆配置信息
            carConfig=brand.find_all(class_=re.compile("^interval"),recursive=False)
            for carModel in carConfig:
                #获取车辆类型及价格
                carPz=carModel.find(class_='interval01-list-cars-text').string
                carTypes=carModel.find_all('li')
                for carType in carTypes:
                    typeDtl=carType.find_all('div',recursive=False)
                    typeName=typeDtl[0].find('a').string
                    typeGuidePrice=''
                    if isStopSale:
                        typeGuidePrice=typeDtl[1].text
                    else:
                        typeGuidePrice=typeDtl[2].text
                    #print(subCompany+"-"+carSeries+"-"+carPz+"-"+typeName+"-"+typeGuidePrice)
                    if isStopSale:
                        file.write(subCompany+"-"+carSeries+"-"+carPz+"-"+typeName+"-"+typeGuidePrice+"-停售"+"\n")
                    elif isSale:
                        file.write(subCompany+"-"+carSeries+"-"+carPz+"-"+typeName+"-"+typeGuidePrice+"-在售"+"\n")
                    elif isWillSale:
                        file.write(subCompany+"-"+carSeries+"-"+carPz+"-"+typeName+"-"+typeGuidePrice+"-即将销售"+"\n")
                    else:
                        pass
                    
def test():
    print('开始分析网页......\n')
    listDir=os.listdir("d:\\qczj")
    fp=open("d:\\car.list","w+")
    for filename in listDir:
        analysisHtml("d:\\qczj\\"+filename,fp)
    fp.flush()
    fp.close()
    print('分析网页完成.....\n')
def main():
    print('开始网页下载.....\n')
    startDownLoadPage("d:\\brandAddr.txt")
    print('下载网页完成.....\n')
    print('开始分析网页......\n')
    listDir=os.listdir("d:\\qczj")
    fp=open("d:\\car.list","a+")
    for filename in listDir:
        analysisHtml("d:\\qczj\\"+filename,fp)
    fp.flush()
    fp.close()
    print('分析网页完成.....\n')
main()
#test()
#getCarMainUrl()    
