import os
import tkinter as tk
from tkinter import filedialog, Scale, Label, Button, Frame, HORIZONTAL, RIDGE, SUNKEN, RAISED, LEFT
from tkinter import ttk
from tkinter import messagebox  # Hata mesajları için messagebox modülünü import et
from PIL import Image, ImageTk
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

"""
GÖRÜNTÜ İŞLEME UYGULAMASI
-------------------------

Bu uygulama, görüntü işleme işlemlerini yapabilen bir Python uygulamasıdır.
Nesne Yönelimli Programlama (OOP) yaklaşımı kullanılarak oluşturulmuştur.

Nesne Yönelimli Programlama, kodu sınıflar içinde düzenleyerek daha organize, 
bakımı kolay ve yeniden kullanılabilir kod yazmayı sağlar. Prosedürel programlamada
sadece fonksiyonlar kullanılırken, OOP'de sınıflar (class) ve nesneler (object) kullanılır.

Temel OOP Kavramları:
1. Sınıf (Class): Nesnelerin şablonunu tanımlayan yapıdır.
2. Nesne (Object): Sınıftan türetilen örneğe denir.
3. self: Sınıfın kendisini temsil eden bir referanstır. Sınıf metodlarının ilk parametresi olmalıdır.
4. __init__: Yapıcı metod (constructor) olarak adlandırılır ve nesne oluşturulduğunda otomatik çalışır.
5. Metod: Sınıfa ait fonksiyonlardır.

Bu uygulamada, GoruntuIslemeUygulamasi adlı bir sınıf tanımlanmış ve bu sınıf içerisinde
görüntü işleme methodları yer almaktadır.
"""

