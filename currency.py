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
        for currency in root.findall("Currency"):
            currency_dict = {
                "currency_code": currency.get("CurrencyCode"),
                "currency_name": currency.find("Isim").text,
                "forex_buying": extract_float_from_element(currency.find("ForexBuying")),
                "forex_selling": extract_float_from_element(currency.find("ForexSelling")),
                "banknote_buying": extract_float_from_element(currency.find("BanknoteBuying")),
                "banknote_selling": extract_float_from_element(currency.find("BanknoteSelling")),
                "unit": extract_float_from_element(currency.find("Unit")),
            }
            currencies.append(currency_dict)
        return currencies
    except Exception as e:
        print(f"Bir hata olustu: {e}")


def display_currency_menu(currencies):
    for index, currency in enumerate(currencies, start=1):
        print(f"{index} - {currency['currency_name']} ({currency['currency_code']})")
    print()


def display_currency_detail(currency):
    print(f"{currency['currency_code']}, Döviz Alis/Satis = {currency['forex_buying']}/{currency['forex_selling']}, Efektif Alis/Satis = {currency['banknote_buying']}/{currency['banknote_selling']}")


def extract_float_from_element(element):
    try:
        clean_number = float(element.text.strip().replace(',', '.'))
        return max(clean_number, 0.0)
    except Exception:
        return 0.0


def convert_string_to_float(number):
    try:
        clean_number = float(number.strip().replace(',', '.'))
        return max(clean_number, 0.0)
    except Exception:
        return 0.0


def convert_string_to_int(number):
    try:
        clean_number = int(number.strip().replace(',', ''))
        return max(clean_number, 0)
    except Exception:
        return 0


def calculate_exchange_amount(currency):
    try:
        while True:
            amount = convert_string_to_float(input("Döviz islemi icin belirlediginiz miktar(tl) : "))
            if amount >= 1:
                break
            print("0 dan büyük pozitif bir sayi giriniz")
        
        final_amount = (amount / currency["forex_buying"]) * currency["unit"]
        print(f"{amount} TL = {format(final_amount, '.3f')} {currency['currency_name']}")
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
                display_currency_detail(currency)
                
                if currency['forex_buying'] <= 0 or currency['unit'] <= 0:
                    print(f"ForexBuying: {currency['forex_buying']} veya Unit: {currency['unit']} değeri 0 veya daha küçük olduğundan hesap yapilamaz.")
                    input("Devam etmek için 'enter' a basin")
                    break
                
                while True:
                    select = convert_string_to_int(input("Ana menu için 0 Belirli bir para miktarini çevirmek için 1: "))
                    if select == 1:
                        calculate_exchange_amount(currency)
                    elif select == 0:
                        break
                    else:
                        print("Yanlis tuslama")
except Exception as e:
    print(f"Bir hata olustu: {e}")