TR;
Uygulama, XML dosyasındaki 22 farklı döviz biriminin güncel kur verilerini çekip kullanıcıya sunmaktadır. XML mimarisinde her Currency nesnesi içinde yer alan Grandchild elemanları gruplandırılarak bir diziye aktarılır; bu işlem her istekte güncel olarak tekrarlanır. İsimlendirmelerde XML'deki orijinal alan isimleri korunmuştur.

Kullanıcılar seçtikleri döviz biriminin anlık verilerini görüntüleyebileceği gibi, belirttikleri TL tutarını seçilen para birimine dönüştürme imkanına da sahiptir.

EN;
The application retrieves current exchange rate data for 22 different currencies from an XML file and presents it to the user. In the XML structure, the “Grandchild” elements contained within each “Currency” object are grouped and transferred to an array; this process is repeated in real time with each request. The original field names in the XML have been preserved in the naming conventions.

Users can view real-time data for their selected currency and also convert a specified amount in Turkish lira (TL) to the selected currency.
