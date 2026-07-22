import xml.etree.ElementTree as ET
from urllib.request import urlopen

def get_xml(url):
    try:
        with urlopen(url) as response:
                xml_data = response.read()
        return xml_data
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

def set_xml():
    try:
        root = ET.fromstring(get_xml("https://www.tcmb.gov.tr/kurlar/today.xml"))
        currencys =[]
        for x,currency in enumerate(root.findall("Currency"), start=1):
            CurrencyCode = currency.get("CurrencyCode")
            Isim = currency.find("Isim").text
            ForexBuying = safe_float(currency.find("ForexBuying"))
            ForexSelling = safe_float(currency.find("ForexSelling"))
            BanknoteBuying = safe_float(currency.find("BanknoteBuying"))
            BanknoteSelling = safe_float(currency.find("BanknoteSelling"))
            Unit = safe_float(currency.find("Unit"))
            currencys.append([x,CurrencyCode,Isim,ForexBuying,ForexSelling,BanknoteBuying,BanknoteSelling,Unit])
        return currencys
    except Exception as e:
            print(f"Bir hata oluştu: {e}")

def print_xml(currencys):
    try:
        for currency in currencys:
             print(f"{currency[0]} - {currency[1]} ({currency[2]})")
        print()
    except Exception as e:
                print(f"Bir hata oluştu: {e}")

def safe_float(element):
    if element is not None and element.text:
        return  float(element.text)
    return 0.0

def calculate_currency(currency):
    try:
        amount = float(input("Döviz islemi icin belirlediginiz miktar(tl) : "))    
        finall_amount =  (amount / (currency[3]))*currency[7]
        print(f"{amount} TL = {format(finall_amount, '.3f')} {currency[1]}")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

try:
    while True:
        currencys = set_xml()
        print_xml(currencys)
        currency = int(input("Bir numara secin: ")) - 1
        if currency > (len(currencys)-1):
            print("Yanlis tuslama")
            break
        currency = currencys[currency]
        print(f"{currency[1]}, Döviz Alis/Satis = {currency[3]}/{currency[4]}, Efektif Alis/Satis = {currency[5]}/{currency[6]}")
        
        while True:
            select = int(input("Ana menü için 0 Belirli bir para miktarini çevirmek için 1: "))
            if select == 1:
                calculate_currency(currency)
            elif select == 0:
                break
            else:
                print("Yanlis tuslama")
except Exception as e:
    print(f"Bir hata oluştu: {e}")