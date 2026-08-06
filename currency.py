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
                    return response.read()
                print("Istek basarisiz oldu")
        except Exception as e:
            print(f"fetch_xml_data`de bir hata olustu({try_count + 1} / {max_try_count}): {e}")
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
                "currency_code": safe_str(currency.get("CurrencyCode")),
                "currency_name": safe_str(currency.find("Isim")),
                "forex_buying": safe_float(currency.find("ForexBuying")),
                "forex_selling": safe_float(currency.find("ForexSelling")),
                "banknote_buying": safe_float(currency.find("BanknoteBuying")),
                "banknote_selling": safe_float(currency.find("BanknoteSelling")),
                "unit": safe_float(currency.find("Unit")),
            }
            currencies.append(currency_dict)
        return currencies
    except Exception as e:
        print(f"parse_currencies`de bir hata olustu: {e}")


def display_currency_menu(currencies):
    for index, currency in enumerate(currencies, start=1):
        print(f"{index} - {currency['currency_name']} ({currency['currency_code']})")
    print()


def display_currency_detail(currency):
    print(f"***{currency['currency_name']} ({currency['currency_code']})***")
    print(f"Döviz Alis/Satis = {currency['forex_buying']}/  {currency['forex_selling']}")
    print(f"Efektif Alis/Satis = {currency['banknote_buying']}/ {currency['banknote_selling']}")


def safe_str(value) -> str:
    try:
        if hasattr(value, "text"):
            value = value.text
        if value is None:
            return "Deger bos"
        return str(value).strip()
    except Exception as e:
        print(f"safe_str`de bir hata olustu: {e}")
        return "Veri alinamadi"


def safe_float(value) -> float:
    if hasattr(value, "text"):
        value = value.text

    if value is None:
        return 0.0
    try:
        clean_number = float(str(value).strip().replace(",", "."))
        return max(clean_number, 0.0)
    except Exception:
        return 0.0


def safe_int(value: str) -> int:
    try:
        clean_value = int(value.strip().replace(",", ""))
        return max(clean_value, -1)
    except Exception:
        return -1


def calculate_exchange_amount(currency):
    try:
        while True:
            amount = safe_float(input("Döviz islemi icin belirlediginiz miktar(tl) : "))
            if amount > 0:
                break
            print("0 dan büyük pozitif bir sayi giriniz")

        final_amount = (amount / currency["forex_buying"]) * currency["unit"]
        print(
            f"{amount} TL = {final_amount:.3f} {currency['currency_name']}"
        )
    except Exception as e:
        print(f"calculate_exchange_amount`de bir hata olustu: {e}")


try:
    if __name__ == "__main__":
        while True:
            xml = fetch_xml_data(URL_EXCHANGE_RATES_TODAY)
            currencies = parse_currencies(xml)
            display_currency_menu(currencies)

            input_currency = safe_int(input("Bir numara secin: "))
            if input_currency > len(currencies) or input_currency <= 0:
                print("Yanlis tuslama")
                input("Devam etmek için 'enter' a basin")
                continue

            input_currency -= 1
            currency = currencies[input_currency]
            display_currency_detail(currency)

            if currency["forex_buying"] <= 0 or currency["unit"] <= 0:
                print(
                    f"ForexBuying: {currency['forex_buying']} veya Unit: {currency['unit']} değeri 0 veya daha küçük olduğundan hesap yapilamaz."
                )
                input("Devam etmek için 'enter' a basin")
                continue

            while True:
                input_select = safe_int(
                    input(
                        "Ana menu için 0 Belirli bir para miktarini çevirmek için 1: "
                    )
                )
                if input_select == 1:
                    calculate_exchange_amount(currency)
                elif input_select == 0:
                    break
                else:
                    print("Yanlis tuslama")
                    input("Devam etmek için 'enter' a basin")
                    continue
except Exception as e:
    print(f"Bir hata olustu: {e}")