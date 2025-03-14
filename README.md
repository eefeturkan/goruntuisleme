# Görüntü İşleme Uygulaması

Bu uygulama, görüntü işleme dersi için geliştirilmiş bir Python uygulamasıdır. Tkinter kullanılarak oluşturulan arayüz sayesinde çeşitli görüntü işleme teknikleri uygulanabilir.

## Özellikler

1. **Temel İşlemler**
   - Görüntü yükleme ve kaydetme
   - Gri tonlamaya çevirme
   - RGB kanallara ayırma

2. **Görüntü İşleme Teknikleri**
   - Görüntünün negatifini alma
   - Parlaklık ayarlama
   - Eşikleme (Thresholding)
   - Histogram hesaplama ve eşitleme
   - Kontrast ayarlama

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

1. "Görüntü Aç" butonuna tıklayarak bir görüntü dosyası seçin.
2. Sol taraftaki kontrol panelinden istediğiniz görüntü işleme tekniğini seçin.
3. İşlenmiş görüntüyü "Görüntüyü Kaydet" butonu ile kaydedebilirsiniz.

## Gereksinimler

- Python 3.6+
- OpenCV
- NumPy
- Matplotlib
- Pillow (PIL) 