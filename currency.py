import xml.etree.ElementTree as ET
from urllib.request import urlopen
import sys

def set_xml(xml_data):
    try:
        root = ET.fromstring(xml_data)
        currencys = []
        for x,currency in enumerate(root.findall("Currency"), start=1):
            CurrencyCode = currency.get("CurrencyCode")
            Isim = currency.find("Isim").text
            ForexBuying = safe_float_element(currency.find("ForexBuying"))
            ForexSelling = safe_float_element(currency.find("ForexSelling"))
            BanknoteBuying = safe_float_element(currency.find("BanknoteBuying"))
            BanknoteSelling = safe_float_element(currency.find("BanknoteSelling"))
            Unit = safe_float_element(currency.find("Unit"))
            currencys.append([x,CurrencyCode,Isim,ForexBuying,ForexSelling,BanknoteBuying,BanknoteSelling,Unit])
        return currencys
    except Exception as e:
        print(f"Bir hata olustu: {e}")

def print_xml(currencys):
    try:
        for currency in currencys:
            print(f"{currency[0]} - {currency[1]} ({currency[2]})")
        print()
    except Exception as e:
        print(f"Bir hata olustu: {e}")

def safe_float_element(element):
    try:
        clean_number = float(element.text.strip().replace(',','.'))
        if clean_number >= 0:return clean_number
        return 0.0
    except Exception:
        return 0.0

def safe_float(number):
    try:
        clean_number = float(number.strip().replace(',','.'))
        if clean_number >= 0:return clean_number
        return 0.0
    except Exception:
        return 0.0

def safe_int(number):
    try:
        clean_number = int(number.strip().replace(',',''))
        if clean_number >= 0:return clean_number
        return 0
    except Exception:
        return 0

def calculate_currency(currency):
    try:
        while True:
            amount = safe_float(input("Döviz islemi icin belirlediginiz miktar(tl) : "))
            if amount >= 1:break
            print("0 dan büyük pozitif bir sayi giriniz")
        finall_amount =  (amount / (currency[3]))*currency[7]
        print(f"{amount} TL = {format(finall_amount, '.3f')} {currency[1]}")
    except Exception as e:
        print(f"Bir hata olustu: {e}")

try:
    if __name__ == '__main__':
        try_count = 0
        max_try_count = 3
        while True:
            while True:
                try:
                    with urlopen("https://www.tcmb.gov.tr/kurlar/today.xml") as response:
                        result_successful = response.status
                        if result_successful:
                            xml_data = response.read()
                        else:
                            print("Istek basarisiz oldu")
                            print(f"Deneniyor: {try_count + 1} / {max_try_count}")
                            try_count+=1
                            if try_count == max_try_count:
                                print(f"Denenme sonlandirildi. Url ya da kodu kontrol edin")
                                sys.exit()
                            break
                except Exception as e:
                    print(f"Bir hata olustu: {e}")
                    print(f"Deneniyor: {try_count + 1} / {max_try_count}")
                    try_count+=1
                    if try_count == max_try_count:
                        print(f"Denenme sonlandirildi. Url ya da kodu kontrol edin")
                        sys.exit()
                    break
                currencys = set_xml(xml_data)
                print_xml(currencys)
                number = safe_int(input("Bir numara secin: "))
                if number > (len(currencys)) or number <= 0:
                    print("Yanlis tuslama")
                    input("Devam etmek için 'enter' a basin")
                    break
                number-=1
                currency = currencys[number]
                print(f"{currency[1]}, Döviz Alis/Satis = {currency[3]}/{currency[4]}, Efektif Alis/Satis = {currency[5]}/{currency[6]}")
                if currency[3] <= 0 or currency[7] <= 0:
                    print(f"ForexBuying: {currency[3]} veya Unit: {currency[7]} değeri 0 veya daha küçük olduğundan hesap yapilamaz.")
                    input("Devam etmek için 'enter' a basin")
                    break
                while True:
                    select = safe_int(input("Ana menü için 0 Belirli bir para miktarini çevirmek için 1: "))
                    if select == 1:
                        calculate_currency(currency)
                    elif select == 0:
                        break
                    else:
                        print("Yanlis tuslama")
except Exception as e:
    print(f"Bir hata olustu: {e}")