#    TCMB Döviz Kuru Takip ve Çevirici (HTTP GET XML)

TR; Bu uygulama, TCMB XML servisinden 22 farklı döviz biriminin güncel kur verilerini çekip kullanıcıya sunmaktadır. XML mimarisinde her `Currency` nesnesi içinde yer alan elemanlar gruplandırılarak bir diziye aktarılır; bu işlem her istekte güncel olarak tekrarlanır. İsimlendirmelerde XML'deki orijinal alan isimleri korunmuştur.

Kullanıcılar seçtikleri döviz biriminin anlık verilerini görüntüleyebileceği gibi, belirttikleri TL tutarını seçilen para birimine dönüştürme imkanına da sahiptir.

---

##    Fonksiyonlar

* `get_xml(url)`: Verilen URL adresindeki XML dosyasını çeker ve `xml_data` olarak çıktı verir.
* `set_xml()`: `get_xml()` ile alınan XML verisini işler. Veriyi `currencys` dizisine şu formatta sırayla ekler ve döndürür:
  `[x, CurrencyCode, Isim, ForexBuying, ForexSelling, BanknoteBuying, BanknoteSelling, Unit]`
* `print_xml(currencys)`: `currencys` dizisinde bulunan liste elemanlarını (`x`, `CurrencyCode`, `Isim`) ekrana listeler.
* `safe_float(element)`: XML'den gelen veriler boş veya dönüştürülemeyen yapıda olduğunda uygulamanın çökmesini önler; geçerli bir metin varsa `float` tipine çevirir, aksi halde `0.0` döndürür.
* `calculate_currency(currency)`: Kullanıcının girdiği TL tutarının seçilen para birimindeki karşılığını hesaplar.
