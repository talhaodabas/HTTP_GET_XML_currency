import sys
import time
import xml.etree.ElementTree as ET
from urllib.request import urlopen

URL_EXCHANGE_RATES_TODAY = "https://www.tcmb.gov.tr/kurlar/today.xml"


def fetch_xml_data(url, max_try_count=3, delay_time=3):
    try_count = 0
    while try_count < max_try_count:
        try:
            with urlopen(url) as response:
                if response.status == 200:
                    return response.read()
                print("Istek basarisiz oldu")
        except ValueError as e:
            print(f"fetch_xml_data`de bir hata olustu (Deneme sayisi: {try_count + 1} / {max_try_count}): {e}")
        try_count += 1
        time.sleep(delay_time)
    print("Denenme sonlandirildi. Veri çekilemedi")
    return None


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
    except ValueError as e:
        print(f"parse_currencies`de bir hata olustu: {e}")
    print("Veri ayriştirilamadi")
    return None


def refresh_currencies(url=URL_EXCHANGE_RATES_TODAY, delay_time=3):
    xml = fetch_xml_data(url, delay_time=delay_time)
    if not xml:
        return None
    currencies = parse_currencies(xml)
    if not currencies:
        return None
    return currencies


def display_currency_menu(currencies):
    for index, currency in enumerate(currencies, start=1):
        print(f"{index} - {currency['currency_name']} ({currency['currency_code']})")
    print()


def display_currency_detail(currency):
    print(f"***{currency['currency_name']} ({currency['currency_code']})***")
    print(f"Döviz Alis/Satis = {currency['forex_buying']}/  {currency['forex_selling']}")
    print(f"Efektif Alis/Satis = {currency['banknote_buying']}/ {currency['banknote_selling']}")


def safe_str(value) -> str:
    if hasattr(value, "text"):
        value = value.text
    if value is None:
        return "Deger bos"
    if not isinstance(value,str):
        return "Deger none_str"
    try:
        float(value)
        return "Deger none_str"
    except ValueError:
        pass
    try:
        return str(value).strip()
    except ValueError as e:
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
    except ValueError:
        return 0.0


def safe_int(value: str) -> int:
    if value is None:
        return -1
    try:
        clean_value = int(value.strip().replace(",", ""))
        return max(clean_value, -1)
    except ValueError:
        return -1


def calculate_exchange(amount: float, forex_buying: float, unit: float) -> float:
    if forex_buying is None or unit is None or forex_buying <=0 or unit <=0:
        return 0.0
    try:
        return (amount / forex_buying) * unit
    except ValueError as e:
        print(f"calculate_exchange`de bir hata olustu: {e}")
        return 0.0


def handle_exchange(currency):
    try:
        while True:
            amount = safe_float(
                input("Döviz islemi icin belirlediginiz miktar(tl) : ")
            )
            if amount > 0:
                break
            print("0 dan büyük pozitif bir sayi giriniz")

        final_amount = calculate_exchange(amount, currency["forex_buying"], currency["unit"])
        print(
            f"{amount} TL = {final_amount:.3f} {currency['currency_name']}"
        )
    except ValueError as e:
        print(f"handle_exchange`de bir hata olustu: {e}")


try:
    if __name__ == "__main__":
        currencies = refresh_currencies()
        if not currencies:
            print("'currencies' oluşturulunamadi")
            sys.exit()
        start_time = time.time()
        check_time = 60
        while True:
            current_time = time.time()
            if current_time - start_time > check_time:
                print("Kur güncelleniyor...")
                time.sleep(1)
                new_currencies = refresh_currencies()
                if new_currencies:
                    currencies = new_currencies
                    print("Kur güncellendi")
                else:
                    print("Hata, eski kurdan devam ediniliniyor")
                start_time = time.time()
            display_currency_menu(currencies)

            input_currency = safe_int(input("Bir numara secin: "))
            if input_currency > len(currencies) or input_currency <= 0:
                print("Yanlis tuslama")
                input("Devam etmek için 'enter' a basin")
                continue

            input_currency -= 1
            currency = currencies[input_currency]
            display_currency_detail(currency)

            while True:
                input_select = safe_int(
                    input(
                        "Ana menu için 0 Belirli bir para miktarini çevirmek için 1: "
                    )
                )
                if input_select == 1:
                    if currency["forex_buying"] <= 0 or currency["unit"] <= 0:
                        print(
                            f"{currency['currency_code']} kurunun Döviz Alis/Satis veya Unit değeri bozuk olduğundan hesap yapilamaz."
                        )
                        input("Ana menü için 'enter' a basin")
                        break
                    handle_exchange(currency)
                elif input_select == 0:
                    break
                else:
                    print("Yanlis tuslama")
                    input("Devam etmek için 'enter' a basin")
                    continue
except ValueError as e:
    print(f"Bir hata olustu: {e}")