class GoruntuIslemeUygulamasi:
    """
    GoruntuIslemeUygulamasi sınıfı, görüntü işleme uygulamamızın tüm işlevlerini içerir.
    Bir sınıf, ilişkili verileri ve metodları bir arada tutan bir yapıdır.
    """
    
    def __init__(self, root):
        """
        __init__ metodu, sınıfın yapıcı metodudur (constructor).
        Nesne oluşturulduğunda otomatik olarak çağrılır ve nesnenin başlangıç durumunu ayarlar.
        
        self parametresi, sınıfın kendisine referans verir. Python'da tüm sınıf metodları
        ilk parametre olarak self almalıdır. Bu, metodun hangi nesne üzerinde çalıştığını belirtir.
        
        root parametresi, Tkinter uygulamasının ana penceresini temsil eder.
        
        Parametreler:
            root (tk.Tk): Tkinter ana penceresi
        """
        # Ana pencereyi sınıf değişkeni olarak saklıyoruz
        self.root = root
        self.root.title("Görüntü İşleme Uygulaması")
        self.root.geometry("1280x900")  # Pencerenin boyutunu artırıyoruz
        self.root.configure(bg="#f0f0f0")  # Arka plan rengini ayarlıyoruz
        
        # Ana görüntü değişkenleri - bunlar sınıf içinde her yerden erişilebilir değişkenlerdir
        self.original_image = None  # Orijinal görüntü verisini saklar
        self.current_image = None   # Şu anki (işlenmiş) görüntü verisini saklar
        self.file_path = None       # Açılan dosyanın yolunu saklar
        
        # Arayüz bileşenlerini oluştur - create_widgets metodunu çağırarak UI elemanlarını oluşturuyoruz
        self.create_widgets()
        
    def create_widgets(self):
        """
        Uygulama arayüzünün tüm görsel bileşenlerini oluşturan metod.
        Ana çerçeveleri, görüntü gösterme alanlarını ve kontrol butonlarını oluşturur.
        
        Tkinter, grafik arayüz oluşturmak için kullanılan standart Python kütüphanesidir.
        Frame, Label, Button gibi bileşenler Tkinter'ın temel arayüz elemanlarıdır.
        """
        # Ana çerçeveler - Sol ve sağ ana bölümleri oluşturuyoruz
        # Frame: Diğer bileşenleri gruplamak için kullanılan konteyner
        # relief: Çerçeve kenarlığının görünümü (RIDGE, SUNKEN, RAISED vb.)
        # borderwidth: Kenarlık kalınlığı
        
        # Sol panel için bir canvas ve scrollbar oluşturuyoruz
        self.left_outer_frame = Frame(self.root, width=300, bg="#e0e0e0", relief=RIDGE, borderwidth=2)
        self.left_outer_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Sol panele kaydırma çubuğu ekle
        self.left_scrollbar = tk.Scrollbar(self.left_outer_frame, orient="vertical")
        self.left_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Canvas oluştur ve scrollbar'a bağla
        self.left_canvas = tk.Canvas(self.left_outer_frame, bg="#e0e0e0", 
                                   yscrollcommand=self.left_scrollbar.set)
        self.left_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.left_scrollbar.config(command=self.left_canvas.yview)
        
        # Canvas içine konulacak frame oluştur
        self.left_frame = Frame(self.left_canvas, bg="#e0e0e0")
        self.left_canvas.create_window((0, 0), window=self.left_frame, anchor="nw")
        
        # Sağ çerçeve oluştur
        self.right_frame = Frame(self.root, bg="#e0e0e0", relief=RIDGE, borderwidth=2)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Görüntü gösterme alanı - İşlenen görüntünün gösterileceği bölüm
        self.image_frame = Frame(self.right_frame, bg="white", relief=SUNKEN, borderwidth=2)
        self.image_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Label: Metin veya görüntü göstermek için kullanılan bileşen
        self.image_label = Label(self.image_frame, bg="white")
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        # Histogram gösterme alanı - Görüntü histogramının gösterileceği bölüm
        self.histogram_frame = Frame(self.right_frame, height=200, bg="white", relief=SUNKEN, borderwidth=2)
        self.histogram_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Kontrol butonları - Sol paneldeki tüm butonları oluşturan metodu çağırıyoruz
        self.create_control_buttons()
        
        # Sol panelin boyutlarını güncelle
        self.left_frame.update_idletasks()
        self.left_canvas.config(scrollregion=self.left_canvas.bbox("all"))
        self.left_canvas.config(width=280, height=700)  # Canvas boyutlarını ayarla
        
    def create_control_buttons(self):
        """
        Sol panelde yer alan tüm kontrol butonlarını ve arayüz elemanlarını oluşturan metod.
        Dosya işlemleri, temel görüntü işleme, parlaklık, eşikleme, histogram ve kontrast
        ayarları için gerekli butonları ve kaydırıcıları oluşturur.
        """
        # Dosya işlemleri bölümü
        file_frame = Frame(self.left_frame, bg="#e0e0e0", relief=RAISED, borderwidth=1)
        file_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Başlık etiketi
        Label(file_frame, text="Dosya İşlemleri", bg="#e0e0e0", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Butonlar - command parametresi, butona tıklandığında çağrılacak metodu belirtir
        Button(file_frame, text="Görüntü Aç", command=self.open_image, width=20).pack(pady=2)
        Button(file_frame, text="Görüntüyü Kaydet", command=self.save_image, width=20).pack(pady=2)
        
        # Temel işlemler bölümü
        basic_frame = Frame(self.left_frame, bg="#e0e0e0", relief=RAISED, borderwidth=1)
        basic_frame.pack(fill=tk.X, padx=5, pady=5)
        
        Label(basic_frame, text="Temel İşlemler", bg="#e0e0e0", font=("Arial", 10, "bold")).pack(pady=5)
        
        Button(basic_frame, text="Orijinal Görüntü", command=self.show_original, width=20).pack(pady=2)
        Button(basic_frame, text="Gri Tonlama", command=self.convert_to_gray, width=20).pack(pady=2)
        Button(basic_frame, text="RGB Kanallara Ayır", command=self.split_channels, width=20).pack(pady=2)
        Button(basic_frame, text="Negatif", command=self.negative_image, width=20).pack(pady=2)
        
        # Parlaklık ayarı bölümü
        brightness_frame = Frame(self.left_frame, bg="#e0e0e0", relief=RAISED, borderwidth=1)
        brightness_frame.pack(fill=tk.X, padx=5, pady=5)
        
        Label(brightness_frame, text="Parlaklık Ayarı", bg="#e0e0e0", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Scale: Kaydırıcı bileşeni, değer aralığı belirterek kullanıcıdan sayısal değer almak için kullanılır
        # from_: Minimum değer, to: Maksimum değer, orient: Kaydırıcının yönü
        # command: Değer değiştiğinde çağrılacak metod
        self.brightness_scale = Scale(brightness_frame, from_=-100, to=100, orient=HORIZONTAL, 
                                     command=self.adjust_brightness, length=200)
        self.brightness_scale.set(0)  # Başlangıç değerini 0 olarak ayarla
        self.brightness_scale.pack(pady=2)
        
        # Eşikleme bölümü
        threshold_frame = Frame(self.left_frame, bg="#e0e0e0", relief=RAISED, borderwidth=1)
        threshold_frame.pack(fill=tk.X, padx=5, pady=5)
        
        Label(threshold_frame, text="Eşikleme", bg="#e0e0e0", font=("Arial", 10, "bold")).pack(pady=5)
        
        self.threshold_scale = Scale(threshold_frame, from_=0, to=255, orient=HORIZONTAL, 
                                    command=self.apply_threshold, length=200)
        self.threshold_scale.set(127)  # Başlangıç değerini 127 olarak ayarla (orta değer)
        self.threshold_scale.pack(pady=2)
        
        # Histogram işlemleri bölümü
        histogram_frame = Frame(self.left_frame, bg="#e0e0e0", relief=RAISED, borderwidth=1)
        histogram_frame.pack(fill=tk.X, padx=5, pady=5)
        
        Label(histogram_frame, text="Histogram İşlemleri", bg="#e0e0e0", font=("Arial", 10, "bold")).pack(pady=5)
        
        Button(histogram_frame, text="Histogram Göster", command=self.show_histogram, width=20).pack(pady=2)
        Button(histogram_frame, text="Histogram Eşitleme", command=self.equalize_histogram, width=20).pack(pady=2)
        
        # Kontrast ayarı bölümü
        contrast_frame = Frame(self.left_frame, bg="#e0e0e0", relief=RAISED, borderwidth=1)
        contrast_frame.pack(fill=tk.X, padx=5, pady=5)
        
        Label(contrast_frame, text="Kontrast Ayarı", bg="#e0e0e0", font=("Arial", 10, "bold")).pack(pady=5)
        
        # resolution: Kaydırıcının adım büyüklüğü
        self.contrast_scale = Scale(contrast_frame, from_=0.1, to=3.0, resolution=0.1, orient=HORIZONTAL, 
                                   command=self.adjust_contrast, length=200)
        self.contrast_scale.set(1.0)  # Başlangıç değerini 1.0 olarak ayarla (normal kontrast)
        self.contrast_scale.pack(pady=2)
        
        # Görüntü Dönüşümleri bölümü
        transforms_frame = Frame(self.left_frame, bg="#e0e0e0", relief=RAISED, borderwidth=1)
        transforms_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Başlığı normal tema ile aynı yap
        Label(transforms_frame, text="Görüntü Dönüşümleri", bg="#e0e0e0", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Taşıma işlemi için buton
        Button(transforms_frame, text="Görüntüyü Taşı", command=self.open_translation_dialog, 
            width=20).pack(pady=2)
        
        # Aynalama işlemleri için butonlar
        Button(transforms_frame, text="X Ekseninde Aynala", command=self.flip_horizontal, 
            width=20).pack(pady=2)
        Button(transforms_frame, text="Y Ekseninde Aynala", command=self.flip_vertical, 
            width=20).pack(pady=2)
        
        # Eğme (Shearing) işlemi için buton
        Button(transforms_frame, text="Görüntüyü Eğ", command=self.open_shearing_dialog, 
            width=20).pack(pady=2)
            
        # Ölçekleme (Zoom in/out) işlemi için buton
        Button(transforms_frame, text="Görüntüyü Ölçekle", command=self.open_scaling_dialog, 
            width=20).pack(pady=2)
            
        # Döndürme (Rotation) işlemi için buton
        Button(transforms_frame, text="Görüntüyü Döndür", command=self.open_rotation_dialog, 
            width=20).pack(pady=2)
            
        # Kırpma (Cropping) işlemi için buton
        Button(transforms_frame, text="Görüntüyü Kırp", command=self.open_cropping_dialog, 
            width=20).pack(pady=2)
        
    def open_image(self):
        """
        Dosya seçme dialogu açarak bir görüntü dosyası seçmeyi ve yüklemeyi sağlar.
        
        filedialog.askopenfilename: Dosya seçme dialogu açan Tkinter fonksiyonu
        cv2.imread: OpenCV kütüphanesinde görüntü dosyasını okumak için kullanılan fonksiyon
        cv2.cvtColor: OpenCV'de renk dönüşümü yapmak için kullanılan fonksiyon
        
        Not: OpenCV görüntüleri BGR formatında okurken, 
        çoğu uygulama (ve bizim Tkinter arayüzümüz) RGB formatını kullanır. 
        Bu yüzden BGR'den RGB'ye dönüşüm yapıyoruz.
        """
        # Dosya seçme dialogu aç ve desteklenen formatları belirt
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        
        if file_path:
            self.file_path = file_path
            # OpenCV ile görüntüyü oku - OpenCV görüntüleri NumPy dizisi olarak yükler
            self.original_image = cv2.imread(file_path)
            # BGR'den RGB'ye dönüştür (OpenCV BGR kullanır, ama biz RGB göstermek istiyoruz)
            self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            self.current_image = self.original_image.copy()  # İşlenecek görüntü için kopya oluştur
            self.display_image(self.current_image)  # Görüntüyü arayüzde göster
            
    def save_image(self):
        """
        Mevcut işlenmiş görüntüyü bir dosyaya kaydetmeyi sağlar.
        
        filedialog.asksaveasfilename: Dosya kaydetme dialogu açan Tkinter fonksiyonu
        cv2.imwrite: OpenCV kütüphanesinde görüntüyü dosyaya yazmak için kullanılan fonksiyon
        """
        if self.current_image is None:
            return
            
        # Dosya kaydetme dialogu aç
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if file_path:
            # RGB'den BGR'ye dönüştür (OpenCV BGR formatında kaydeder)
            save_image = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(file_path, save_image)  # Görüntüyü dosyaya kaydet
            
    def display_image(self, image):
        """
        Verilen görüntüyü arayüzde gösterir. Görüntüyü uygun boyuta getirir
        ve Tkinter Label'ına yerleştirir.
        
        cv2.resize: OpenCV'de görüntü boyutlandırma için kullanılan fonksiyon
        PIL.Image.fromarray: NumPy dizisini PIL Image nesnesine dönüştürür
        ImageTk.PhotoImage: PIL Image'i Tkinter'da gösterilebilir formata çevirir
        
        Parametreler:
            image (numpy.ndarray): Gösterilecek görüntü (RGB formatlı NumPy dizisi)
        """
        if image is None:
            return
            
        # Görüntüyü yeniden boyutlandır - Eğer görüntü çok büyükse, ekrana sığdırmak için küçültüyoruz
        h, w = image.shape[:2]  # Görüntünün yükseklik ve genişliğini al
        max_size = 700  # Maksimum boyut
        
        if h > max_size or w > max_size:
            # En-boy oranını koru
            if h > w:
                new_h, new_w = max_size, int(w * max_size / h)
            else:
                new_h, new_w = int(h * max_size / w), max_size
                
            display_img = cv2.resize(image, (new_w, new_h))  # Görüntüyü yeniden boyutlandır
        else:
            display_img = image.copy()
            
        # NumPy dizisini PIL Image'e dönüştür
        pil_img = Image.fromarray(display_img)
        # PIL Image'i Tkinter PhotoImage'e dönüştür
        tk_img = ImageTk.PhotoImage(pil_img)
        
        # Görüntüyü Label'a yerleştir
        self.image_label.configure(image=tk_img)
        self.image_label.image = tk_img  # Referansı koru (Python'un çöp toplayıcısı silmesin diye)
        
    def show_original(self):
        """
        Orijinal görüntüyü gösterir. İşlenmiş görüntüden sonra
        orijinal görüntüye dönmek için kullanılır.
        """
        if self.original_image is not None:
            self.current_image = self.original_image.copy()  # Orijinalin kopyasını al
            self.display_image(self.current_image)  # Görüntüyü göster
            
    def convert_to_gray(self):
        """
        Görüntüyü gri tonlamalı hale dönüştürür.
        
        cv2.cvtColor: OpenCV'de renk dönüşümü için kullanılan fonksiyon
        COLOR_RGB2GRAY: RGB'den gri tonlamaya dönüşüm sabiti
        COLOR_GRAY2RGB: Gri tonlamadan RGB'ye dönüşüm sabiti (gösterim için)
        
        Not: OpenCV'de gri tonlamalı görüntüler tek kanallıdır, ama
        gösterim için genellikle 3 kanallı RGB'ye dönüştürülür.
        """
        if self.original_image is None:
            return
            
        # RGB'den gri tonlamaya dönüştür
        gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2GRAY)
        # Gri görüntüyü 3 kanallı RGB'ye dönüştür (gösterim için)
        # Bu dönüşüm sadece görselleştirme içindir - her kanal aynı değeri alır
        self.current_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB)
        self.display_image(self.current_image)
        
    def split_channels(self):
        """
        Görüntüyü R, G, B (Kırmızı, Yeşil, Mavi) kanallarına ayırır ve
        her bir kanalı ayrı bir pencerede gösterir.
        
        cv2.split: Çok kanallı bir görüntüyü ayrı kanallara ayıran OpenCV fonksiyonu
        np.zeros_like: Belirtilen dizi gibi sıfırlardan oluşan bir dizi oluşturan NumPy fonksiyonu
        Toplevel: Tkinter'da yeni bir pencere oluşturmak için kullanılan sınıf
        """
        if self.original_image is None:
            return
            
        # Yeni pencere oluştur
        channels_window = tk.Toplevel(self.root)
        channels_window.title("RGB Kanalları")
        channels_window.geometry("800x600")
        
        # Kanalları ayır - r, g, b tek kanallı (2B) görüntülerdir
        r, g, b = cv2.split(self.original_image)
        
        # Tek kanallı görüntüleri 3 kanallı görüntülere dönüştür
        # Her kanalı kendi renginde göstermek için:
        r_img = np.zeros_like(self.original_image)  # Orijinal boyutunda sıfır dizisi
        g_img = np.zeros_like(self.original_image)
        b_img = np.zeros_like(self.original_image)
        
        # Her kanalı kendi pozisyonuna yerleştir (RGB formatında)
        r_img[:,:,0] = r  # Kırmızı kanal, RGB'nin ilk kanalına (indeks 0)
        g_img[:,:,1] = g  # Yeşil kanal, RGB'nin ikinci kanalına (indeks 1)
        b_img[:,:,2] = b  # Mavi kanal, RGB'nin üçüncü kanalına (indeks 2)
        
        # Görüntüleri göster - Her kanal için bir çerçeve ve etiket oluştur
        frame_r = Frame(channels_window)
        frame_r.pack(side=tk.LEFT, padx=5, pady=5)
        Label(frame_r, text="R Kanalı").pack()
        
        frame_g = Frame(channels_window)
        frame_g.pack(side=tk.LEFT, padx=5, pady=5)
        Label(frame_g, text="G Kanalı").pack()
        
        frame_b = Frame(channels_window)
        frame_b.pack(side=tk.LEFT, padx=5, pady=5)
        Label(frame_b, text="B Kanalı").pack()
        
        # Görüntüleri PIL ve Tkinter formatına dönüştür
        pil_r = Image.fromarray(r_img)
        pil_g = Image.fromarray(g_img)
        pil_b = Image.fromarray(b_img)
        
        # Yeniden boyutlandır - Tüm görüntüleri aynı boyuta getir
        pil_r = pil_r.resize((200, 200))
        pil_g = pil_g.resize((200, 200))
        pil_b = pil_b.resize((200, 200))
        
        # PIL görüntülerini Tkinter Photo Image'e dönüştür
        tk_r = ImageTk.PhotoImage(pil_r)
        tk_g = ImageTk.PhotoImage(pil_g)
        tk_b = ImageTk.PhotoImage(pil_b)
        
        # Etiketlere yerleştir
        label_r = Label(frame_r, image=tk_r)
        label_r.image = tk_r  # Referansı koru
        label_r.pack()
        
        label_g = Label(frame_g, image=tk_g)
        label_g.image = tk_g  # Referansı koru
        label_g.pack()
        
        label_b = Label(frame_b, image=tk_b)
        label_b.image = tk_b  # Referansı koru
        label_b.pack()
        
    def negative_image(self):
        """
        Görüntünün negatifini alır. Her piksel değerini 255'ten çıkararak
        renkleri tersine çevirir. Siyah beyaz olur, beyaz siyah olur.
        
        Görüntü negatifi, medikal görüntülemede, film fotoğrafçılığında ve
        bazı görüntü işleme uygulamalarında kullanılır.
        """
        if self.original_image is None:
            return
            
        # 255'ten çıkararak negatif al
        self.current_image = 255 - self.original_image
        self.display_image(self.current_image)
        
    def adjust_brightness(self, val):
        """
        Görüntünün parlaklığını ayarlar. Pozitif değerler parlaklığı artırır,
        negatif değerler azaltır.
        
        cv2.add: İki diziyi toplayan OpenCV fonksiyonu
        cv2.subtract: Bir diziden başka bir diziyi çıkaran OpenCV fonksiyonu
        np.ones_like: Belirtilen dizi gibi birlerden oluşan bir dizi oluşturan NumPy fonksiyonu
        
        Parametreler:
            val (str): Kaydırıcıdan gelen değer (string olarak)
        """
        if self.original_image is None:
            return
            
        brightness = int(val)  # String'i integer'a dönüştür
        if brightness > 0:
            # Parlaklığı artır: Her piksele sabit bir değer ekle
            self.current_image = cv2.add(self.original_image, np.ones_like(self.original_image) * brightness)
        else:
            # Parlaklığı azalt: Her pikselden sabit bir değer çıkar
            self.current_image = cv2.subtract(self.original_image, np.ones_like(self.original_image) * abs(brightness))
            
        self.display_image(self.current_image)
        
    def apply_threshold(self, val):
        """
        Görüntüye eşikleme (thresholding) uygular. Piksel değeri eşik değerinden
        büyükse beyaz (255), küçükse siyah (0) yaparak ikili (binary) görüntü oluşturur.
        
        cv2.threshold: Görüntüye eşikleme uygulayan OpenCV fonksiyonu
        THRESH_BINARY: İkili eşikleme türü - eşiğin üstü 255, altı 0 olur
        
        Parametreler:
            val (str): Kaydırıcıdan gelen eşik değeri (string olarak)
        """
        if self.original_image is None:
            return
            
        threshold = int(val)  # String'i integer'a dönüştür
        # Görüntüyü gri tonlamaya çevir (eşikleme için)
        gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2GRAY)
        # Eşikleme uygula
        # _: İlk dönüş değeri eşik değeri, biz onu kullanmadığımız için _ ile göz ardı ediyoruz
        _, thresholded = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
        
        # Tek kanallı görüntüyü 3 kanallı görüntüye dönüştür (gösterim için)
        self.current_image = cv2.cvtColor(thresholded, cv2.COLOR_GRAY2RGB)
        self.display_image(self.current_image)
        
    def show_histogram(self):
        """
        Mevcut görüntünün histogramını hesaplar ve gösterir.
        Histogram, bir görüntüdeki piksel yoğunluklarının dağılımını gösterir.
        
        cv2.calcHist: Histogram hesaplayan OpenCV fonksiyonu
        matplotlib: Grafik çizmek için kullanılan Python kütüphanesi
        FigureCanvasTkAgg: Matplotlib figürünü Tkinter'a entegre etmek için kullanılır
        """
        if self.original_image is None:
            return
            
        # Histogram çerçevesini temizle
        for widget in self.histogram_frame.winfo_children():
            widget.destroy()
            
        # Matplotlib figürü oluştur
        fig = plt.Figure(figsize=(10, 2), dpi=100)
        ax = fig.add_subplot(111)  # 1x1 grid, 1. pozisyon
        
        # Gri tonlamalı görüntü için histogram
        # np.array_equal: İki dizinin eşit olup olmadığını kontrol eden NumPy fonksiyonu
        # Eğer tüm kanallar aynıysa, görüntü gri tonlamalıdır
        if len(self.current_image.shape) == 2 or (len(self.current_image.shape) == 3 and np.array_equal(self.current_image[:,:,0], self.current_image[:,:,1]) and np.array_equal(self.current_image[:,:,0], self.current_image[:,:,2])):
            gray_img = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2GRAY) if len(self.current_image.shape) == 3 else self.current_image
            hist = cv2.calcHist([gray_img], [0], None, [256], [0, 256])
            ax.plot(hist, color='black')
            ax.set_xlim([0, 256])
            ax.set_title('Gri Tonlama Histogramı')
        else:
            # Renkli görüntü için histogram - Her kanal için ayrı histogram
            colors = ('r', 'g', 'b')
            for i, color in enumerate(colors):
                hist = cv2.calcHist([self.current_image], [i], None, [256], [0, 256])
                ax.plot(hist, color=color)
            ax.set_xlim([0, 256])
            ax.set_title('RGB Histogramı')
            
        # Figürü Tkinter'a ekle
        canvas = FigureCanvasTkAgg(fig, master=self.histogram_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def equalize_histogram(self):
        """
        Histogram eşitleme uygular. Bu işlem, görüntünün kontrastını artırır
        ve detayları daha görünür hale getirir.
        
        cv2.equalizeHist: Histogram eşitleme uygulayan OpenCV fonksiyonu
        
        Histogram eşitleme, tıbbi görüntüleme, uydu görüntüleri ve
        düşük kontrastlı fotoğrafları iyileştirmek için kullanılır.
        """
        if self.original_image is None:
            return
            
        # Görüntüyü gri tonlamaya çevir (histogram eşitleme tek kanallı görüntüler için çalışır)
        gray_img = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2GRAY)
        
        # Histogram eşitleme uygula
        equalized = cv2.equalizeHist(gray_img)
        
        # Tek kanallı görüntüyü 3 kanallı görüntüye dönüştür (gösterim için)
        self.current_image = cv2.cvtColor(equalized, cv2.COLOR_GRAY2RGB)
        self.display_image(self.current_image)
        
        # Histogramı göster
        self.show_histogram()
        
    def adjust_contrast(self, val):
        """
        Görüntünün kontrastını ayarlar. 1.0'dan büyük değerler kontrastı artırır,
        küçük değerler azaltır.
        
        cv2.convertScaleAbs: Piksel değerlerini ölçeklendiren ve mutlak değer alan OpenCV fonksiyonu
        alpha: Kontrast faktörü (çarpan)
        beta: Parlaklık faktörü (toplam)
        
        Parametreler:
            val (str): Kaydırıcıdan gelen kontrast değeri (string olarak)
        """
        if self.original_image is None:
            return
            
        contrast = float(val)  # String'i float'a dönüştür
        # convertScaleAbs fonksiyonu: f(x) = alpha*x + beta
        # alpha: kontrast faktörü, beta: parlaklık faktörü (burada 0)
        self.current_image = cv2.convertScaleAbs(self.original_image, alpha=contrast, beta=0)
        self.display_image(self.current_image)
    
    def open_translation_dialog(self):
        """
        Görüntüyü taşımak için bir dialog penceresi açar. Bu dialog, kullanıcının 
        görüntüyü x ve y eksenlerinde ne kadar taşımak istediğini belirlemesini sağlar.
        
        Taşıma (translation), görüntünün tüm piksellerini belirli bir miktarda x ve y 
        yönünde kaydırma işlemidir.
        """
        if self.original_image is None:
            return
            
        # Yeni bir dialog penceresi oluştur
        translation_dialog = tk.Toplevel(self.root)
        translation_dialog.title("Görüntüyü Taşı")
        translation_dialog.geometry("300x200")
        translation_dialog.resizable(False, False)
        
        # X ekseninde taşıma için kaydırıcı
        Label(translation_dialog, text="X Ekseninde Taşıma:").pack(pady=5)
        x_scale = Scale(translation_dialog, from_=-100, to=100, orient=HORIZONTAL, length=200)
        x_scale.set(0)
        x_scale.pack(pady=5)
        
        # Y ekseninde taşıma için kaydırıcı
        Label(translation_dialog, text="Y Ekseninde Taşıma:").pack(pady=5)
        y_scale = Scale(translation_dialog, from_=-100, to=100, orient=HORIZONTAL, length=200)
        y_scale.set(0)
        y_scale.pack(pady=5)
        
        # Uygula butonu
        def apply_translation():
            tx = x_scale.get()  # X taşıma miktarı
            ty = y_scale.get()  # Y taşıma miktarı
            self.translate_image(tx, ty)
            translation_dialog.destroy()  # Dialog penceresini kapat
            
        Button(translation_dialog, text="Uygula", command=apply_translation).pack(pady=10)
    
    def translate_image(self, tx, ty):
        """
        Görüntüyü belirtilen miktarda x ve y eksenlerinde taşır.
        
        cv2.warpAffine: Görüntüye afin dönüşümü uygulayan OpenCV fonksiyonu
        np.float32: 32-bit kayan noktalı sayı türünde NumPy dizisi oluşturur
        
        Parametreler:
            tx (int): X ekseninde taşıma miktarı
            ty (int): Y ekseninde taşıma miktarı
        """
        if self.original_image is None:
            return
            
        # Görüntü boyutları
        h, w = self.original_image.shape[:2]
        
        # Taşıma matrisi oluştur [ [1, 0, tx], [0, 1, ty] ]
        # İlk parametre 2x3'lük bir matris olmalı
        M = np.float32([[1, 0, tx], [0, 1, ty]])
        
        # Görüntüyü taşı
        self.current_image = cv2.warpAffine(self.original_image, M, (w, h))
        self.display_image(self.current_image)
    
    def flip_horizontal(self):
        """
        Görüntüyü yatay eksende aynalar (x eksenine göre çevirir).
        Bu işlem, görüntüyü soldan sağa ters çevirir.
        
        cv2.flip: Görüntüyü belirtilen eksende çeviren OpenCV fonksiyonu
        flipCode = 1: Yatay eksende aynalama
        """
        if self.original_image is None:
            return
            
        # Görüntüyü yatay eksende aynala (flipCode = 1)
        self.current_image = cv2.flip(self.original_image, 1)
        self.display_image(self.current_image)
    
    def flip_vertical(self):
        """
        Görüntüyü dikey eksende aynalar (y eksenine göre çevirir).
        Bu işlem, görüntüyü yukarıdan aşağıya ters çevirir.
        
        cv2.flip: Görüntüyü belirtilen eksende çeviren OpenCV fonksiyonu
        flipCode = 0: Dikey eksende aynalama
        """
        if self.original_image is None:
            return
            
        # Görüntüyü dikey eksende aynala (flipCode = 0)
        self.current_image = cv2.flip(self.original_image, 0)
        self.display_image(self.current_image)
    
    def open_shearing_dialog(self):
        """
        Görüntüyü eğmek (shearing) için bir dialog penceresi açar. Bu dialog,
        kullanıcının görüntüyü x ve y eksenlerinde ne kadar eğmek istediğini belirlemesini sağlar.
        
        Eğme (shearing), görüntünün bir tarafını sabit tutarken, diğer tarafını
        kaydırma işlemidir. Bu, görüntüyü parallelogram şekline dönüştürür.
        """
        if self.original_image is None:
            return
            
        # Yeni bir dialog penceresi oluştur
        shearing_dialog = tk.Toplevel(self.root)
        shearing_dialog.title("Görüntüyü Eğ")
        shearing_dialog.geometry("300x200")
        shearing_dialog.resizable(False, False)
        
        # X ekseninde eğme için kaydırıcı
        Label(shearing_dialog, text="X Ekseninde Eğme:").pack(pady=5)
        x_scale = Scale(shearing_dialog, from_=-0.5, to=0.5, resolution=0.1, orient=HORIZONTAL, length=200)
        x_scale.set(0)
        x_scale.pack(pady=5)
        
        # Y ekseninde eğme için kaydırıcı
        Label(shearing_dialog, text="Y Ekseninde Eğme:").pack(pady=5)
        y_scale = Scale(shearing_dialog, from_=-0.5, to=0.5, resolution=0.1, orient=HORIZONTAL, length=200)
        y_scale.set(0)
        y_scale.pack(pady=5)
        
        # Uygula butonu
        def apply_shearing():
            sx = float(x_scale.get())  # X eğme miktarı
            sy = float(y_scale.get())  # Y eğme miktarı
            self.shear_image(sx, sy)
            shearing_dialog.destroy()  # Dialog penceresini kapat
            
        Button(shearing_dialog, text="Uygula", command=apply_shearing).pack(pady=10)
    
    def shear_image(self, sx, sy):
        """
        Görüntüyü belirtilen miktarda x ve y eksenlerinde eğer.
        
        cv2.warpAffine: Görüntüye afin dönüşümü uygulayan OpenCV fonksiyonu
        cv2.getAffineTransform: 3 kontrol noktası kullanarak afin dönüşüm matrisi oluşturan OpenCV fonksiyonu
        
        Parametreler:
            sx (float): X ekseninde eğme miktarı
            sy (float): Y ekseninde eğme miktarı
        """
        if self.original_image is None:
            return
            
        # Görüntü boyutları
        h, w = self.original_image.shape[:2]
        
        # Eğme matrisi oluştur
        M = np.float32([[1, sx, 0], [sy, 1, 0]])
        
        # Görüntüyü eğ
        self.current_image = cv2.warpAffine(self.original_image, M, (w, h))
        self.display_image(self.current_image)
    
    def open_scaling_dialog(self):
        """
        Görüntüyü ölçeklemek (zoom in/out) için bir dialog penceresi açar.
        Bu dialog, kullanıcının görüntüyü x ve y eksenlerinde ne oranda 
        büyütmek veya küçültmek istediğini belirlemesini sağlar.
        
        Ölçekleme (scaling), görüntünün boyutunu değiştirme işlemidir.
        """
        if self.original_image is None:
            return
            
        # Yeni bir dialog penceresi oluştur
        scaling_dialog = tk.Toplevel(self.root)
        scaling_dialog.title("Görüntüyü Ölçekle")
        scaling_dialog.geometry("300x200")
        scaling_dialog.resizable(False, False)
        
        # X ekseninde ölçekleme için kaydırıcı
        Label(scaling_dialog, text="X Ekseninde Ölçek:").pack(pady=5)
        x_scale = Scale(scaling_dialog, from_=0.1, to=3.0, resolution=0.1, orient=HORIZONTAL, length=200)
        x_scale.set(1.0)  # Başlangıç değeri: 1.0 (orijinal boyut)
        x_scale.pack(pady=5)
        
        # Y ekseninde ölçekleme için kaydırıcı
        Label(scaling_dialog, text="Y Ekseninde Ölçek:").pack(pady=5)
        y_scale = Scale(scaling_dialog, from_=0.1, to=3.0, resolution=0.1, orient=HORIZONTAL, length=200)
        y_scale.set(1.0)  # Başlangıç değeri: 1.0 (orijinal boyut)
        y_scale.pack(pady=5)
        
        # Uygula butonu
        def apply_scaling():
            sx = float(x_scale.get())  # X ölçekleme oranı
            sy = float(y_scale.get())  # Y ölçekleme oranı
            self.scale_image(sx, sy)
            scaling_dialog.destroy()  # Dialog penceresini kapat
            
        Button(scaling_dialog, text="Uygula", command=apply_scaling).pack(pady=10)
    
    def scale_image(self, sx, sy):
        """
        Görüntüyü belirtilen oranda ölçekler (büyütür veya küçültür).
        
        cv2.resize: Görüntüyü yeniden boyutlandıran OpenCV fonksiyonu
        interpolation: Yeniden boyutlandırma işleminde kullanılacak interpolasyon yöntemi
        
        Parametreler:
            sx (float): X ekseninde ölçekleme oranı
            sy (float): Y ekseninde ölçekleme oranı
        """
        if self.original_image is None:
            return
            
        # Görüntü boyutları
        h, w = self.original_image.shape[:2]
        
        # Yeni boyutları hesapla
        new_w = int(w * sx)
        new_h = int(h * sy)
        
        # Görüntüyü ölçekle (yeniden boyutlandır)
        # Büyütme işlemi için cv2.INTER_CUBIC, küçültme işlemi için cv2.INTER_AREA önerilir
        interpolation = cv2.INTER_CUBIC if sx > 1 or sy > 1 else cv2.INTER_AREA
        self.current_image = cv2.resize(self.original_image, (new_w, new_h), interpolation=interpolation)
        self.display_image(self.current_image)
    
    def open_rotation_dialog(self):
        """
        Görüntüyü döndürmek için bir dialog penceresi açar.
        Bu dialog, kullanıcının görüntüyü belirli bir açıda döndürmesini sağlar.
        
        Döndürme (rotation), görüntüyü belirli bir merkez etrafında 
        belirli bir açıda çevirme işlemidir.
        """
        if self.original_image is None:
            return
            
        # Yeni bir dialog penceresi oluştur
        rotation_dialog = tk.Toplevel(self.root)
        rotation_dialog.title("Görüntüyü Döndür")
        rotation_dialog.geometry("300x150")
        rotation_dialog.resizable(False, False)
        
        # Açı seçimi için kaydırıcı
        Label(rotation_dialog, text="Döndürme Açısı (derece):").pack(pady=5)
        angle_scale = Scale(rotation_dialog, from_=-180, to=180, orient=HORIZONTAL, length=200)
        angle_scale.set(0)  # Başlangıç değeri: 0 (dönüş yok)
        angle_scale.pack(pady=5)
        
        # Uygula butonu
        def apply_rotation():
            angle = angle_scale.get()  # Döndürme açısı
            self.rotate_image(angle)
            rotation_dialog.destroy()  # Dialog penceresini kapat
            
        Button(rotation_dialog, text="Uygula", command=apply_rotation).pack(pady=10)
    
    def rotate_image(self, angle):
        """
        Görüntüyü belirtilen açıda döndürür.
        
        cv2.getRotationMatrix2D: Döndürme matrisi oluşturan OpenCV fonksiyonu
        cv2.warpAffine: Görüntüye afin dönüşümü uygulayan OpenCV fonksiyonu
        
        Parametreler:
            angle (int): Döndürme açısı (derece cinsinden, pozitif değerler saat yönünün tersine)
        """
        if self.original_image is None:
            return
            
        # Görüntü boyutları
        h, w = self.original_image.shape[:2]
        
        # Görüntünün merkezi
        center = (w // 2, h // 2)
        
        # Döndürme matrisi oluştur (merkez, açı, ölçek)
        # Üçüncü parametre (1.0) ölçeği belirtir (1.0 = orijinal boyut)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        
        # Döndürülmüş görüntünün sınırlarını hesapla
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])
        new_w = int((h * sin) + (w * cos))
        new_h = int((h * cos) + (w * sin))
        
        # Dönüşüm matrisini yeni merkeze göre ayarla
        M[0, 2] += (new_w / 2) - center[0]
        M[1, 2] += (new_h / 2) - center[1]
        
        # Görüntüyü döndür
        self.current_image = cv2.warpAffine(self.original_image, M, (new_w, new_h))
        self.display_image(self.current_image)
    
    def open_cropping_dialog(self):
        """
        Görüntüyü kırpmak için bir dialog penceresi açar.
        Bu dialog, kullanıcının görüntüden kesilecek bölgeyi belirlemesini sağlar.
        
        Kırpma (cropping), görüntünün belirli bir bölgesini seçip 
        geri kalan kısımlarını atma işlemidir.
        """
        if self.original_image is None:
            return
            
        # Yeni bir dialog penceresi oluştur
        cropping_dialog = tk.Toplevel(self.root)
        cropping_dialog.title("Görüntüyü Kırp")
        cropping_dialog.geometry("350x450")  # Pencere boyutunu artır
        cropping_dialog.resizable(False, False)
        
        # Ana frame oluştur
        main_frame = Frame(cropping_dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Görüntü boyutları
        h, w = self.original_image.shape[:2]
        
        # X başlangıç (sol kenar) için kaydırıcı
        Label(main_frame, text="Sol Kenar:").pack(pady=5)
        x_start_scale = Scale(main_frame, from_=0, to=w-10, orient=HORIZONTAL, length=300)
        x_start_scale.set(0)  # Başlangıç değeri: 0 (sol kenar)
        x_start_scale.pack(pady=5)
        
        # X bitiş (sağ kenar) için kaydırıcı
        Label(main_frame, text="Sağ Kenar:").pack(pady=5)
        x_end_scale = Scale(main_frame, from_=10, to=w, orient=HORIZONTAL, length=300)
        x_end_scale.set(w)  # Başlangıç değeri: genişlik (sağ kenar)
        x_end_scale.pack(pady=5)
        
        # Y başlangıç (üst kenar) için kaydırıcı
        Label(main_frame, text="Üst Kenar:").pack(pady=5)
        y_start_scale = Scale(main_frame, from_=0, to=h-10, orient=HORIZONTAL, length=300)
        y_start_scale.set(0)  # Başlangıç değeri: 0 (üst kenar)
        y_start_scale.pack(pady=5)
        
        # Y bitiş (alt kenar) için kaydırıcı
        Label(main_frame, text="Alt Kenar:").pack(pady=5)
        y_end_scale = Scale(main_frame, from_=10, to=h, orient=HORIZONTAL, length=300)
        y_end_scale.set(h)  # Başlangıç değeri: yükseklik (alt kenar)
        y_end_scale.pack(pady=5)
        
        # Buton çerçevesi
        button_frame = Frame(main_frame)
        button_frame.pack(pady=20)
        
        # Uygula butonu
        def apply_cropping():
            x_start = x_start_scale.get()
            x_end = x_end_scale.get()
            y_start = y_start_scale.get()
            y_end = y_end_scale.get()
            
            # Geçerli bir kırpma bölgesi olduğunu kontrol et
            if x_start >= x_end or y_start >= y_end:
                messagebox.showerror("Hata", "Geçersiz kırpma bölgesi! Başlangıç değeri bitiş değerinden küçük olmalı.")
                return
                
            self.crop_image(x_start, y_start, x_end, y_end)
            cropping_dialog.destroy()  # Dialog penceresini kapat
        
        # İptal ve Uygula butonları    
        Button(button_frame, text="İptal", command=cropping_dialog.destroy, width=10).pack(side=LEFT, padx=5)
        Button(button_frame, text="Uygula", command=apply_cropping, width=10).pack(side=LEFT, padx=5)
    
    def crop_image(self, x_start, y_start, x_end, y_end):
        """
        Görüntüyü belirtilen koordinatlardan kırpar.
        
        Numpy dizileri dilimleyerek kırpma işlemini gerçekleştirir.
        
        Parametreler:
            x_start (int): Kırpılacak bölgenin sol kenarı
            y_start (int): Kırpılacak bölgenin üst kenarı
            x_end (int): Kırpılacak bölgenin sağ kenarı
            y_end (int): Kırpılacak bölgenin alt kenarı
        """
        if self.original_image is None:
            return
            
        # Görüntüyü kırp
        # NumPy dizisi dilimleme sözdizimi: array[y_start:y_end, x_start:x_end]
        self.current_image = self.original_image[y_start:y_end, x_start:x_end].copy()
        self.display_image(self.current_image)

# Ana program başlangıcı
# '__main__' kontrolü, bu dosyanın doğrudan çalıştırıldığında çalışmasını sağlar
# (başka bir dosyadan import edildiğinde çalışmaz)
if __name__ == "__main__":
    root = tk.Tk()  # Ana Tkinter penceresi oluştur
    app = GoruntuIslemeUygulamasi(root)  # Uygulama nesnesini oluştur
    root.mainloop()  # Tkinter olay döngüsünü başlat 