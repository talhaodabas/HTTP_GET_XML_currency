#    TCMB Döviz Kuru Takip ve Çevirici (HTTP GET XML)

TR; Bu uygulama, TCMB XML servisinden 22 farklı döviz biriminin güncel kur verilerini çekip kullanıcıya sunmaktadır. XML mimarisinde her `Currency` nesnesi içinde yer alan elemanlar gruplandırılarak bir diziye aktarılır; bu işlem her istekte güncel olarak tekrarlanır. İsimlendirmelerde XML'deki orijinal alan isimleri korunmuştur.

Kullanıcılar seçtikleri döviz biriminin anlık verilerini görüntüleyebileceği gibi, belirttikleri TL tutarını seçilen para birimine dönüştürme imkanına da sahiptir.

---

##    Fonksiyonlar

* `fetch_xml_data(url)`: Verilen URL adresindeki XML dosyasını çeker ve `xml_data` olarak çıktı verir.
* `parse_currencies(xml_data)`: `fetch_xml_data(url)` ile alınan XML verisini işler. Veriyi `currencies` dizisine şu formatta sırayla ekler ve döndürür:
  `[x, currency_code, currency_name, forex_buying, forex_selling, banknote_buying, banknote_selling, unit]`
* `display_currency_menu(currencies)`: `currencies` dizisinde bulunan liste elemanlarını (`x`, `currency_code`, `currency_name`) ekrana listeler.
* `extract_float_from_element(element)`: XML'den gelen veriler boş veya dönüştürülemeyen yapıda olduğunda uygulamanın çökmesini önler; geçerli bir metin varsa `float` tipine çevirir, aksi halde `0.0` döndürür.
* `convert_string_to_float(number)`: `input` dan gelen verinin boş veya dönüştürülemeyen yapıda olduğunda uygulamanın çökmesini önler; geçerli bir metin varsa `float` tipine çevirir, aksi halde `0.0` döndürür.
* `convert_string_to_int`: `input` dan gelen verinin boş veya dönüştürülemeyen yapıda olduğunda uygulamanın çökmesini önler; geçerli bir metin varsa `int` tipine çevirir, aksi halde `0` döndürür.
* `calculate_exchange_amount(currency)`: Kullanıcının girdiği TL tutarının seçilen para birimindeki karşılığını hesaplar.
