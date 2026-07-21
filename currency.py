import xml.etree.ElementTree as ET
from urllib.request import urlopen

while True:
        
        with urlopen("https://www.tcmb.gov.tr/kurlar/today.xml") as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)
        currencys =[]
        x = 1
        for currency in root.findall("Currency"):
            CurrencyCode = currency.get("CurrencyCode")
            Isim = currency.find("Isim").text
            ForexBuying = currency.find("ForexBuying").text
            ForexSelling = currency.find("ForexSelling").text
            BanknoteBuying = currency.find("BanknoteBuying").text
            BanknoteSelling = currency.find("BanknoteSelling").text
            CrossRateUSD = currency.find("CrossRateUSD").text
            CrossRateOther = currency.find("CrossRateOther").text
            currencys.append([x,CurrencyCode,Isim,ForexBuying,ForexSelling,BanknoteBuying,BanknoteSelling,CrossRateUSD,CrossRateOther])
            print(f"{currencys[x-1][0]} - {currencys[x-1][1]} ({currencys[x-1][2]})")
            x+=1
        print()
        s_currency = int(input("Bir numara secin: "))-1
        if s_currency > (x-2):
            print("Yanlis tuslama")
            break
        print(s_currency,x)
        print(f"{currencys[s_currency][1]}, Döviz Alis/Satis {currencys[s_currency][3]}/{currencys[s_currency][4]}, Efektif Alis/Satis {currencys[s_currency][5]}/{currencys[s_currency][6]}, CrossRateUSD {currencys[s_currency][7]}, CrossRateOther {currencys[s_currency][8]}")
        while True:
            select = int(input("Ana menü için 0 Belirli bir para miktarini çevirmek için 1: "))
            if select == 1:
                money = float(input("Döviz islemi icin belirlediginiz miktar(tl) : "))
                finall_money =  money / float(currencys[s_currency][3])
                print(f"{money} TL = {format(finall_money, '.3f')} {currencys[s_currency][1]}")
            elif select == 0:
                break
            else:
                print("Yanlis tuslama")
