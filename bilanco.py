##IS YATIRIM'DAN TOPLU BİLANCO CEKME

import requests

from bs4 import BeautifulSoup
import pandas as pd

hisseler= ["AKBNK"] #cektigim hisseleri bu listede saklayacagım
url="https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse=ACSEL"
r=requests.get(url)

s=BeautifulSoup(r.text,"html.parser") #r değişkeninden text yani string yapılarını almaya calisiyorum

s1=s.find("select",id="ddlAddCompare")

c1=s1.findChild("optgroup").findAll("option") #htmldeki otpgroup'daki optionları gereksiz olduğu icin aldık ve cıkartıyoruz


#for a in c1:
#    hisseler.append(a.string) #string diyerek tagin icindeki string degerini aldık yoksa tüm satırı alıyor

##eğer tum hisseleri değil belirledigimiz birkac hisseyi almak istiyorsak:
## hisseler=["ASCEL","THYAQ"] kodu bunun icin yeterli


#---------------------------------------------------------

#tum hisseler icin bu islemi tek tek yapması icin for olusturduk
for i in hisseler:
    hisse=i
    grup=[]
    #donemler her hisse icin farkılılık gosteriyor orgenin thy icin farklı akbank icin farklı donemlere ait veriler var.
    #bu yuzden bunu da bir degisken kabul ediyoruz. hepsinin aynı degil cunku
    tarihler=[]
    yillar=[]
    donemler=[]

    url1="https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse="+hisse #yukaridaki linkten ASCEL kısmını sildik ve hisselerimiz icindeki
    #tum hisselerin linklerine tek tek ulasmasını sagladık
    r1=requests.get(url1)
    soup=BeautifulSoup(r1.text,"html.parser")
    
    secim=soup.find("select",id="ddlMaliTabloFirst")
    secim2=soup.find("select",id="ddlMaliTabloGroup")

    try:
        cocuklar=secim.findChildren("option") #tarihleri alip tarihler isimli yapıya göndereceğim
        grup=secim2.find("option")["value"] #xı_29 degerini aldik ACSEL icin ve her hissede bu deger degisiyor

        for i in cocuklar:
            tarihler.append(i.string.rsplit("/")) #bos liste olusturmustuk, burada cocuklardan gelen degeri gonderiyorum
            #rsplit ile ornegin "2014/9" olan yapıyı "2014","9" olarak ayırmıs olduk 
            #simdi de olusturdugumuz listede yılları ve donemleri ayıracagız
        for j in tarihler:
            yillar.append(j[0]) #yıllar listede sıfırıncı indexte gorunuyor, dönemler 1. indexte
            donemler.append(j[1])
        
        if len(tarihler)>=4: ##4 dönemden daha az bilgi varsa örnegin sirketin sadece 3 doneme ait bilgisi var, biz bunu istemiyoruz pas gec diyecegiz
            parametreler=(
                ("companyCode",hisse),
                ("exchange","TRY"),
                ("financialGroup",grup),
                ("year1",yillar[0]), #ornegin 2023/3 icin 2023u alacak
                ("period1",donemler[0]),#burada 3u alacak
                ("year2",yillar[1]), 
                ("period2",donemler[1]), 
                ("year3",yillar[2]), 
                ("period3",donemler[2]),
                ("year4",yillar[3]),
                ("period4",donemler[3])
            )
            url2="https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo"
            r2=requests.get(url2,params=parametreler).json()["value"] #sadece value degerlerini aldim
            veri=pd.DataFrame.from_dict(r2)
            veri.drop(columns=["itemCode","itemDescEng"],inplace=True)
            print(veri)
        else:
            continue
    except AttributeError: ##bazı hisseler findChildren hatası veriyor bu yüzdden try except yapısı kullandık
        continue ##böyle bir seyle karsılastıgında hata vermeyecek ama herhangi bir islem de yapmayacak


#ilk dört dönemi zaten aldığımız icin tarihlerdeki ilk 4 dönemi silmemiz gerekiyor?
    del tarihler[0:4]
    tumveri=[veri]

    for _ in range(0,int(len(tarihler+1))):
        if len(tarihler)==len(yillar):
            del tarihler[0:4]
        else:
            yillar=[]
            donemler=[]
            


