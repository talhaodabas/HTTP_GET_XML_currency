#    TCMB Döviz Kuru Takip ve Çevirici (HTTP GET XML)

TR; Bu uygulama, TCMB XML servisinden 22 farklı döviz biriminin güncel kur verilerini çekip kullanıcıya sunmaktadır. XML mimarisinde her `Currency` nesnesi içinde yer alan elemanlar gruplandırılarak bir diziye aktarılır; bu işlem her istekte güncel olarak tekrarlanır. İsimlendirmelerde XML'deki orijinal alan isimleri korunmuştur.

Kullanıcılar seçtikleri döviz biriminin anlık verilerini görüntüleyebileceği gibi, belirttikleri TL tutarını seçilen para birimine dönüştürme imkanına da sahiptir.

---

##    Fonksiyonlar

* `fetch_xml_data(url)`: Verilen URL adresindeki XML dosyasını çeker ve `xml_data` olarak çıktı verir. Veri alınamadığı durumda belirtilen deneme sayısı kadar yeniden dener.
* `parse_currencies(xml_data)`: XML verisini ayrıştırır. Her bir para birimini Dictionary yapısına dönüştürerek `currencies` dizisine şu formatta ekler ve döndürür:
  ```python
  {
    "currency_code": "USD",
    "currency_name": "ABD DOLARI",
    "forex_buying": 34.25,
    "forex_selling": 34.31,
    "banknote_buying": 34.22,
    "banknote_selling": 34.36,
    "unit": 1.0
  }
* `refresh_currencies(url, delay_time)`: XML verisini çekme (`fetch_xml_data`) ve ayrıştırma (`parse_currencies`) işlemlerini tek bir adımda çalıştırır; veriyi başarıyla alırsa `currencies` dizisini, aksi halde `None` döndürür.
* `display_currency_menu(currencies)`: `currencies` dizisinde bulunan para birimlerini kodu ve adıyla birlikte menü formatında ekrana listeler.
* `display_currency_detail(currency)`: Seçilen para birimine ait kodu ve detaylı kur bilgilerini (Döviz Alış/Satış, Efektif Alış/Satış) düzenli bir formatta ekrana basar.
* `safe_str(value)`: XML'den gelen veriler boş veya dönüştürülemeyen yapıda olduğunda uygulamanın çökmesini önler ve `input` dan gelen verinin boş veya dönüştürülemeyen yapıda olduğunda uygulamanın çökmesini önler; geçerli bir metin varsa `str` tipine çevirir, aksi halde `Deger bos` döndürür.
* `safe_float(value)`: XML'den gelen veriler boş veya dönüştürülemeyen yapıda olduğunda uygulamanın çökmesini önler ve `input` dan gelen verinin boş veya dönüştürülemeyen yapıda olduğunda uygulamanın çökmesini önler; geçerli bir metin varsa `float` tipine çevirir, aksi halde `0.0` döndürür.
* `safe_int(value: str)`: `input` dan gelen verinin boş veya dönüştürülemeyen yapıda olduğunda uygulamanın çökmesini önler; geçerli bir metin varsa `int` tipine çevirir, aksi halde `-1` döndürür.
* `calculate_exchange(amount, forex_buying, unit)`: Girilen TL tutarını, seçilen döviz kuru ve birim (`unit`) değerine göre matematiksel olarak dönüştürür ve sonucu `float` tipinde döndürür.
* `handle_exchange(currency)`: Kullanıcıdan çevrilmek istenen TL tutarını `input` ile alır, `calculate_exchange` fonksiyonunu çağırarak hesaplamayı yaptırır ve sonucu ekrana basar.