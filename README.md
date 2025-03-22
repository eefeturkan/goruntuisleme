# Görüntü İşleme Uygulaması

Bu uygulama, görüntü işleme dersi için geliştirilmiş bir Python uygulamasıdır. Tkinter kullanılarak oluşturulan arayüz sayesinde çeşitli görüntü işleme teknikleri uygulanabilir. Uygulama, kaydırılabilir bir kontrol paneli ile gelişmiş görüntü işleme özelliklerine kolay erişim sağlar.

## Özellikler

1. **Dosya İşlemleri**
   - Görüntü yükleme ve kaydetme
   - Çoklu formatta (PNG, JPG, BMP, GIF) dosya desteği

2. **Temel İşlemler**
   - Orijinal görüntüyü görüntüleme
   - Gri tonlamaya çevirme
   - RGB kanallara ayırma
   - Görüntünün negatifini alma

3. **Görüntü İyileştirme**
   - Parlaklık ayarlama (-100 ile +100 arası)
   - Eşikleme (Thresholding) (0-255 arası)
   - Histogram hesaplama ve görselleştirme
   - Histogram eşitleme
   - Kontrast ayarlama (0.1 ile 3.0 arası)

4. **Görüntü Dönüşümleri**
   - Görüntüyü taşıma (Translation)
   - X ve Y ekseninde aynalama (Flipping)
   - Görüntüyü eğme (Shearing)
   - Görüntüyü ölçekleme (Scaling/Zoom)
   - Görüntüyü döndürme (Rotation)
   - Görüntüyü kırpma (Cropping)

## Kurulum

1. Gerekli kütüphaneleri yükleyin:
   ```
   pip install -r requirements.txt
   ```

2. Uygulamayı çalıştırın:
   ```
   python goruntu_isleme_uygulamasi.py
   ```

## Kullanım

1. **Görüntü Açma**: "Görüntü Aç" butonuna tıklayarak bir görüntü dosyası seçin.
2. **İşlem Seçimi**: Sol taraftaki kaydırılabilir kontrol panelinden istediğiniz görüntü işleme tekniğini seçin.
3. **Dönüşüm İşlemleri**: "Görüntü Dönüşümleri" bölümünden ölçekleme, döndürme, eğme gibi işlemler için ilgili butona tıklayın ve açılan diyalog penceresinden parametreleri ayarlayın.
4. **Sonucu Kaydetme**: İşlenmiş görüntüyü "Görüntüyü Kaydet" butonu ile kaydedebilirsiniz.
5. **Histogram Analizi**: "Histogram Göster" butonu ile görüntünün histogramını görüntüleyebilirsiniz.

## Görüntü Dönüşüm İşlemleri Detayları

1. **Ölçekleme (Scaling)**:
   - X ve Y eksenlerinde ayrı ayrı ölçekleme faktörleri (0.1 - 3.0)
   - Büyütme ve küçültme işlemleri için optimize edilmiş interpolasyon

2. **Döndürme (Rotation)**:
   - -180° ile +180° arası döndürme açısı
   - Otomatik boyut ayarlama ile görüntünün tamamını koruma

3. **Kırpma (Cropping)**:
   - Sol, sağ, üst ve alt kenarların hassas ayarlanması
   - Seçilen bölgenin geçerliliğinin kontrolü

4. **Eğme (Shearing)**:
   - X ve Y eksenleri boyunca -0.5 ile 0.5 arası eğme faktörleri
   - Parallelogram efekti oluşturma

## Gereksinimler

- Python 3.6+
- OpenCV 4.8.0
- NumPy 1.24.3
- Matplotlib 3.7.2
- Pillow (PIL) 10.0.0

## Teknik Detaylar

Uygulama, Nesne Yönelimli Programlama (OOP) yaklaşımı kullanılarak geliştirilmiştir. Tüm görüntü işleme işlevleri, `GoruntuIslemeUygulamasi` sınıfı içinde metotlar olarak düzenlenmiştir.

Uygulama ayrıca detaylı görüntü işleme bilgileri içeren bir yardım dosyası (`goruntu_isleme_temel_bilgiler.txt`) ile birlikte gelir. 