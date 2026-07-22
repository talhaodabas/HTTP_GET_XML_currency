TR;
Uygulama, XML dosyasındaki 22 farklı döviz biriminin güncel kur verilerini çekip kullanıcıya sunmaktadır. XML mimarisinde her Currency nesnesi içinde yer alan Grandchild elemanları gruplandırılarak bir diziye aktarılır; bu işlem her istekte güncel olarak tekrarlanır. İsimlendirmelerde XML'deki orijinal alan isimleri korunmuştur.

Kullanıcılar seçtikleri döviz biriminin anlık verilerini görüntüleyebileceği gibi, belirttikleri TL tutarını seçilen para birimine dönüştürme imkanına da sahiptir.

Fonksiyonlar;
    get_xml(url): Verilen url adresinde ki xml dosyayı çeker.   xml_data olarak çıktı verir.
    set_xml(): get_xml den aldığı xml verisini okunabilir hale getirir. Veriyi currencys dizisine [x,CurrencyCode,Isim,ForexBuying,ForexSelling,BanknoteBuying,BanknoteSelling,Unit] şeklinde sırayla ekler. Tamamlanmış currencys dizisini çıkartır.
    print_xml(currencys): currencys dizisinde bulunan sütunlarda ki x,CurrencyCode,Isim verilerini ekrana yazdırır.
    safe_float(element): ForexBuying,ForexSelling,BanknoteBuying,BanknoteSelling burada ki veriler boş veya float a dönüştürülemez gelmesi durumunda hata almamak için önceden bu verilerin boş ve text olduğunu kontrol edip float a dönüştürüyor. Eğer veri boş veya text değil ise veriyi 0.0 eşitliyor hataları önlemek için.
    calculate_currency: Kişi girdiği tl değerin seçtiği para birimindeki karşılığını burada hesaplanıyor. Şuan sadece 1 ve 100 unitler için hazırlandı.

