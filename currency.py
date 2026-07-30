import sys
import time
import xml.etree.ElementTree as ET
from urllib.request import urlopen

URL_EXCHANGE_RATES_TODAY = "https://www.tcmb.gov.tr/kurlar/today.xml"


def fetch_xml_data(url):
    try_count = 0
    max_try_count = 3
    while True:
        try:
            with urlopen(url) as response:
                if response.status == 200:
                    xml_data = response.read()
                    return xml_data
                else:
                    print("Istek basarisiz oldu")
                    print(f"Deneniyor: {try_count + 1} / {max_try_count}")
                    try_count += 1
                    if try_count == max_try_count:
                        print("Denenme sonlandirildi. Url ya da kodu kontrol edin")
                        sys.exit()
                    time.sleep(3)
        except Exception as e:
            print(f"Bir hata olustu: {e}")
            print(f"Deneniyor: {try_count + 1} / {max_try_count}")
            try_count += 1
            if try_count == max_try_count:
                print("Denenme sonlandirildi. Url ya da kodu kontrol edin")
                sys.exit()
            time.sleep(3)


def parse_currencies(xml_data):
    try:
        root = ET.fromstring(xml_data)
        currencies = []
        for x, currency in enumerate(root.findall("Currency"), start=1):
            currency_code = currency.get("CurrencyCode")
            currency_name = currency.find("Isim").text
            forex_buying = extract_float_from_element(currency.find("ForexBuying"))
            forex_selling = extract_float_from_element(currency.find("ForexSelling"))
            banknote_buying = extract_float_from_element(currency.find("BanknoteBuying"))
            banknote_selling = extract_float_from_element(currency.find("BanknoteSelling"))
            unit = extract_float_from_element(currency.find("Unit"))
            
            currencies.append([
                x, currency_code, currency_name, 
                forex_buying, forex_selling, banknote_buying, banknote_selling, unit
            ])
        return currencies
    except Exception as e:
        print(f"Bir hata olustu: {e}")


def display_currency_menu(currencies):
    try:
        for currency in currencies:
            print(f"{currency[0]} - {currency[1]} ({currency[2]})")
        print()
    except Exception as e:
        print(f"Bir hata olustu: {e}")


def extract_float_from_element(element):
    try:
        clean_number = float(element.text.strip().replace(',', '.'))
        if clean_number >= 0:
            return clean_number
        return 0.0
    except Exception:
        return 0.0


def convert_string_to_float(number):
    try:
        clean_number = float(number.strip().replace(',', '.'))
        if clean_number >= 0:
            return clean_number
        return 0.0
    except Exception:
        return 0.0


def convert_string_to_int(number):
    try:
        clean_number = int(number.strip().replace(',', ''))
        if clean_number >= 0:
            return clean_number
        return 0
    except Exception:
        return 0


def calculate_exchange_amount(currency):
    try:
        while True:
            amount = convert_string_to_float(input("Döviz islemi icin belirlediginiz miktar(tl) : "))
            if amount >= 1:
                break
            print("0 dan büyük pozitif bir sayi giriniz")
        
        final_amount = (amount / currency[3]) * currency[7]
        print(f"{amount} TL = {format(final_amount, '.3f')} {currency[1]}")
    except Exception as e:
        print(f"Bir hata olustu: {e}")


try:
    if __name__ == '__main__':
        while True:
            while True:
                xml = fetch_xml_data(URL_EXCHANGE_RATES_TODAY)
                currencies = parse_currencies(xml)
                display_currency_menu(currencies)
                
                input_currency = convert_string_to_int(input("Bir numara secin: "))
                if input_currency > len(currencies) or input_currency <= 0:
                    print("Yanlis tuslama")
                    input("Devam etmek için 'enter' a basin")
                    break
                
                input_currency -= 1
                currency = currencies[input_currency]
                currency_code, forex_buying, forex_selling, banknote_buying, banknote_selling, unit = currency[1], currency[3], currency[4], currency[5], currency[6], currency[7]
                
                print(f"{currency_code}, Döviz Alis/Satis = {forex_buying}/{forex_selling}, Efektif Alis/Satis = {banknote_buying}/{banknote_selling}")
                
                if forex_buying <= 0 or unit <= 0:
                    print(f"ForexBuying: {forex_buying} veya Unit: {unit} değeri 0 veya daha küçük olduğundan hesap yapilamaz.")
                    input("Devam etmek için 'enter' a basin")
                    break
                
                while True:
                    select = convert_string_to_int(input("Ana menü için 0 Belirli bir para miktarini çevirmek için 1: "))
                    if select == 1:
                        calculate_exchange_amount(currency)
                    elif select == 0:
                        break
                    else:
                        print("Yanlis tuslama")
except Exception as e:
    print(f"Bir hata olustu: {e}")