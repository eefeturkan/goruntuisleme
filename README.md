# Görüntü İşleme Uygulaması

Bu uygulama, görüntü işleme dersi için geliştirilmiş kapsamlı bir Python uygulamasıdır. Tkinter kullanılarak oluşturulan arayüz sayesinde çok çeşitli görüntü işleme teknikleri interaktif olarak uygulanabilir. Uygulama, sol ve sağ panellerde gruplandırılmış kontrol butonları ve sağ panelde sekmeli bir yapı ile kullanıcı dostu bir deneyim sunar.


## İçindekiler
- [Özellikler](#özellikler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Gereksinimler](#gereksinimler)
- [Teknik Detaylar](#teknik-detaylar)
- [Katkıda Bulunma](#katkıda-bulunma)
- [Lisans](#lisans)

## Özellikler

**Sol Panel Kontrolleri:**

1.  **Dosya İşlemleri**
    *   Görüntü yükleme (JPG, JPEG, PNG, BMP, GIF)
    *   İşlenmiş görüntüyü kaydetme (PNG, JPG)
2.  **Temel İşlemler**
    *   Orijinal görüntüyü gösterme
    *   Gri tonlamaya çevirme
    *   RGB kanallarına ayırma ve ayrı pencerelerde gösterme
    *   Görüntünün negatifini alma
3.  **Görüntü Ayarları**
    *   Parlaklık ayarlama (-100 ile +100 arası)
    *   Eşikleme (Thresholding) (0-255 arası)
    *   Kontrast ayarlama (0.1 ile 3.0 arası)
4.  **Histogram İşlemleri**
    *   Gri tonlama veya RGB histogramını hesaplama ve ana arayüzde gösterme
    *   Histogram eşitleme (Gri tonlama üzerinden)

**Sağ Panel Kontrolleri (Sekmeli Yapı):**

1.  **Dönüşümler Sekmesi**
    *   Görüntüyü Taşıma (Translation): X ve Y eksenlerinde kaydırma.
    *   Aynalama (Flipping): X ve Y eksenlerinde.
    *   Görüntüyü Eğme (Shearing): X ve Y eksenlerinde.
    *   Görüntüyü Ölçekleme (Scaling/Zoom): X ve Y eksenlerinde farklı oranlarda.
    *   Görüntüyü Döndürme (Rotation): Belirlenen açıda.
    *   Görüntüyü Kırpma (Cropping): Kullanıcı tanımlı dikdörtgen bölge.
    *   Perspektif Düzeltme: Kullanıcının seçtiği 4 nokta ile.
2.  **Mekansal Sekmesi (Mekansal Alan Filtreleri)**
    *   Ortalama Filtresi
    *   Medyan Filtresi
    *   Gaussian Filtresi (Mekansal)
    *   Konservatif Filtre
    *   Crimmins Speckle Gürültü Giderme
    *   Aşındırma (Erosion)
    *   Genişletme (Dilation)
3.  **Frekans Sekmesi (Frekans Alanı Filtreleri)**
    *   Fourier Alçak Geçiren Filtre
    *   Fourier Yüksek Geçiren Filtre
    *   Bant Geçiren Filtre
    *   Bant Durduran Filtre
    *   Butterworth Filtresi (Alçak/Yüksek Geçiren)
    *   Gauss Düşük/Yüksek Geçiren Filtre (Frekans Uzayında)
    *   Homomorfik Filtre
4.  **Kenar Algılama Sekmesi**
    *   Sobel Filtresi
    *   Prewitt Filtresi
    *   Roberts Cross Filtresi
    *   Compass Filtresi
    *   Canny Kenar Algılama (Eşik ayarlı)
    *   Laplace Filtresi
    *   Gabor Filtresi (Parametre ayarlı)
5.  **Gelişmiş Sekmesi (Gelişmiş Görüntü İşleme)**
    *   Hough Dönüşümü (Çizgiler): Parametre ayarlı.
    *   Hough Dönüşümü (Çemberler): Parametre ayarlı.
    *   K-Means Segmentasyon: Küme sayısı (K) ayarlı.

## Kurulum

1.  Depoyu klonlayın veya ZIP olarak indirin:
    ```bash
    git clone https://github.com/kullanici_adiniz/goruntuisleme.git
    cd goruntuisleme
    ```
2.  Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install -r requirements.txt
    ```
3.  Uygulamayı çalıştırın:
    ```bash
    python goruntu_isleme_uygulamasi.py
    ```

## Kullanım

1.  **Görüntü Açma**: Sol paneldeki "Görüntü Aç" butonuna tıklayarak bir görüntü dosyası seçin. Orijinal görüntü ortadaki sol panele, işlenecek/işlenmiş görüntü ise ortadaki sağ panele yüklenir.
2.  **İşlem Seçimi**: Sol paneldeki temel işlemler ve ayarlar için butonları veya kaydırıcıları kullanın. Daha gelişmiş dönüşümler, filtreler ve analizler için sağ paneldeki sekmelerden istediğiniz işlemi seçin.
3.  **Parametre Ayarı**: Birçok işlem (özellikle filtreler ve dönüşümler) tıklandığında ayrı bir diyalog penceresi açarak kullanıcıdan ilgili parametreleri girmesini ister (örn: filtre boyutu, eşik değeri, açı, ölçek faktörü vb.).
4.  **Sonucu İnceleme**: Uygulanan işlemlerin sonucu ortadaki "İşlenmiş Görüntü" panelinde anında görüntülenir. "Histogram Göster" butonu ile mevcut işlenmiş görüntünün histogramı da alt kısımda belirir.
5.  **Sonucu Kaydetme**: İşlenmiş görüntüyü sol paneldeki "Görüntüyü Kaydet" butonu ile farklı formatlarda kaydedebilirsiniz.
6.  **Orijinale Dönme**: Sol paneldeki "Orijinal Görüntü" butonu ile istediğiniz zaman yüklediğiniz ilk görüntüye geri dönebilirsiniz.

## Örnek Uygulamalar

### Görüntüyü Gri Tonlamaya Çevirme
```python
# Gri tonlama işlemi için kullanılan kod parçası
def convert_to_gray(self):
    if self.original_image is None:
        return
        
    # RGB'den gri tonlamaya dönüştür
    gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2GRAY)
    # Gri görüntüyü 3 kanallı RGB'ye dönüştür (gösterim için)
    self.current_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB)
    self.display_image(self.current_image)
```

### Kenar Algılama (Sobel Filtresi)
```python
# Sobel filtresi için kullanılan kod parçası
def apply_sobel_filter(self):
    if self.current_image is None:
        return
        
    gray_image = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2GRAY)
    
    # Sobel filtresi uygula
    grad_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
    
    # Gradyan büyüklüğünü hesapla
    gradient_magnitude = cv2.magnitude(grad_x, grad_y)
    
    # Gradyan büyüklüğünü normalize et
    sobel_output = cv2.normalize(gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    # Tek kanallı görüntüyü 3 kanallı görüntüye dönüştür (gösterim için)
    self.current_image = cv2.cvtColor(sobel_output, cv2.COLOR_GRAY2RGB)
    self.display_image(self.current_image)
```

## Gereksinimler

*   Python 3.x
*   OpenCV-Python (`opencv-python`)
*   NumPy (`numpy`)
*   Matplotlib (`matplotlib`)
*   Pillow (`Pillow`)

Tam sürüm bilgileri için:
```
opencv-python==4.8.0.76
numpy==1.24.3
matplotlib==3.7.2
Pillow==10.0.0
```

## Teknik Detaylar

Uygulama, Nesne Yönelimli Programlama (OOP) prensipleri kullanılarak Python ve Tkinter ile geliştirilmiştir. Tüm görüntü işleme fonksiyonları ve arayüz yönetimi `GoruntuIslemeUygulamasi` sınıfı içerisinde metotlar olarak düzenlenmiştir. Görüntü verileri için NumPy dizileri, temel görüntü manipülasyonları ve algoritmalar için OpenCV, histogram ve bazı grafiksel gösterimler için Matplotlib, arayüz için ise Tkinter (ve `ttk` modülü) kullanılmıştır.

Uygulama ayrıca, temel görüntü işleme kavramlarını ve OpenCV kullanımlarını açıklayan bir metin dosyası (`goruntu_isleme_temel_bilgiler.txt`) ile birlikte gelir. Bu dosya, uygulamadaki birçok işlemin teorik altyapısı ve basit kod örnekleri hakkında bilgi içerir.

### Uygulama Mimarisi

```
goruntuisleme/
│
├── goruntu_isleme_uygulamasi.py  # Ana uygulama dosyası
├── requirements.txt              # Bağımlılıklar
├── README.md                     # Bu belge
└── goruntu_isleme_temel_bilgiler.txt  # Teorik bilgiler ve örnekler
```

