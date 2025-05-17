import os
import tkinter as tk
from tkinter import filedialog, Scale, Label, Button, Frame, HORIZONTAL, RIDGE, SUNKEN, RAISED, LEFT, RIGHT
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
        
        # Ekran boyutunu al ve tam ekran olarak ayarla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        
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
        
        Arayüz şu şekilde düzenlenmiştir:
        - Sol panel: İşlem butonlarının bir kısmını içerir
        - Orta panel: Orijinal ve işlenmiş görüntüleri yan yana gösterir
        - Sağ panel: Diğer işlem butonlarını içerir
        """
        # Ana çerçeveler oluşturuyoruz
        
        # Sol panel için bir canvas ve scrollbar oluşturuyoruz
        self.left_outer_frame = Frame(self.root, width=350, bg="#e0e0e0", relief=RIDGE, borderwidth=2)
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
        
        # Orta panel (Görüntülerin gösterileceği alan)
        self.center_frame = Frame(self.root, bg="#f0f0f0", relief=RIDGE, borderwidth=2)
        self.center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Orijinal görüntü için çerçeve oluştur
        self.original_image_frame = Frame(self.center_frame, bg="white", relief=SUNKEN, borderwidth=2, width=400, height=400)
        self.original_image_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=10)
        self.original_image_frame.pack_propagate(False)  # Boyutu sabit tut
        
        # İşlenmiş görüntü ve histogram için ana çerçeve
        self.processed_area_frame = Frame(self.center_frame, bg="#f0f0f0", width=400)
        self.processed_area_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=10)
        
        # İşlenmiş görüntü çerçevesi
        self.processed_image_frame = Frame(self.processed_area_frame, bg="white", relief=SUNKEN, borderwidth=2, width=400, height=400)
        self.processed_image_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 10))
        self.processed_image_frame.pack_propagate(False)  # Boyutu sabit tut
        
        # Histogram gösterme alanı - işlenmiş görüntünün altında
        self.histogram_container = Frame(self.processed_area_frame, bg="#f0f0f0", relief=RIDGE, borderwidth=2, height=200)
        self.histogram_container.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False)
        
        Label(self.histogram_container, text="Histogram", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(pady=5)
        
        self.histogram_frame = Frame(self.histogram_container, height=160, bg="white", relief=SUNKEN, borderwidth=2)
        self.histogram_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.histogram_frame.pack_propagate(False)  # Boyutu sabit tut
        
        # Görüntü etiketleri
        Label(self.original_image_frame, text="Orijinal Görüntü", bg="white", font=("Arial", 10, "bold")).pack(pady=5)
        self.original_image_label = Label(self.original_image_frame, bg="white")
        self.original_image_label.pack(fill=tk.BOTH, expand=True)
        
        Label(self.processed_image_frame, text="İşlenmiş Görüntü", bg="white", font=("Arial", 10, "bold")).pack(pady=5)
        self.processed_image_label = Label(self.processed_image_frame, bg="white")
        self.processed_image_label.pack(fill=tk.BOTH, expand=True)
        
        # Sağ panel için bir canvas ve scrollbar oluşturuyoruz
        self.right_outer_frame = Frame(self.root, width=350, bg="#e0e0e0", relief=RIDGE, borderwidth=2)
        self.right_outer_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        # Sağ panele kaydırma çubuğu ekle
        self.right_scrollbar = tk.Scrollbar(self.right_outer_frame, orient="vertical")
        self.right_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Canvas oluştur ve scrollbar'a bağla
        self.right_canvas = tk.Canvas(self.right_outer_frame, bg="#e0e0e0", 
                                    yscrollcommand=self.right_scrollbar.set)
        self.right_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right_scrollbar.config(command=self.right_canvas.yview)
        
        # Canvas içine konulacak ana frame yerine Notebook widget'ı
        self.right_notebook = ttk.Notebook(self.right_canvas)
        
        # Sekmeleri oluşturacak frame'ler (bunlar create_control_buttons içinde doldurulacak)
        self.transforms_tab = Frame(self.right_notebook, bg="#e0e0e0")
        self.spatial_filters_tab = Frame(self.right_notebook, bg="#e0e0e0")
        self.frequency_filters_tab = Frame(self.right_notebook, bg="#e0e0e0")
        self.edge_detection_tab = Frame(self.right_notebook, bg="#e0e0e0")
        self.advanced_ops_tab = Frame(self.right_notebook, bg="#e0e0e0")

        self.right_notebook.add(self.transforms_tab, text='Dönüşümler')
        self.right_notebook.add(self.spatial_filters_tab, text='Mekansal')
        self.right_notebook.add(self.frequency_filters_tab, text='Frekans')
        self.right_notebook.add(self.edge_detection_tab, text='Kenar Algılama')
        self.right_notebook.add(self.advanced_ops_tab, text='Gelişmiş')
        
        self.right_canvas.create_window((0, 0), window=self.right_notebook, anchor="nw")
        
        # Kontrol butonları - Sol ve sağ paneldeki butonları oluşturan metodu çağırıyoruz
        self.create_control_buttons()
        
        # Sol ve sağ panelin boyutlarını güncelle
        self.left_frame.update_idletasks()
        self.left_canvas.config(scrollregion=self.left_canvas.bbox("all"))
        self.left_canvas.config(width=330, height=800)
        
        self.right_notebook.update_idletasks()
        self.right_canvas.config(scrollregion=self.right_canvas.bbox("all"))
        self.right_canvas.config(width=340, height=800) # Genişlik 330'dan 340'a çıkarıldı
    
    def create_control_buttons(self):
        """
        Sol ve sağ panellerde yer alan tüm kontrol butonlarını ve arayüz elemanlarını oluşturan metod.
        
        Sol panelde şu bölümler bulunur:
        - Dosya işlemleri
        - Temel işlemler
        - Parlaklık ayarı
        - Eşikleme
        - Histogram işlemleri
        - Kontrast ayarı
        
        Sağ panelde şu bölümler bulunur:
        - Görüntü dönüşümleri
        - Filtreleme işlemleri
        """
        # -------------- SOL PANEL İÇİN KONTROL BUTONLARI --------------
        
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
        
        # -------------- SAĞ PANEL İÇİN KONTROL BUTONLARI (SEKMELİ YAPI) --------------
        
        # --- Dönüşümler Sekmesi ---
        transforms_frame_tab_content = Frame(self.transforms_tab, bg="#e0e0e0", relief=RAISED, borderwidth=1)
        transforms_frame_tab_content.pack(fill=tk.X, padx=5, pady=5)
        Label(transforms_frame_tab_content, text="Görüntü Dönüşümleri", bg="#e0e0e0", font=("Arial", 10, "bold")).pack(pady=5)
        Button(transforms_frame_tab_content, text="Görüntüyü Taşı", command=self.open_translation_dialog, width=22).pack(pady=2)
        Button(transforms_frame_tab_content, text="X Ekseninde Aynala", command=self.flip_horizontal, width=22).pack(pady=2)
        Button(transforms_frame_tab_content, text="Y Ekseninde Aynala", command=self.flip_vertical, width=22).pack(pady=2)
        Button(transforms_frame_tab_content, text="Görüntüyü Eğ", command=self.open_shearing_dialog, width=22).pack(pady=2)
        Button(transforms_frame_tab_content, text="Görüntüyü Ölçekle", command=self.open_scaling_dialog, width=22).pack(pady=2)
        Button(transforms_frame_tab_content, text="Görüntüyü Döndür", command=self.open_rotation_dialog, width=22).pack(pady=2)
        Button(transforms_frame_tab_content, text="Görüntüyü Kırp", command=self.open_cropping_dialog, width=22).pack(pady=2)
        Button(transforms_frame_tab_content, text="Perspektif Düzelt", command=self.open_perspective_correction, width=22).pack(pady=2)

        # --- Mekansal Filtreler Sekmesi ---
        spatial_filters_frame_content = Frame(self.spatial_filters_tab, bg="#e0e0e0", relief=RAISED, borderwidth=1)
        spatial_filters_frame_content.pack(fill=tk.X, padx=5, pady=5)
        Label(spatial_filters_frame_content, text="Mekansal Alan Filtreleri", bg="#e0e0e0", font=("Arial", 10, "bold")).pack(pady=5)
        Button(spatial_filters_frame_content, text="Ortalama Filtresi", command=self.open_mean_filter_dialog, width=22).pack(pady=2)
        Button(spatial_filters_frame_content, text="Medyan Filtresi", command=self.open_median_filter_dialog, width=22).pack(pady=2)
        Button(spatial_filters_frame_content, text="Gaussian Filtresi", command=self.open_gaussian_filter_dialog, width=22).pack(pady=2)
        Button(spatial_filters_frame_content, text="Konservatif Filtre", command=self.open_conservative_filter_dialog, width=22).pack(pady=2)
        Button(spatial_filters_frame_content, text="Crimmins Speckle", command=self.open_crimmins_speckle_dialog, width=22).pack(pady=2)
        Button(spatial_filters_frame_content, text="Aşındırma (Erode)", command=lambda: self.open_morph_dialog("Erode"), width=22).pack(pady=2)
        Button(spatial_filters_frame_content, text="Genişletme (Dilate)", command=lambda: self.open_morph_dialog("Dilate"), width=22).pack(pady=2)

        # --- Frekans Filtreleri Sekmesi ---
        frequency_filters_frame_content = Frame(self.frequency_filters_tab, bg="#e0e0e0", relief=RAISED, borderwidth=1)
        frequency_filters_frame_content.pack(fill=tk.X, padx=5, pady=5)
        Label(frequency_filters_frame_content, text="Frekans Alanı Filtreleri", bg="#e0e0e0", font=("Arial", 10, "bold")).pack(pady=5)
        Button(frequency_filters_frame_content, text="Fourier Alçak Geçiren", command=self.open_fourier_lowpass_dialog, width=22).pack(pady=2)
        Button(frequency_filters_frame_content, text="Fourier Yüksek Geçiren", command=self.open_fourier_highpass_dialog, width=22).pack(pady=2)
        Button(frequency_filters_frame_content, text="Band Geçiren Filtre", command=self.open_band_pass_dialog, width=22).pack(pady=2)
        Button(frequency_filters_frame_content, text="Band Durduran Filtre", command=self.open_band_stop_dialog, width=22).pack(pady=2)
        Button(frequency_filters_frame_content, text="Butterworth Filtresi", command=self.open_butterworth_filter_dialog, width=22).pack(pady=2)
        Button(frequency_filters_frame_content, text="Gauss Düşük/Yüksek Geçiren", command=self.open_gaussian_freq_dialog, width=22).pack(pady=2)
        Button(frequency_filters_frame_content, text="Homomorfik Filtre", command=self.apply_homomorphic_filter, width=22).pack(pady=2)
        
        # --- Kenar Algılama Sekmesi ---
        edge_detection_frame_content = Frame(self.edge_detection_tab, bg="#e0e0e0", relief=RAISED, borderwidth=1)
        edge_detection_frame_content.pack(fill=tk.X, padx=5, pady=5)
        Label(edge_detection_frame_content, text="Kenar Algılama Filtreleri", bg="#e0e0e0", font=("Arial", 10, "bold")).pack(pady=5)
        Button(edge_detection_frame_content, text="Sobel Filtresi", command=self.apply_sobel_filter, width=22).pack(pady=2)
        Button(edge_detection_frame_content, text="Prewitt Filtresi", command=self.apply_prewitt_filter, width=22).pack(pady=2)
        Button(edge_detection_frame_content, text="Roberts Cross Filtresi", command=self.apply_roberts_cross_filter, width=22).pack(pady=2)
        Button(edge_detection_frame_content, text="Compass Filtresi", command=self.apply_compass_filter, width=22).pack(pady=2)
        Button(edge_detection_frame_content, text="Canny Kenar Algılama", command=self.open_canny_dialog, width=22).pack(pady=2)
        Button(edge_detection_frame_content, text="Laplace Filtresi", command=self.apply_laplacian_filter, width=22).pack(pady=2)
        Button(edge_detection_frame_content, text="Gabor Filtresi", command=self.open_gabor_filter_dialog, width=22).pack(pady=2)

        # --- Gelişmiş İşlemler Sekmesi ---
        advanced_ops_frame_content = Frame(self.advanced_ops_tab, bg="#e0e0e0", relief=RAISED, borderwidth=1)
        advanced_ops_frame_content.pack(fill=tk.X, padx=5, pady=5)
        Label(advanced_ops_frame_content, text="Gelişmiş Görüntü İşleme", bg="#e0e0e0", font=("Arial", 10, "bold")).pack(pady=5)
        Button(advanced_ops_frame_content, text="Hough Dönüşümü (Çizgiler)", command=self.open_hough_line_dialog, width=25).pack(pady=2)
        Button(advanced_ops_frame_content, text="Hough Dönüşümü (Çemberler)", command=self.open_hough_circle_dialog, width=25).pack(pady=2)
        Button(advanced_ops_frame_content, text="K-Means Segmentasyon", command=self.open_kmeans_segmentation_dialog, width=25).pack(pady=2)
    
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
        Verilen görüntüyü işlenmiş görüntü olarak gösterir ve orijinal görüntüyü de gösterir.
        Görüntüleri uygun boyuta getirir ve ilgili Tkinter Label'larına yerleştirir.
        
        Parametreler:
            image (numpy.ndarray): Gösterilecek işlenmiş görüntü (RGB formatlı NumPy dizisi)
        """
        if image is None:
            return
        
        # İlk kez bir görüntü gösteriliyorsa veya orijinal görüntü gösterilmek isteniyorsa
        if self.original_image is not None:
            # Orijinal görüntüyü göster
            self._resize_and_display(self.original_image, self.original_image_label)
        
        # İşlenmiş görüntüyü göster
        self._resize_and_display(image, self.processed_image_label)
    
    def _resize_and_display(self, image, target_label):
        """
        Verilen görüntüyü yeniden boyutlandırır ve hedef label'a yerleştirir.
        
        Parametreler:
            image (numpy.ndarray): Gösterilecek görüntü
            target_label (tk.Label): Görüntünün yerleştirileceği Label
        """
        # Görüntüyü yeniden boyutlandır - Eğer görüntü çok büyükse, ekrana sığdırmak için küçültüyoruz
        h, w = image.shape[:2]  # Görüntünün yükseklik ve genişliğini al
        max_size = 350  # Tek bir panel için maksimum boyut
        
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
        target_label.configure(image=tk_img)
        target_label.image = tk_img  # Referansı koru (Python'un çöp toplayıcısı silmesin diye)
    
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
        try:
            # Hiç görüntü yüklenmemişse işlem yapma
            if self.original_image is None:
                messagebox.showinfo("Bilgi", "Önce bir görüntü yüklemelisiniz!")
                return
                
            # Eğer current_image yoksa, original_image'i kullan
            if self.current_image is None:
                self.current_image = self.original_image.copy()
                
            # Histogram çerçevesini temizle
            for widget in self.histogram_frame.winfo_children():
                widget.destroy()
                
            # Histogram için özel bir frame oluştur
            hist_display_frame = Frame(self.histogram_frame, bg="white")
            hist_display_frame.pack(fill=tk.BOTH, expand=True)
            
            # Matplotlib figürü oluştur - boyutları sabit tut
            fig = plt.Figure(figsize=(12, 3), dpi=80)
            ax = fig.add_subplot(111)  # 1x1 grid, 1. pozisyon
            
            # Gri tonlamalı görüntü için histogram
            # np.array_equal: İki dizinin eşit olup olmadığını kontrol eden NumPy fonksiyonu
            # Eğer tüm kanallar aynıysa, görüntü gri tonlamalıdır
            if len(self.current_image.shape) == 2 or (len(self.current_image.shape) == 3 and np.array_equal(self.current_image[:,:,0], self.current_image[:,:,1]) and np.array_equal(self.current_image[:,:,0], self.current_image[:,:,2])):
                gray_img = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2GRAY) if len(self.current_image.shape) == 3 else self.current_image
                hist = cv2.calcHist([gray_img], [0], None, [256], [0, 256])
                ax.plot(hist, color='black', linewidth=2)
                ax.set_xlim([0, 256])
                ax.set_title('Gri Tonlama Histogramı', fontsize=12, fontweight='bold')
                ax.set_xlabel('Piksel Değeri', fontsize=10)
                ax.set_ylabel('Piksel Sayısı', fontsize=10)
                ax.grid(True, linestyle='--', alpha=0.7)
            else:
                # Renkli görüntü için histogram - Her kanal için ayrı histogram
                colors = ('r', 'g', 'b')
                labels = ('Kırmızı', 'Yeşil', 'Mavi')
                for i, (color, label) in enumerate(zip(colors, labels)):
                    hist = cv2.calcHist([self.current_image], [i], None, [256], [0, 256])
                    ax.plot(hist, color=color, linewidth=2, label=label)
                ax.set_xlim([0, 256])
                ax.set_title('RGB Histogramı', fontsize=12, fontweight='bold')
                ax.set_xlabel('Piksel Değeri', fontsize=10)
                ax.set_ylabel('Piksel Sayısı', fontsize=10)
                ax.grid(True, linestyle='--', alpha=0.7)
                ax.legend()
            
            # Figürü Tkinter'a ekle
            canvas = FigureCanvasTkAgg(fig, master=hist_display_frame)
            canvas.draw()
            
            # Canvas'ı düzgün bir şekilde yerleştir
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Tüm panelleri güncelle
            self.histogram_frame.update_idletasks()
            self.center_frame.update_idletasks()
            self.root.update_idletasks()
            
            # Histogramın başarıyla gösterildiğini bildir
            print("Histogram başarıyla gösterildi.")
            
        except Exception as e:
            # Hata mesajını göster
            messagebox.showerror("Hata", f"Histogram gösterilirken bir hata oluştu: {str(e)}")
            print(f"Histogram hatası: {str(e)}")
    
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
        if self.current_image is None:
            return
            
        # Görüntü boyutları
        h, w = self.current_image.shape[:2]
        
        # Taşıma matrisi oluştur [ [1, 0, tx], [0, 1, ty] ]
        # İlk parametre 2x3'lük bir matris olmalı
        M = np.float32([[1, 0, tx], [0, 1, ty]])
        
        # Görüntüyü taşı
        self.current_image = cv2.warpAffine(self.current_image, M, (w, h))
        self.display_image(self.current_image)
    
    def flip_horizontal(self):
        """
        Görüntüyü yatay eksende aynalar (x eksenine göre çevirir).
        Bu işlem, görüntüyü soldan sağa ters çevirir.
        
        cv2.flip: Görüntüyü belirtilen eksende çeviren OpenCV fonksiyonu
        flipCode = 1: Yatay eksende aynalama
        """
        if self.current_image is None:
            return
            
        # Görüntüyü yatay eksende aynala (flipCode = 1)
        self.current_image = cv2.flip(self.current_image, 1)
        self.display_image(self.current_image)
    
    def flip_vertical(self):
        """
        Görüntüyü dikey eksende aynalar (y eksenine göre çevirir).
        Bu işlem, görüntüyü yukarıdan aşağıya ters çevirir.
        
        cv2.flip: Görüntüyü belirtilen eksende çeviren OpenCV fonksiyonu
        flipCode = 0: Dikey eksende aynalama
        """
        if self.current_image is None:
            return
            
        # Görüntüyü dikey eksende aynala (flipCode = 0)
        self.current_image = cv2.flip(self.current_image, 0)
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
        if self.current_image is None:
            return
            
        # Görüntü boyutları
        h, w = self.current_image.shape[:2]
        
        # Eğme matrisi oluştur
        M = np.float32([[1, sx, 0], [sy, 1, 0]])
        
        # Görüntüyü eğ
        self.current_image = cv2.warpAffine(self.current_image, M, (w, h))
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
        if self.current_image is None:
            return
            
        # Görüntü boyutları
        h, w = self.current_image.shape[:2]
        
        # Yeni boyutları hesapla
        new_w = int(w * sx)
        new_h = int(h * sy)
        
        # Görüntüyü ölçekle (yeniden boyutlandır)
        # Büyütme işlemi için cv2.INTER_CUBIC, küçültme işlemi için cv2.INTER_AREA önerilir
        interpolation = cv2.INTER_CUBIC if sx > 1 or sy > 1 else cv2.INTER_AREA
        self.current_image = cv2.resize(self.current_image, (new_w, new_h), interpolation=interpolation)
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
        if self.current_image is None:
            return
            
        # Görüntü boyutları
        h, w = self.current_image.shape[:2]
        
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
        self.current_image = cv2.warpAffine(self.current_image, M, (new_w, new_h))
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
        if self.current_image is None:
            return
            
        # Görüntüyü kırp
        # NumPy dizisi dilimleme sözdizimi: array[y_start:y_end, x_start:x_end]
        self.current_image = self.current_image[y_start:y_end, x_start:x_end].copy()
        self.display_image(self.current_image)
    
    def open_perspective_correction(self):
        """
        Perspektif düzeltme işlemi için bir OpenCV penceresi açar.
        Kullanıcının düzeltilecek bölgenin 4 köşesini seçmesini sağlar.
        Seçilen noktalar kullanılarak perspektif dönüşüm uygulanır.
        """
        if self.current_image is None:
            return
            
        # Sınıf değişkeni olarak seçilen noktaları saklayacak listeyi tanımla
        self.selected_points = []
            
        # OpenCV ile görüntüyü göster
        # Görüntüyü RGB'den BGR'ye çevir (OpenCV BGR formatını kullanır)
        img_to_show = cv2.cvtColor(self.current_image.copy(), cv2.COLOR_RGB2BGR)
        
        # Kullanıcıya talimat göster
        img_with_text = img_to_show.copy()
        text = "4 nokta secin: Sol Ust -> Sag Ust -> Sol Alt -> Sag Alt"
        cv2.putText(img_with_text, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Pencereyi oluştur ve mouse callback fonksiyonunu bağla
        cv2.imshow("Perspektif Duzeltme - 4 Nokta Sec", img_with_text)
        cv2.setMouseCallback("Perspektif Duzeltme - 4 Nokta Sec", self.perspective_correction_select_points, img_to_show)
        
        # Kullanıcı 4 nokta seçene kadar veya pencere kapatılana kadar bekle
        while len(self.selected_points) < 4 and cv2.getWindowProperty("Perspektif Duzeltme - 4 Nokta Sec", cv2.WND_PROP_VISIBLE) > 0:
            key = cv2.waitKey(100)
            if key == 27:  # ESC tuşu
                break
        
        # Pencereyi kapat
        cv2.destroyAllWindows()
        
        # Eğer 4 nokta seçildiyse, perspektif düzeltmeyi uygula
        if len(self.selected_points) == 4:
            self.apply_perspective_correction()
            
    def perspective_correction_select_points(self, event, x, y, flags, param):
        """
        Mouse tıklamalarını yakalayan callback fonksiyonu.
        Her sol tıklamada, tıklanan noktayı selected_points listesine ekler.
        
        Parametreler:
            event: Mouse olayı türü
            x, y: Tıklanan noktanın koordinatları
            flags: Ek bayraklar
            param: Ek parametreler (burada orijinal görüntü kullanılır)
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            # Noktayı listeye ekle
            self.selected_points.append((x, y))
            
            # Noktayı görüntü üzerinde göster
            img = param.copy()
            for i, point in enumerate(self.selected_points):
                cv2.circle(img, point, 5, (0, 0, 255), -1)
                cv2.putText(img, str(i+1), (point[0]+10, point[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Talimatları güncelle
            remaining = 4 - len(self.selected_points)
            if remaining > 0:
                text = f"{remaining} nokta daha secin"
            else:
                text = "Tum noktalar secildi! Pencere kapaniyor..."
            cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Güncellenmiş görüntüyü göster
            cv2.imshow("Perspektif Duzeltme - 4 Nokta Sec", img)
            
            # Eğer 4 nokta seçildiyse, kısa bir süre sonra pencereyi kapat
            if len(self.selected_points) == 4:
                cv2.waitKey(1000)
                cv2.destroyAllWindows()
    
    def apply_perspective_correction(self):
        """
        Seçilen 4 nokta kullanılarak perspektif düzeltme işlemini uygular.
        Seçilen noktalar kaynağı, standart bir dikdörtgen hedefi temsil eder.
        Dönüşüm matrisi hesaplanır ve warpPerspective ile uygulanır.
        """
        if len(self.selected_points) != 4:
            return
        
        # Kullanıcının seçtiği noktaları numpy array'e çevir
        pts1 = np.float32(self.selected_points)
        
        # Dialog ile hedef boyutları belirle
        perspective_dialog = tk.Toplevel(self.root)
        perspective_dialog.title("Perspektif Düzeltme Boyutları")
        perspective_dialog.geometry("300x200")
        perspective_dialog.resizable(False, False)
        
        # Genişlik için giriş alanı
        Label(perspective_dialog, text="Genişlik:").pack(pady=5)
        width_entry = tk.Entry(perspective_dialog)
        width_entry.insert(0, "500")  # Varsayılan değer
        width_entry.pack(pady=5)
        
        # Yükseklik için giriş alanı
        Label(perspective_dialog, text="Yükseklik:").pack(pady=5)
        height_entry = tk.Entry(perspective_dialog)
        height_entry.insert(0, "500")  # Varsayılan değer
        height_entry.pack(pady=5)
        
        # Uygulama butonu
        def apply_transform():
            try:
                width = int(width_entry.get())
                height = int(height_entry.get())
                
                if width <= 0 or height <= 0:
                    messagebox.showerror("Hata", "Genişlik ve yükseklik pozitif değerler olmalıdır.")
                    return
                
                # Düzeltme sonrası köşeleri belirle (çıkış boyutlarına göre)
                pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
                
                # Perspektif dönüşüm matrisini hesapla
                matrix = cv2.getPerspectiveTransform(pts1, pts2)
                
                # Perspektif dönüşümünü uygula
                # OpenCV BGR formatını kullanırken, bizim görüntümüz RGB formatında,
                # bu yüzden gerekli dönüşümleri yapmalıyız
                img_bgr = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2BGR)
                warped_image_bgr = cv2.warpPerspective(img_bgr, matrix, (width, height))
                warped_image_rgb = cv2.cvtColor(warped_image_bgr, cv2.COLOR_BGR2RGB)
                
                # İşlenmiş görüntüyü güncelle ve göster
                self.current_image = warped_image_rgb
                self.display_image(self.current_image)
                
                # Dialog penceresini kapat
                perspective_dialog.destroy()
                
            except ValueError:
                messagebox.showerror("Hata", "Geçersiz genişlik veya yükseklik değeri!")
        
        # Butonları oluştur
        Button(perspective_dialog, text="İptal", command=perspective_dialog.destroy).pack(side=LEFT, padx=20, pady=20)
        Button(perspective_dialog, text="Uygula", command=apply_transform).pack(side=RIGHT, padx=20, pady=20)
    
    # ------------ FİLTRELEME İŞLEMLERİ ------------
    
    def open_mean_filter_dialog(self):
        """
        Ortalama filtresi uygulamak için bir dialog penceresi açar.
        Bu dialog, kullanıcının filtrenin çekirdek boyutunu belirlemesini sağlar.
        
        Ortalama filtresi, görüntüdeki piksel değerlerini belirli bir komşuluktaki piksellerin 
        ortalaması ile değiştirerek gürültüyü azaltır ve görüntüyü yumuşatır.
        """
        if self.current_image is None:
            return
            
        # Yeni bir dialog penceresi oluştur
        mean_dialog = tk.Toplevel(self.root)
        mean_dialog.title("Ortalama Filtresi")
        mean_dialog.geometry("300x150")
        mean_dialog.resizable(False, False)
        
        # Çekirdek boyutu için seçim
        Label(mean_dialog, text="Çekirdek Boyutu:").pack(pady=5)
        kernel_size_var = tk.StringVar(value="3")
        kernel_sizes = ["3", "5", "7", "9", "11", "15"]
        kernel_dropdown = ttk.Combobox(mean_dialog, textvariable=kernel_size_var, values=kernel_sizes, state="readonly", width=10)
        kernel_dropdown.pack(pady=5)
        
        # Uygula butonu
        def apply_mean_filter():
            kernel_size = int(kernel_size_var.get())
            self.apply_mean_filter(kernel_size)
            mean_dialog.destroy()  # Dialog penceresini kapat
        
        Button(mean_dialog, text="Uygula", command=apply_mean_filter, width=15).pack(pady=10)
    
    def apply_mean_filter(self, kernel_size):
        """
        Görüntüye ortalama filtresi uygular.
        
        cv2.blur: Ortalama filtresi uygulayan OpenCV fonksiyonu
        
        Parametreler:
            kernel_size (int): Filtre çekirdeğinin boyutu (örn. 3 için 3x3 çekirdek)
        """
        if self.current_image is None:
            return
        
        # Görüntüyü ortalama filtresi ile filtrele
        self.current_image = cv2.blur(self.current_image, (kernel_size, kernel_size))
        self.display_image(self.current_image)
    
    def open_median_filter_dialog(self):
        """
        Medyan filtresi uygulamak için bir dialog penceresi açar.
        Bu dialog, kullanıcının filtrenin çekirdek boyutunu belirlemesini sağlar.
        
        Medyan filtresi, görüntüdeki piksel değerlerini belirli bir komşuluktaki piksellerin 
        medyanı ile değiştirerek gürültüyü azaltır. Salt & pepper (tuz ve biber) gürültüsünü 
        gidermede özellikle etkilidir.
        """
        if self.current_image is None:
            return
            
        # Yeni bir dialog penceresi oluştur
        median_dialog = tk.Toplevel(self.root)
        median_dialog.title("Medyan Filtresi")
        median_dialog.geometry("300x150")
        median_dialog.resizable(False, False)
        
        # Çekirdek boyutu için seçim - Medyan filtresi için tek sayı olmalı
        Label(median_dialog, text="Çekirdek Boyutu:").pack(pady=5)
        kernel_size_var = tk.StringVar(value="3")
        kernel_sizes = ["3", "5", "7", "9", "11"]
        kernel_dropdown = ttk.Combobox(median_dialog, textvariable=kernel_size_var, values=kernel_sizes, state="readonly", width=10)
        kernel_dropdown.pack(pady=5)
        
        # Uygula butonu
        def apply_median_filter():
            kernel_size = int(kernel_size_var.get())
            self.apply_median_filter(kernel_size)
            median_dialog.destroy()  # Dialog penceresini kapat
        
        Button(median_dialog, text="Uygula", command=apply_median_filter, width=15).pack(pady=10)
    
    def apply_median_filter(self, kernel_size):
        """
        Görüntüye medyan filtresi uygular.
        
        cv2.medianBlur: Medyan filtresi uygulayan OpenCV fonksiyonu
        
        Parametreler:
            kernel_size (int): Filtre çekirdeğinin boyutu (örn. 3 için 3x3 çekirdek)
        """
        if self.current_image is None:
            return
        
        # Görüntüyü medyan filtresi ile filtrele
        self.current_image = cv2.medianBlur(self.current_image, kernel_size)
        self.display_image(self.current_image)

    def open_gaussian_filter_dialog(self):
        """
        Mekansal Gaussian filtresi uygulamak için bir dialog penceresi açar.
        
        Gaussian filtresi, görüntüyü 2 boyutlu Gaussian fonksiyonu ile konvolüsyon yaparak gürültüyü
        azaltırken keskin hatları da koruyan bir yumuşatma filtresidir.
        """
        if self.current_image is None:
            return
            
        # Yeni bir dialog penceresi oluştur
        gaussian_dialog = tk.Toplevel(self.root)
        gaussian_dialog.title("Gaussian Filtresi")
        gaussian_dialog.geometry("300x200")
        gaussian_dialog.resizable(False, False)
        
        # Çekirdek boyutu için seçim
        Label(gaussian_dialog, text="Çekirdek Boyutu:").pack(pady=5)
        kernel_size_var = tk.StringVar(value="3")
        kernel_sizes = ["3", "5", "7", "9", "11", "15"]
        kernel_dropdown = ttk.Combobox(gaussian_dialog, textvariable=kernel_size_var, values=kernel_sizes, state="readonly", width=10)
        kernel_dropdown.pack(pady=5)
        
        # Sigma değeri için slider
        Label(gaussian_dialog, text="Sigma Değeri:").pack(pady=5)
        sigma_scale = Scale(gaussian_dialog, from_=0.1, to=5.0, resolution=0.1, orient=HORIZONTAL, length=200)
        sigma_scale.set(1.0)  # Varsayılan değer
        sigma_scale.pack(pady=5)
        
        # Uygula butonu
        def apply_gaussian_filter():
            kernel_size = int(kernel_size_var.get())
            sigma = sigma_scale.get()
            self.apply_gaussian_filter(kernel_size, sigma)
            gaussian_dialog.destroy()  # Dialog penceresini kapat
        
        Button(gaussian_dialog, text="Uygula", command=apply_gaussian_filter, width=15).pack(pady=10)
    
    def apply_gaussian_filter(self, kernel_size, sigma):
        """
        Görüntüye mekansal Gaussian filtresi uygular.
        
        cv2.GaussianBlur: Gaussian filtresi uygulayan OpenCV fonksiyonu
        
        Parametreler:
            kernel_size (int): Filtre çekirdeğinin boyutu (örn. 3 için 3x3 çekirdek)
            sigma (float): Gaussian fonksiyonunun standart sapması
        """
        if self.current_image is None:
            return
        
        # Görüntüyü Gaussian filtresi ile filtrele
        self.current_image = cv2.GaussianBlur(self.current_image, (kernel_size, kernel_size), sigma)
        self.display_image(self.current_image)
        
    def apply_conservative_filter(self):
        """
        Görüntüye konservatif filtreleme uygular.
        
        Konservatif filtreleme, bir piksel etrafındaki komşu piksellerin minimum ve maksimum değerleri
        arasında sınırlama yaparak gürültüyü azaltan bir yöntemdir. Bu yöntem, kenarları korur ve
        küçük gürültüleri giderir.
        
        OpenCV'de doğrudan bu filtre bulunmadığı için manuel olarak uygulanmıştır.
        """
        if self.current_image is None:
            return
            
        # Görüntü bir kopya olarak alınır
        result = self.current_image.copy()
        
        # Gri tonlama görüntüsü için işlemi gerçekleştir
        if len(self.current_image.shape) == 2 or (len(self.current_image.shape) == 3 and self.current_image.shape[2] == 1):
            # Gri tonlama görüntüsü
            padded = cv2.copyMakeBorder(self.current_image, 1, 1, 1, 1, cv2.BORDER_REFLECT)
            
            for i in range(1, padded.shape[0]-1):
                for j in range(1, padded.shape[1]-1):
                    # 3x3 pencere
                    window = padded[i-1:i+2, j-1:j+2]
                    center = padded[i, j]
                    
                    # Minimum ve maksimum değerleri bul
                    min_val = np.min(window)
                    max_val = np.max(window)
                    
                    # Eğer merkez piksel minimum değerden küçükse, minimum olarak ayarla
                    if center < min_val:
                        result[i-1, j-1] = min_val
                    # Eğer merkez piksel maksimum değerden büyükse, maksimum olarak ayarla
                    elif center > max_val:
                        result[i-1, j-1] = max_val
                    # Aksi takdirde değişiklik yapma
        else:
            # Renkli görüntü (BGR)
            # Her kanal için ayrı ayrı filtrele
            for k in range(3):  # 3 kanal: B, G, R
                padded = cv2.copyMakeBorder(self.current_image[:,:,k], 1, 1, 1, 1, cv2.BORDER_REFLECT)
                
                for i in range(1, padded.shape[0]-1):
                    for j in range(1, padded.shape[1]-1):
                        # 3x3 pencere
                        window = padded[i-1:i+2, j-1:j+2]
                        center = padded[i, j]
                        
                        # Minimum ve maksimum değerleri bul
                        min_val = np.min(window)
                        max_val = np.max(window)
                        
                        # Eğer merkez piksel minimum değerden küçükse, minimum olarak ayarla
                        if center < min_val:
                            result[i-1, j-1, k] = min_val
                        # Eğer merkez piksel maksimum değerden büyükse, maksimum olarak ayarla
                        elif center > max_val:
                            result[i-1, j-1, k] = max_val
                        # Aksi takdirde değişiklik yapma
        
        self.current_image = result
        self.display_image(self.current_image)

    def open_conservative_filter_dialog(self):
        """
        Konservatif filtreleme işlemi için bir dialog penceresi açar.
        
        Konservatif filtre, görüntüdeki tuz ve biber gürültüsünü azaltırken
        kenarları koruyan bir filtreleme türüdür.
        """
        if self.current_image is None:
            return
            
        # Onay mesajı
        confirm = messagebox.askyesno(
            "Konservatif Filtreleme", 
            "Konservatif filtreleme işlemi başlatılacak.\n\n"
            "Bu işlem büyük görüntülerde uzun sürebilir.\n"
            "Devam etmek istiyor musunuz?"
        )
        
        if confirm:
            # İşlemi başlat
            self.apply_conservative_filter()

    def open_crimmins_speckle_dialog(self):
        """
        Crimmins Speckle gürültü giderme işlemi için bir dialog penceresi açar.
        
        Crimmins Speckle algoritması, özellikle tuz ve biber gürültüsünü gidermekte
        etkili olan bir yöntemdir.
        """
        if self.current_image is None:
            return
            
        # Onay mesajı
        confirm = messagebox.askyesno(
            "Crimmins Speckle Filtreleme", 
            "Crimmins Speckle filtreleme işlemi başlatılacak.\n\n"
            "Bu işlem büyük görüntülerde uzun sürebilir.\n"
            "Devam etmek istiyor musunuz?"
        )
        
        if confirm:
            # İşlemi başlat
            self.apply_crimmins_speckle()

    def apply_crimmins_speckle(self):
        """
        Görüntüye Crimmins speckle gürültü giderme algoritmasını uygular.
        
        Crimmins algoritması piksel değerlerini, komşu piksellerle karşılaştırarak
        gürültülü pikselleri tanıyan ve düzelten, özellikle speckle (nokta) gürültüsü 
        gidermede etkili bir yöntemdir.
        
        OpenCV'de doğrudan bu filtre bulunmadığı için manuel olarak uygulanmıştır.
        """
        if self.current_image is None:
            return
            
        # Görüntü bir kopya olarak alınır
        result = self.current_image.copy()
        
        # Crimmins speckle gürültü giderme algoritması
        def crimmins_one_iteration(img, copy):
            # Yardımcı fonksiyonlar - sırasıyla 4 yönde ilerleyip filtreleme yapar
            # Kuzey (yukarı)
            for i in range(1, img.shape[0]):
                for j in range(img.shape[1]):
                    if img[i-1, j] >= img[i, j] + 2:
                        copy[i, j] = copy[i, j] + 1
                    elif img[i, j] >= img[i-1, j] + 2:
                        copy[i, j] = copy[i, j] - 1
            
            # Güney (aşağı)
            for i in range(img.shape[0]-2, -1, -1):
                for j in range(img.shape[1]):
                    if img[i+1, j] >= img[i, j] + 2:
                        copy[i, j] = copy[i, j] + 1
                    elif img[i, j] >= img[i+1, j] + 2:
                        copy[i, j] = copy[i, j] - 1
            
            # Doğu (sağa)
            for i in range(img.shape[0]):
                for j in range(1, img.shape[1]):
                    if img[i, j-1] >= img[i, j] + 2:
                        copy[i, j] = copy[i, j] + 1
                    elif img[i, j] >= img[i, j-1] + 2:
                        copy[i, j] = copy[i, j] - 1
            
            # Batı (sola)
            for i in range(img.shape[0]):
                for j in range(img.shape[1]-2, -1, -1):
                    if img[i, j+1] >= img[i, j] + 2:
                        copy[i, j] = copy[i, j] + 1
                    elif img[i, j] >= img[i, j+1] + 2:
                        copy[i, j] = copy[i, j] - 1
            
            # Kuzeydoğu (sağ üst çapraz)
            for i in range(1, img.shape[0]):
                for j in range(1, img.shape[1]):
                    if img[i-1, j-1] >= img[i, j] + 2:
                        copy[i, j] = copy[i, j] + 1
                    elif img[i, j] >= img[i-1, j-1] + 2:
                        copy[i, j] = copy[i, j] - 1
            
            # Güneybatı (sol alt çapraz)
            for i in range(img.shape[0]-2, -1, -1):
                for j in range(img.shape[1]-2, -1, -1):
                    if img[i+1, j+1] >= img[i, j] + 2:
                        copy[i, j] = copy[i, j] + 1
                    elif img[i, j] >= img[i+1, j+1] + 2:
                        copy[i, j] = copy[i, j] - 1
            
            # Kuzeybatı (sol üst çapraz)
            for i in range(1, img.shape[0]):
                for j in range(img.shape[1]-2, -1, -1):
                    if img[i-1, j+1] >= img[i, j] + 2:
                        copy[i, j] = copy[i, j] + 1
                    elif img[i, j] >= img[i-1, j+1] + 2:
                        copy[i, j] = copy[i, j] - 1
            
            # Güneydoğu (sağ alt çapraz)
            for i in range(img.shape[0]-2, -1, -1):
                for j in range(1, img.shape[1]):
                    if img[i+1, j-1] >= img[i, j] + 2:
                        copy[i, j] = copy[i, j] + 1
                    elif img[i, j] >= img[i+1, j-1] + 2:
                        copy[i, j] = copy[i, j] - 1
                        
            return copy
        
        # Gri tonlama görüntüsü için işlemi gerçekleştir
        if len(self.current_image.shape) == 2 or (len(self.current_image.shape) == 3 and self.current_image.shape[2] == 1):
            # Gri tonlama görüntüsü
            img_copy = self.current_image.copy()
            # Algoritma 5 kez uygulandı
            for _ in range(5):
                img_copy = crimmins_one_iteration(img_copy, img_copy.copy())
            result = img_copy
        else:
            # Renkli görüntü (BGR)
            # Her kanal için ayrı ayrı filtrele
            for k in range(3):  # 3 kanal: B, G, R
                img_channel = self.current_image[:,:,k].copy()
                img_copy = img_channel.copy()
                # Algoritma 5 kez uygulandı
                for _ in range(5):
                    img_copy = crimmins_one_iteration(img_copy, img_copy.copy())
                result[:,:,k] = img_copy
        
        self.current_image = result
        self.display_image(self.current_image)

    def _fourier_transform(self, image):
        """
        Görüntünün Fourier dönüşümünü hesaplar.
        
        Parametreler:
            image: Dönüşüm uygulanacak görüntü
            
        Dönüş:
            f_transform: Kompleks Fourier dönüşümü
            magnitude_spectrum: Görselleştirme için kullanılabilecek genlik spektrumu
            dft_shift: Merkezi kaydırılmış Fourier dönüşümü
        """
        # Görüntü boyutunu optimize et
        rows, cols = image.shape
        optimal_rows = cv2.getOptimalDFTSize(rows)
        optimal_cols = cv2.getOptimalDFTSize(cols)
        
        # Görüntüyü optimal boyuta genişlet (sınırları sıfırla doldur)
        padded = cv2.copyMakeBorder(image, 0, optimal_rows - rows, 0, optimal_cols - cols, cv2.BORDER_CONSTANT, value=0)
        
        # Fourier dönüşümünü hesapla
        f_transform = cv2.dft(np.float32(padded), flags=cv2.DFT_COMPLEX_OUTPUT)
        
        # Düşük frekans bileşenlerini merkeze taşı
        dft_shift = np.fft.fftshift(f_transform)
        
        # Fourier dönüşümünün genlik spektrumunu hesapla
        magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:,:,0], dft_shift[:,:,1]) + 1)
        
        return f_transform, magnitude_spectrum, dft_shift

    def _inverse_fourier_transform(self, dft_shift, original_shape):
        """
        Fourier dönüşümünün tersini alarak görüntüyü geri oluşturur.
        
        Parametreler:
            dft_shift: Merkezi kaydırılmış Fourier dönüşümü
            original_shape: Orijinal görüntünün boyutu (satır, sütun)
            
        Dönüş:
            Ters Fourier dönüşümü ile elde edilen görüntü
        """
        # Merkez kaydırmayı geri al
        f_ishift = np.fft.ifftshift(dft_shift)
        
        # Ters Fourier dönüşümünü hesapla
        img_back = cv2.idft(f_ishift)
        
        # Gerçek kısmını al ve normlandır
        img_back = cv2.magnitude(img_back[:,:,0], img_back[:,:,1])
        
        # Orijinal boyuta kırp ve normalize et
        rows, cols = original_shape
        img_back = img_back[0:rows, 0:cols]
        cv2.normalize(img_back, img_back, 0, 255, cv2.NORM_MINMAX)
        
        return np.uint8(img_back)

    def open_fourier_lowpass_dialog(self):
        """
        Fourier Alçak Geçiren Filtre dialog penceresini açar.
        
        Alçak geçiren filtre, görüntüdeki yüksek frekans bileşenlerini (kenar, detay, gürültü) 
        zayıflatırken düşük frekans bileşenlerini (büyük yapılar, düşük kontrast) geçirir.
        """
        if self.current_image is None:
            return
            
        # Görüntü gri tonlamada değilse çevir
        if len(self.current_image.shape) > 2:
            gray_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = self.current_image.copy()
        
        # Yeni bir dialog penceresi oluştur
        lowpass_dialog = tk.Toplevel(self.root)
        lowpass_dialog.title("Fourier Alçak Geçiren Filtre")
        lowpass_dialog.geometry("400x250")
        lowpass_dialog.resizable(False, False)
        
        # Yarıçap için slider
        Label(lowpass_dialog, text="Filtre Yarıçapı:").pack(pady=5)
        radius_scale = Scale(lowpass_dialog, from_=10, to=200, resolution=1, orient=HORIZONTAL, length=300)
        radius_scale.set(50)  # Varsayılan değer
        radius_scale.pack(pady=5)
        
        # Görüntü önizleme için
        preview_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(lowpass_dialog, text="Genlik Spektrumunu Göster", variable=preview_var).pack(pady=5)
        
        # Uygula butonu
        def apply_lowpass_filter():
            radius = radius_scale.get()
            show_spectrum = preview_var.get()
            self.apply_fourier_lowpass(radius, gray_image, show_spectrum)
            lowpass_dialog.destroy()  # Dialog penceresini kapat
        
        Button(lowpass_dialog, text="Uygula", command=apply_lowpass_filter, width=15).pack(pady=10)
    
    def apply_fourier_lowpass(self, radius, gray_image, show_spectrum=False):
        """
        Görüntüye Fourier Alçak Geçiren Filtre uygular.
        
        Parametreler:
            radius: Filtre yarıçapı
            gray_image: Gri tonlamalı görüntü
            show_spectrum: Genlik spektrumunu gösterme seçeneği
        """
        # Fourier dönüşümünü hesapla
        _, _, dft_shift = self._fourier_transform(gray_image)
        
        # Görüntü merkez koordinatlarını bul
        rows, cols = gray_image.shape
        crow, ccol = rows // 2, cols // 2
        
        # Merkez etrafında belirli yarıçapta maske oluştur
        mask = np.zeros((rows, cols, 2), np.uint8)
        center = [crow, ccol]
        x, y = np.ogrid[:rows, :cols]
        mask_area = (x - center[0]) ** 2 + (y - center[1]) ** 2 <= radius ** 2
        mask[mask_area] = 1
        
        # Filtreyi uygula
        filtered_dft = dft_shift * mask
        
        # Görüntüyü geri oluştur
        filtered_image = self._inverse_fourier_transform(filtered_dft, (rows, cols))
        
        # Genlik spektrumunu gösterme seçeneği
        if show_spectrum:
            # Filtreli spektrumu hesapla
            filtered_spectrum = 20 * np.log(cv2.magnitude(filtered_dft[:,:,0], filtered_dft[:,:,1]) + 1)
            
            # Yan yana göstermek için
            result = np.hstack((filtered_image, cv2.normalize(filtered_spectrum, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)))
            cv2.imshow("Alçak Geçiren Filtre ve Spektrum", result)
        
        # Renkli görüntüye uygula (her kanalı ayrı filtrele)
        if len(self.current_image.shape) > 2:
            result = np.zeros_like(self.current_image)
            for i in range(3):
                # Her kanal için Fourier dönüşümünü hesapla
                channel = self.current_image[:,:,i]
                _, _, dft_shift_channel = self._fourier_transform(channel)
                
                # Filtreyi uygula
                filtered_dft_channel = dft_shift_channel * mask
                
                # Kanalı geri oluştur
                result[:,:,i] = self._inverse_fourier_transform(filtered_dft_channel, (rows, cols))
                
            self.current_image = result
        else:
            self.current_image = filtered_image
            
        self.display_image(self.current_image)

    def open_fourier_highpass_dialog(self):
        """
        Fourier Yüksek Geçiren Filtre dialog penceresini açar.
        
        Yüksek geçiren filtre, görüntüdeki düşük frekans bileşenlerini (büyük yapılar, düşük kontrast) 
        zayıflatırken yüksek frekans bileşenlerini (kenar, detay) geçirir.
        """
        if self.current_image is None:
            return
            
        # Görüntü gri tonlamada değilse çevir
        if len(self.current_image.shape) > 2:
            gray_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = self.current_image.copy()
        
        # Yeni bir dialog penceresi oluştur
        highpass_dialog = tk.Toplevel(self.root)
        highpass_dialog.title("Fourier Yüksek Geçiren Filtre")
        highpass_dialog.geometry("400x250")
        highpass_dialog.resizable(False, False)
        
        # Yarıçap için slider
        Label(highpass_dialog, text="Filtre Yarıçapı:").pack(pady=5)
        radius_scale = Scale(highpass_dialog, from_=1, to=100, resolution=1, orient=HORIZONTAL, length=300)
        radius_scale.set(30)  # Varsayılan değer
        radius_scale.pack(pady=5)
        
        # Görüntü önizleme için
        preview_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(highpass_dialog, text="Genlik Spektrumunu Göster", variable=preview_var).pack(pady=5)
        
        # Uygula butonu
        def apply_highpass_filter():
            radius = radius_scale.get()
            show_spectrum = preview_var.get()
            self.apply_fourier_highpass(radius, gray_image, show_spectrum)
            highpass_dialog.destroy()  # Dialog penceresini kapat
        
        Button(highpass_dialog, text="Uygula", command=apply_highpass_filter, width=15).pack(pady=10)
    
    def apply_fourier_highpass(self, radius, gray_image, show_spectrum=False):
        """
        Görüntüye Fourier Yüksek Geçiren Filtre uygular.
        
        Parametreler:
            radius: Filtre yarıçapı
            gray_image: Gri tonlamalı görüntü
            show_spectrum: Genlik spektrumunu gösterme seçeneği
        """
        # Fourier dönüşümünü hesapla
        _, _, dft_shift = self._fourier_transform(gray_image)
        
        # Görüntü merkez koordinatlarını bul
        rows, cols = gray_image.shape
        crow, ccol = rows // 2, cols // 2
        
        # Merkez etrafında belirli yarıçapta maske oluştur (yüksek geçiren filtre için tersi)
        mask = np.ones((rows, cols, 2), np.uint8)
        center = [crow, ccol]
        x, y = np.ogrid[:rows, :cols]
        mask_area = (x - center[0]) ** 2 + (y - center[1]) ** 2 <= radius ** 2
        mask[mask_area] = 0
        
        # Filtreyi uygula
        filtered_dft = dft_shift * mask
        
        # Görüntüyü geri oluştur
        filtered_image = self._inverse_fourier_transform(filtered_dft, (rows, cols))
        
        # Genlik spektrumunu gösterme seçeneği
        if show_spectrum:
            # Filtreli spektrumu hesapla
            filtered_spectrum = 20 * np.log(cv2.magnitude(filtered_dft[:,:,0], filtered_dft[:,:,1]) + 1)
            
            # Yan yana göstermek için
            result = np.hstack((filtered_image, cv2.normalize(filtered_spectrum, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)))
            cv2.imshow("Yüksek Geçiren Filtre ve Spektrum", result)
        
        # Renkli görüntüye uygula (her kanalı ayrı filtrele)
        if len(self.current_image.shape) > 2:
            result = np.zeros_like(self.current_image)
            for i in range(3):
                # Her kanal için Fourier dönüşümünü hesapla
                channel = self.current_image[:,:,i]
                _, _, dft_shift_channel = self._fourier_transform(channel)
                
                # Filtreyi uygula
                filtered_dft_channel = dft_shift_channel * mask
                
                # Kanalı geri oluştur
                result[:,:,i] = self._inverse_fourier_transform(filtered_dft_channel, (rows, cols))
                
            self.current_image = result
        else:
            self.current_image = filtered_image
            
        self.display_image(self.current_image)

    def open_band_pass_dialog(self):
        """
        Bant Geçiren Filtre dialog penceresini açar.
        
        Bant geçiren filtre, görüntüdeki belirli bir frekans aralığını geçirirken
        diğer frekansları zayıflatır. Bu, belirli bir ölçek seviyesindeki yapıları 
        görüntüde korumak/vurgulamak için kullanılır.
        """
        if self.current_image is None:
            return
            
        # Görüntü gri tonlamada değilse çevir
        if len(self.current_image.shape) > 2:
            gray_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = self.current_image.copy()
        
        # Yeni bir dialog penceresi oluştur
        bandpass_dialog = tk.Toplevel(self.root)
        bandpass_dialog.title("Bant Geçiren Filtre")
        bandpass_dialog.geometry("400x300")
        bandpass_dialog.resizable(False, False)
        
        # İç yarıçap için slider
        Label(bandpass_dialog, text="İç Yarıçap:").pack(pady=5)
        inner_radius_scale = Scale(bandpass_dialog, from_=1, to=100, resolution=1, orient=HORIZONTAL, length=300)
        inner_radius_scale.set(20)  # Varsayılan değer
        inner_radius_scale.pack(pady=5)
        
        # Dış yarıçap için slider
        Label(bandpass_dialog, text="Dış Yarıçap:").pack(pady=5)
        outer_radius_scale = Scale(bandpass_dialog, from_=10, to=200, resolution=1, orient=HORIZONTAL, length=300)
        outer_radius_scale.set(50)  # Varsayılan değer
        outer_radius_scale.pack(pady=5)
        
        # Görüntü önizleme için
        preview_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(bandpass_dialog, text="Genlik Spektrumunu Göster", variable=preview_var).pack(pady=5)
        
        # Uygula butonu
        def apply_band_pass_filter():
            inner_radius = inner_radius_scale.get()
            outer_radius = outer_radius_scale.get()
            
            # İç yarıçap dış yarıçaptan büyük olmamalı
            if inner_radius >= outer_radius:
                messagebox.showerror("Hata", "İç yarıçap dış yarıçaptan küçük olmalıdır!")
                return
                
            show_spectrum = preview_var.get()
            self.apply_band_pass(inner_radius, outer_radius, gray_image, show_spectrum)
            bandpass_dialog.destroy()  # Dialog penceresini kapat
        
        Button(bandpass_dialog, text="Uygula", command=apply_band_pass_filter, width=15).pack(pady=10)
    
    def apply_band_pass(self, inner_radius, outer_radius, gray_image, show_spectrum=False):
        """
        Görüntüye Bant Geçiren Filtre uygular.
        
        Parametreler:
            inner_radius: İç yarıçap (küçük değer)
            outer_radius: Dış yarıçap (büyük değer)
            gray_image: Gri tonlamalı görüntü
            show_spectrum: Genlik spektrumunu gösterme seçeneği
        """
        # Fourier dönüşümünü hesapla
        _, _, dft_shift = self._fourier_transform(gray_image)
        
        # Görüntü merkez koordinatlarını bul
        rows, cols = gray_image.shape
        crow, ccol = rows // 2, cols // 2
        
        # Bant geçiren maske oluştur
        mask = np.zeros((rows, cols, 2), np.uint8)
        center = [crow, ccol]
        x, y = np.ogrid[:rows, :cols]
        
        # İç ve dış daireler arasındaki alanı hesapla
        mask_area = np.logical_and(
            (x - center[0]) ** 2 + (y - center[1]) ** 2 >= inner_radius ** 2,
            (x - center[0]) ** 2 + (y - center[1]) ** 2 <= outer_radius ** 2
        )
        mask[mask_area] = 1
        
        # Filtreyi uygula
        filtered_dft = dft_shift * mask
        
        # Görüntüyü geri oluştur
        filtered_image = self._inverse_fourier_transform(filtered_dft, (rows, cols))
        
        # Genlik spektrumunu gösterme seçeneği
        if show_spectrum:
            # Filtreli spektrumu hesapla
            filtered_spectrum = 20 * np.log(cv2.magnitude(filtered_dft[:,:,0], filtered_dft[:,:,1]) + 1)
            
            # Yan yana göstermek için
            result = np.hstack((filtered_image, cv2.normalize(filtered_spectrum, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)))
            cv2.imshow("Bant Geçiren Filtre ve Spektrum", result)
        
        # Renkli görüntüye uygula (her kanalı ayrı filtrele)
        if len(self.current_image.shape) > 2:
            result = np.zeros_like(self.current_image)
            for i in range(3):
                # Her kanal için Fourier dönüşümünü hesapla
                channel = self.current_image[:,:,i]
                _, _, dft_shift_channel = self._fourier_transform(channel)
                
                # Filtreyi uygula
                filtered_dft_channel = dft_shift_channel * mask
                
                # Kanalı geri oluştur
                result[:,:,i] = self._inverse_fourier_transform(filtered_dft_channel, (rows, cols))
                
            self.current_image = result
        else:
            self.current_image = filtered_image
            
        self.display_image(self.current_image)

    def open_band_stop_dialog(self):
        """
        Bant Durduran Filtre dialog penceresini açar.
        
        Bant durduran filtre, görüntüdeki belirli bir frekans aralığını zayıflatırken
        diğer frekansları geçirir. Bu, belirli periyodik gürültüleri gidermek için kullanılır.
        """
        if self.current_image is None:
            return
            
        # Görüntü gri tonlamada değilse çevir
        if len(self.current_image.shape) > 2:
            gray_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = self.current_image.copy()
        
        # Yeni bir dialog penceresi oluştur
        bandstop_dialog = tk.Toplevel(self.root)
        bandstop_dialog.title("Bant Durduran Filtre")
        bandstop_dialog.geometry("400x300")
        bandstop_dialog.resizable(False, False)
        
        # İç yarıçap için slider
        Label(bandstop_dialog, text="İç Yarıçap:").pack(pady=5)
        inner_radius_scale = Scale(bandstop_dialog, from_=1, to=100, resolution=1, orient=HORIZONTAL, length=300)
        inner_radius_scale.set(20)  # Varsayılan değer
        inner_radius_scale.pack(pady=5)
        
        # Dış yarıçap için slider
        Label(bandstop_dialog, text="Dış Yarıçap:").pack(pady=5)
        outer_radius_scale = Scale(bandstop_dialog, from_=10, to=200, resolution=1, orient=HORIZONTAL, length=300)
        outer_radius_scale.set(50)  # Varsayılan değer
        outer_radius_scale.pack(pady=5)
        
        # Görüntü önizleme için
        preview_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(bandstop_dialog, text="Genlik Spektrumunu Göster", variable=preview_var).pack(pady=5)
        
        # Uygula butonu
        def apply_band_stop_filter():
            inner_radius = inner_radius_scale.get()
            outer_radius = outer_radius_scale.get()
            
            # İç yarıçap dış yarıçaptan büyük olmamalı
            if inner_radius >= outer_radius:
                messagebox.showerror("Hata", "İç yarıçap dış yarıçaptan küçük olmalıdır!")
                return
                
            show_spectrum = preview_var.get()
            self.apply_band_stop(inner_radius, outer_radius, gray_image, show_spectrum)
            bandstop_dialog.destroy()  # Dialog penceresini kapat
        
        Button(bandstop_dialog, text="Uygula", command=apply_band_stop_filter, width=15).pack(pady=10)
    
    def apply_band_stop(self, inner_radius, outer_radius, gray_image, show_spectrum=False):
        """
        Görüntüye Bant Durduran Filtre uygular.
        
        Parametreler:
            inner_radius: İç yarıçap (küçük değer)
            outer_radius: Dış yarıçap (büyük değer)
            gray_image: Gri tonlamalı görüntü
            show_spectrum: Genlik spektrumunu gösterme seçeneği
        """
        # Fourier dönüşümünü hesapla
        _, _, dft_shift = self._fourier_transform(gray_image)
        
        # Görüntü merkez koordinatlarını bul
        rows, cols = gray_image.shape
        crow, ccol = rows // 2, cols // 2
        
        # Bant durduran maske oluştur (bant geçiren maskenin tersi)
        mask = np.ones((rows, cols, 2), np.uint8)
        center = [crow, ccol]
        x, y = np.ogrid[:rows, :cols]
        
        # İç ve dış daireler arasındaki alanı hesapla (1 yerine 0 atanacak)
        mask_area = np.logical_and(
            (x - center[0]) ** 2 + (y - center[1]) ** 2 >= inner_radius ** 2,
            (x - center[0]) ** 2 + (y - center[1]) ** 2 <= outer_radius ** 2
        )
        mask[mask_area] = 0
        
        # Filtreyi uygula
        filtered_dft = dft_shift * mask
        
        # Görüntüyü geri oluştur
        filtered_image = self._inverse_fourier_transform(filtered_dft, (rows, cols))
        
        # Genlik spektrumunu gösterme seçeneği
        if show_spectrum:
            # Filtreli spektrumu hesapla
            filtered_spectrum = 20 * np.log(cv2.magnitude(filtered_dft[:,:,0], filtered_dft[:,:,1]) + 1)
            
            # Yan yana göstermek için
            result = np.hstack((filtered_image, cv2.normalize(filtered_spectrum, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)))
            cv2.imshow("Bant Durduran Filtre ve Spektrum", result)
        
        # Renkli görüntüye uygula (her kanalı ayrı filtrele)
        if len(self.current_image.shape) > 2:
            result = np.zeros_like(self.current_image)
            for i in range(3):
                # Her kanal için Fourier dönüşümünü hesapla
                channel = self.current_image[:,:,i]
                _, _, dft_shift_channel = self._fourier_transform(channel)
                
                # Filtreyi uygula
                filtered_dft_channel = dft_shift_channel * mask
                
                # Kanalı geri oluştur
                result[:,:,i] = self._inverse_fourier_transform(filtered_dft_channel, (rows, cols))
                
            self.current_image = result
        else:
            self.current_image = filtered_image
            
        self.display_image(self.current_image)

    def open_butterworth_filter_dialog(self):
        """
        Butterworth Filtre dialog penceresini açar.
        
        Butterworth filtre, keskin geçişler olmadan frekans bileşenlerini yumuşak bir şekilde
        filtrelemek için kullanılır. Hem düşük geçiren hem de yüksek geçiren versiyonları mevcuttur.
        """
        if self.current_image is None:
            return
            
        # Görüntü gri tonlamada değilse çevir
        if len(self.current_image.shape) > 2:
            gray_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = self.current_image.copy()
        
        # Yeni bir dialog penceresi oluştur
        butterworth_dialog = tk.Toplevel(self.root)
        butterworth_dialog.title("Butterworth Filtre")
        butterworth_dialog.geometry("400x300")
        butterworth_dialog.resizable(False, False)
        
        # Filtre tipi seçimi
        Label(butterworth_dialog, text="Filtre Tipi:").pack(pady=5)
        filter_type_var = tk.StringVar(value="lowpass")
        filter_types = [("Alçak Geçiren", "lowpass"), ("Yüksek Geçiren", "highpass")]
        
        for text, value in filter_types:
            ttk.Radiobutton(butterworth_dialog, text=text, variable=filter_type_var, value=value).pack(anchor=tk.W, padx=20)
        
        # Kesim frekansı (D0) için slider
        Label(butterworth_dialog, text="Kesim Frekansı (D0):").pack(pady=5)
        d0_scale = Scale(butterworth_dialog, from_=1, to=100, resolution=1, orient=HORIZONTAL, length=300)
        d0_scale.set(30)  # Varsayılan değer
        d0_scale.pack(pady=5)
        
        # Filtre derecesi (n) için slider
        Label(butterworth_dialog, text="Filtre Derecesi (n):").pack(pady=5)
        n_scale = Scale(butterworth_dialog, from_=1, to=10, resolution=1, orient=HORIZONTAL, length=300)
        n_scale.set(2)  # Varsayılan değer
        n_scale.pack(pady=5)
        
        # Görüntü önizleme için
        preview_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(butterworth_dialog, text="Genlik Spektrumunu Göster", variable=preview_var).pack(pady=5)
        
        # Uygula butonu
        def apply_butterworth_filter():
            filter_type = filter_type_var.get()
            d0 = d0_scale.get()
            n = n_scale.get()
            show_spectrum = preview_var.get()
            self.apply_butterworth(filter_type, d0, n, gray_image, show_spectrum)
            butterworth_dialog.destroy()  # Dialog penceresini kapat
        
        Button(butterworth_dialog, text="Uygula", command=apply_butterworth_filter, width=15).pack(pady=10)
    
    def apply_butterworth(self, filter_type, d0, n, gray_image, show_spectrum=False):
        """
        Görüntüye Butterworth Filtre uygular.
        
        Parametreler:
            filter_type: Filtre tipi ('lowpass' veya 'highpass')
            d0: Kesim frekansı
            n: Filtre derecesi
            gray_image: Gri tonlamalı görüntü
            show_spectrum: Genlik spektrumunu gösterme seçeneği
        """
        # Fourier dönüşümünü hesapla
        _, _, dft_shift = self._fourier_transform(gray_image)
        
        # Görüntü merkez koordinatlarını bul
        rows, cols = gray_image.shape
        crow, ccol = rows // 2, cols // 2
        
        # Butterworth filtre maskesini oluştur
        mask = np.zeros((rows, cols, 2), np.float32)
        
        for i in range(rows):
            for j in range(cols):
                # Merkeze olan uzaklığı hesapla
                d = np.sqrt((i - crow) ** 2 + (j - ccol) ** 2)
                
                # Butterworth filtre fonksiyonunu uygula
                if filter_type == 'lowpass':
                    # Alçak geçiren Butterworth filtre
                    mask[i, j] = 1 / (1 + (d / d0) ** (2 * n))
                else:
                    # Yüksek geçiren Butterworth filtre
                    mask[i, j] = 1 / (1 + (d0 / (d + 0.000001)) ** (2 * n))
        
        # Filtreyi uygula
        filtered_dft = dft_shift * mask
        
        # Görüntüyü geri oluştur
        filtered_image = self._inverse_fourier_transform(filtered_dft, (rows, cols))
        
        # Genlik spektrumunu gösterme seçeneği
        if show_spectrum:
            # Filtreli spektrumu hesapla
            filtered_spectrum = 20 * np.log(cv2.magnitude(filtered_dft[:,:,0], filtered_dft[:,:,1]) + 1)
            
            # Yan yana göstermek için
            result = np.hstack((filtered_image, cv2.normalize(filtered_spectrum, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)))
            cv2.imshow("Butterworth Filtre ve Spektrum", result)
        
        # Renkli görüntüye uygula (her kanalı ayrı filtrele)
        if len(self.current_image.shape) > 2:
            result = np.zeros_like(self.current_image)
            for i in range(3):
                # Her kanal için Fourier dönüşümünü hesapla
                channel = self.current_image[:,:,i]
                _, _, dft_shift_channel = self._fourier_transform(channel)
                
                # Filtreyi uygula
                filtered_dft_channel = dft_shift_channel * mask
                
                # Kanalı geri oluştur
                result[:,:,i] = self._inverse_fourier_transform(filtered_dft_channel, (rows, cols))
                
            self.current_image = result
        else:
            self.current_image = filtered_image
            
        self.display_image(self.current_image)

    def open_gaussian_freq_dialog(self):
        """
        Frekans Uzayı Gaussian Filtreleme dialog penceresini açar.
        
        Gaussian filtreleri, Butterworth filtrelerden daha yumuşak geçişler sağlar.
        Hem düşük geçiren hem de yüksek geçiren versiyonları mevcuttur.
        """
        if self.current_image is None:
            return
            
        # Görüntü gri tonlamada değilse çevir
        if len(self.current_image.shape) > 2:
            gray_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = self.current_image.copy()
        
        # Yeni bir dialog penceresi oluştur
        gaussian_filter_dialog = tk.Toplevel(self.root)
        gaussian_filter_dialog.title("Frekans Uzayı Gaussian Filtre")
        gaussian_filter_dialog.geometry("400x300")
        gaussian_filter_dialog.resizable(False, False)
        
        # Filtre tipi seçimi
        Label(gaussian_filter_dialog, text="Filtre Tipi:").pack(pady=5)
        filter_type_var = tk.StringVar(value="lowpass")
        filter_types = [("Alçak Geçiren", "lowpass"), ("Yüksek Geçiren", "highpass")]
        
        for text, value in filter_types:
            ttk.Radiobutton(gaussian_filter_dialog, text=text, variable=filter_type_var, value=value).pack(anchor=tk.W, padx=20)
        
        # Sigma değeri için slider
        Label(gaussian_filter_dialog, text="Sigma Değeri:").pack(pady=5)
        sigma_scale = Scale(gaussian_filter_dialog, from_=1, to=100, resolution=1, orient=HORIZONTAL, length=300)
        sigma_scale.set(30)  # Varsayılan değer
        sigma_scale.pack(pady=5)
        
        # Görüntü önizleme için
        preview_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(gaussian_filter_dialog, text="Genlik Spektrumunu Göster", variable=preview_var).pack(pady=5)
        
        # Uygula butonu
        def apply_gaussian_filter_freq():
            filter_type = filter_type_var.get()
            sigma = sigma_scale.get()
            show_spectrum = preview_var.get()
            self.apply_gaussian_freq(filter_type, sigma, gray_image, show_spectrum)
            gaussian_filter_dialog.destroy()  # Dialog penceresini kapat
        
        Button(gaussian_filter_dialog, text="Uygula", command=apply_gaussian_filter_freq, width=15).pack(pady=10)
    
    def apply_gaussian_freq(self, filter_type, sigma, gray_image, show_spectrum=False):
        """
        Görüntüye frekans uzayında Gaussian Filtre uygular.
        
        Parametreler:
            filter_type: Filtre tipi ('lowpass' veya 'highpass')
            sigma: Gaussian fonksiyonunun standart sapması
            gray_image: Gri tonlamalı görüntü
            show_spectrum: Genlik spektrumunu gösterme seçeneği
        """
        # Fourier dönüşümünü hesapla
        _, _, dft_shift = self._fourier_transform(gray_image)
        
        # Görüntü merkez koordinatlarını bul
        rows, cols = gray_image.shape
        crow, ccol = rows // 2, cols // 2
        
        # Gaussian filtre maskesini oluştur
        mask = np.zeros((rows, cols, 2), np.float32)
        
        for i in range(rows):
            for j in range(cols):
                # Merkeze olan uzaklığı hesapla
                d_squared = (i - crow) ** 2 + (j - ccol) ** 2
                
                # Gaussian filtre fonksiyonunu uygula
                if filter_type == 'lowpass':
                    # Alçak geçiren Gaussian filtre
                    mask[i, j] = np.exp(-d_squared / (2 * sigma ** 2))
                else:
                    # Yüksek geçiren Gaussian filtre
                    mask[i, j] = 1 - np.exp(-d_squared / (2 * sigma ** 2))
        
        # Filtreyi uygula
        filtered_dft = dft_shift * mask
        
        # Görüntüyü geri oluştur
        filtered_image = self._inverse_fourier_transform(filtered_dft, (rows, cols))
        
        # Genlik spektrumunu gösterme seçeneği
        if show_spectrum:
            # Filtreli spektrumu hesapla
            filtered_spectrum = 20 * np.log(cv2.magnitude(filtered_dft[:,:,0], filtered_dft[:,:,1]) + 1)
            
            # Yan yana göstermek için
            result = np.hstack((filtered_image, cv2.normalize(filtered_spectrum, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)))
            cv2.imshow("Gaussian Filtre ve Spektrum", result)
        
        # Renkli görüntüye uygula (her kanalı ayrı filtrele)
        if len(self.current_image.shape) > 2:
            result = np.zeros_like(self.current_image)
            for i in range(3):
                # Her kanal için Fourier dönüşümünü hesapla
                channel = self.current_image[:,:,i]
                _, _, dft_shift_channel = self._fourier_transform(channel)
                
                # Filtreyi uygula
                filtered_dft_channel = dft_shift_channel * mask
                
                # Kanalı geri oluştur
                result[:,:,i] = self._inverse_fourier_transform(filtered_dft_channel, (rows, cols))
                
            self.current_image = result
        else:
            self.current_image = filtered_image
            
        self.display_image(self.current_image)

    def apply_homomorphic_filter(self):
        """
        Homomorfik filtre uygulamak için bir dialog penceresi açar.
        
        Homomorfik filtre, aydınlatma varyasyonlarını azaltırken görüntü detaylarını korumak için kullanılır.
        Logaritmik dönüşüm ve Fourier dönüşümü kombinasyonu kullanarak çalışır.
        Aydınlatma (düşük frekans) bileşenlerini azaltır ve reflektans (yüksek frekans) bileşenlerini güçlendirir.
        """
        if self.current_image is None:
            return
            
        # Görüntü gri tonlamada değilse çevir
        if len(self.current_image.shape) > 2:
            gray_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = self.current_image.copy()
        
        # Yeni bir dialog penceresi oluştur
        homomorphic_dialog = tk.Toplevel(self.root)
        homomorphic_dialog.title("Homomorfik Filtre")
        homomorphic_dialog.geometry("400x350")
        homomorphic_dialog.resizable(False, False)
        
        # Gamma Yüksek (yüksek frekans güçlendirme) için slider
        Label(homomorphic_dialog, text="Gamma Yüksek (γH):").pack(pady=5)
        gamma_h_scale = Scale(homomorphic_dialog, from_=1.0, to=3.0, resolution=0.1, orient=HORIZONTAL, length=300)
        gamma_h_scale.set(1.5)  # Varsayılan değer
        gamma_h_scale.pack(pady=5)
        
        # Gamma Düşük (düşük frekans zayıflatma) için slider
        Label(homomorphic_dialog, text="Gamma Düşük (γL):").pack(pady=5)
        gamma_l_scale = Scale(homomorphic_dialog, from_=0.1, to=1.0, resolution=0.1, orient=HORIZONTAL, length=300)
        gamma_l_scale.set(0.5)  # Varsayılan değer
        gamma_l_scale.pack(pady=5)
        
        # Kesim frekansı (D0) için slider
        Label(homomorphic_dialog, text="Kesim Frekansı (D0):").pack(pady=5)
        d0_scale = Scale(homomorphic_dialog, from_=10, to=100, resolution=1, orient=HORIZONTAL, length=300)
        d0_scale.set(30)  # Varsayılan değer
        d0_scale.pack(pady=5)
        
        # Görüntü önizleme için
        preview_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(homomorphic_dialog, text="Genlik Spektrumunu Göster", variable=preview_var).pack(pady=5)
        
        # Uygula butonu
        def apply_homomorphic_filter():
            gamma_h = gamma_h_scale.get()
            gamma_l = gamma_l_scale.get()
            d0 = d0_scale.get()
            show_spectrum = preview_var.get()
            self.apply_homomorphic(gamma_h, gamma_l, d0, gray_image, show_spectrum)
            homomorphic_dialog.destroy()  # Dialog penceresini kapat
        
        Button(homomorphic_dialog, text="Uygula", command=apply_homomorphic_filter, width=15).pack(pady=10)
    
    def apply_homomorphic(self, gamma_h, gamma_l, d0, gray_image, show_spectrum=False):
        """
        Görüntüye homomorfik filtre uygular.
        
        Parametreler:
            gamma_h: Yüksek frekans bileşenleri için gamma değeri (1.0'dan büyük)
            gamma_l: Düşük frekans bileşenleri için gamma değeri (1.0'dan küçük)
            d0: Kesim frekansı
            gray_image: Gri tonlamalı görüntü
            show_spectrum: Genlik spektrumunu gösterme seçeneği
        """
        # Görüntüye küçük bir değer ekleyip logaritmasını al (0 değerlerini önlemek için)
        # ln(I) = ln(L) + ln(R), burada I görüntü, L aydınlatma, R reflektans
        img_log = np.log1p(np.array(gray_image, dtype="float"))
        
        # Fourier dönüşümünü hesapla
        img_fft = np.fft.fft2(img_log)
        
        # Düşük frekans bileşenlerini merkeze taşı
        img_fft_shift = np.fft.fftshift(img_fft)
        
        # Görüntü boyutlarını al
        rows, cols = gray_image.shape
        crow, ccol = rows // 2, cols // 2
        
        # Homomorfik filtre maskesi oluştur
        y, x = np.ogrid[0:rows, 0:cols]
        d = np.sqrt((y - crow) ** 2 + (x - ccol) ** 2)
        mask = gamma_l + (gamma_h - gamma_l) * (1 - np.exp(-((d ** 2) / (2 * (d0 ** 2)))))
        
        # Filtreyi uygula
        img_fft_shift_filtered = img_fft_shift * mask
        
        # Genlik spektrumunu gösterme seçeneği
        if show_spectrum:
            # Maskeyi normalize edip göster
            mask_normalized = cv2.normalize(mask, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            
            # Fourier genlik spektrumunu hesapla
            magnitude_spectrum = 20 * np.log(np.abs(img_fft_shift) + 1)
            magnitude_spectrum_normalized = cv2.normalize(magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            
            # Filtreli Fourier genlik spektrumunu hesapla
            filtered_spectrum = 20 * np.log(np.abs(img_fft_shift_filtered) + 1)
            filtered_spectrum_normalized = cv2.normalize(filtered_spectrum, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            
            # Maskeyi ve spektrumları göster
            cv2.imshow("Filtre Maskesi", mask_normalized)
            cv2.imshow("Orijinal Spektrum", magnitude_spectrum_normalized)
            cv2.imshow("Filtreli Spektrum", filtered_spectrum_normalized)
        
        # Merkez kaydırmasını geri al
        img_fft_filtered = np.fft.ifftshift(img_fft_shift_filtered)
        
        # Ters Fourier dönüşümünü hesapla
        img_ifft = np.fft.ifft2(img_fft_filtered)
        
        # Kompleks sayıların gerçek kısmını al
        img_ifft_real = np.real(img_ifft)
        
        # Logaritmik dönüşümün tersini al
        img_exp = np.expm1(img_ifft_real)
        
        # Görüntüyü 0-255 aralığına normalize et
        img_exp = cv2.normalize(img_exp, None, 0, 255, cv2.NORM_MINMAX)
        img_out = np.uint8(img_exp)
        
        # Renkli görüntüye uygula (her kanalı ayrı filtrele)
        if len(self.current_image.shape) > 2:
            result = np.zeros_like(self.current_image)
            for i in range(3):
                # Her kanal için işlemi tekrarla
                channel = self.current_image[:,:,i]
                
                # Görüntüye küçük bir değer ekleyip logaritmasını al
                channel_log = np.log1p(np.array(channel, dtype="float"))
                
                # Fourier dönüşümünü hesapla
                channel_fft = np.fft.fft2(channel_log)
                
                # Düşük frekans bileşenlerini merkeze taşı
                channel_fft_shift = np.fft.fftshift(channel_fft)
                
                # Filtreyi uygula
                channel_fft_shift_filtered = channel_fft_shift * mask
                
                # Merkez kaydırmasını geri al
                channel_fft_filtered = np.fft.ifftshift(channel_fft_shift_filtered)
                
                # Ters Fourier dönüşümünü hesapla
                channel_ifft = np.fft.ifft2(channel_fft_filtered)
                
                # Kompleks sayıların gerçek kısmını al
                channel_ifft_real = np.real(channel_ifft)
                
                # Logaritmik dönüşümün tersini al
                channel_exp = np.expm1(channel_ifft_real)
                
                # Görüntüyü 0-255 aralığına normalize et
                channel_exp = cv2.normalize(channel_exp, None, 0, 255, cv2.NORM_MINMAX)
                result[:,:,i] = np.uint8(channel_exp)
                
            self.current_image = result
        else:
            self.current_image = img_out
            
        self.display_image(self.current_image)

    def apply_sobel_filter(self):
        """
        Sobel filtresi uygulamak için bir dialog penceresi açar.
        
        Sobel filtresi, kenarları güçlendiren bir filtre türüdür.
        """
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

    def apply_prewitt_filter(self):
        """
        Prewitt filtresi uygulamak için bir dialog penceresi açar.
        
        Prewitt filtresi, kenarları güçlendiren bir filtre türüdür.
        """
        if self.current_image is None:
            return
            
        gray_image = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2GRAY)
        
        # Prewitt çekirdekleri
        kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        kernel_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
        
        # Prewitt filtresi uygula
        grad_x = cv2.filter2D(gray_image, cv2.CV_64F, kernel_x)
        grad_y = cv2.filter2D(gray_image, cv2.CV_64F, kernel_y)
        
        # Gradyan büyüklüğünü hesapla
        gradient_magnitude = cv2.magnitude(grad_x, grad_y)
        
        # Gradyan büyüklüğünü normalize et
        prewitt_output = cv2.normalize(gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        
        # Tek kanallı görüntüyü 3 kanallı görüntüye dönüştür (gösterim için)
        self.current_image = cv2.cvtColor(prewitt_output, cv2.COLOR_GRAY2RGB)
        self.display_image(self.current_image)

    def apply_roberts_cross_filter(self):
        """
        Roberts Cross filtresi uygulamak için bir dialog penceresi açar.
        
        Roberts Cross filtresi, kenarları güçlendiren bir filtre türüdür.
        """
        if self.current_image is None:
            return
            
        gray_image = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2GRAY)
        
        # Roberts Cross çekirdekleri
        kernel_x = np.array([[1, 0], [0, -1]])
        kernel_y = np.array([[0, 1], [-1, 0]])
        
        # Roberts Cross filtresi uygula
        grad_x = cv2.filter2D(gray_image, cv2.CV_64F, kernel_x)
        grad_y = cv2.filter2D(gray_image, cv2.CV_64F, kernel_y)
        
        # Gradyan büyüklüğünü hesapla
        gradient_magnitude = cv2.magnitude(grad_x, grad_y)
        
        # Gradyan büyüklüğünü normalize et
        roberts_output = cv2.normalize(gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        
        # Tek kanallı görüntüyü 3 kanallı görüntüye dönüştür (gösterim için)
        self.current_image = cv2.cvtColor(roberts_output, cv2.COLOR_GRAY2RGB)
        self.display_image(self.current_image)

    def apply_compass_filter(self):
        """
        Compass filtresi uygulamak için bir dialog penceresi açar.
        
        Compass filtresi, kenarları güçlendiren bir filtre türüdür.
        """
        if self.current_image is None:
            return
            
        gray_image = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2GRAY)
        
        # Compass çekirdekleri (Kirsch operatörü gibi)
        kernels = [
            np.array([[5, 5, 5], [-3, 0, -3], [-3, -3, -3]]),  # Kuzey
            np.array([[5, 5, -3], [5, 0, -3], [-3, -3, -3]]),  # Kuzeydoğu
            np.array([[5, -3, -3], [5, 0, -3], [5, -3, -3]]),  # Doğu
            np.array([[-3, -3, -3], [5, 0, -3], [5, 5, -3]]),  # Güneydoğu
            np.array([[-3, -3, -3], [-3, 0, -3], [5, 5, 5]]),  # Güney
            np.array([[-3, -3, -3], [-3, 0, 5], [-3, 5, 5]]),  # Güneybatı
            np.array([[-3, -3, 5], [-3, 0, 5], [-3, -3, 5]]),  # Batı
            np.array([[-3, 5, 5], [-3, 0, 5], [-3, -3, -3]])   # Kuzeybatı
        ]
        
        # Her bir çekirdekle konvolüsyon yap
        max_gradient = np.zeros_like(gray_image, dtype=np.float64)
        for kernel in kernels:
            gradient = cv2.filter2D(gray_image, cv2.CV_64F, kernel)
            np.maximum(max_gradient, np.abs(gradient), out=max_gradient) # En büyük gradyanı al
            
        # Sonucu normalize et
        compass_output = cv2.normalize(max_gradient, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        
        # Tek kanallı görüntüyü 3 kanallı görüntüye dönüştür (gösterim için)
        self.current_image = cv2.cvtColor(compass_output, cv2.COLOR_GRAY2RGB)
        self.display_image(self.current_image)

    def open_canny_dialog(self):
        """
        Canny kenar algılama için eşik değerlerini ayarlamak üzere bir dialog penceresi açar.
        """
        if self.current_image is None:
            return
            
        # Yeni bir dialog penceresi oluştur
        canny_dialog = tk.Toplevel(self.root)
        canny_dialog.title("Canny Kenar Algılama")
        canny_dialog.geometry("300x200")
        canny_dialog.resizable(False, False)
        
        # Düşük eşik değeri için kaydırıcı
        Label(canny_dialog, text="Düşük Eşik Değeri:").pack(pady=5)
        low_threshold_scale = Scale(canny_dialog, from_=0, to=255, orient=HORIZONTAL, length=200)
        low_threshold_scale.set(100)  # Varsayılan değer
        low_threshold_scale.pack(pady=5)
        
        # Yüksek eşik değeri için kaydırıcı
        Label(canny_dialog, text="Yüksek Eşik Değeri:").pack(pady=5)
        high_threshold_scale = Scale(canny_dialog, from_=0, to=255, orient=HORIZONTAL, length=200)
        high_threshold_scale.set(200)  # Varsayılan değer
        high_threshold_scale.pack(pady=5)
        
        # Uygula butonu
        def apply_canny_edge_detection():
            low_threshold = low_threshold_scale.get()
            high_threshold = high_threshold_scale.get()
            self.apply_canny_filter(low_threshold, high_threshold)
            canny_dialog.destroy()  # Dialog penceresini kapat
            
        Button(canny_dialog, text="Uygula", command=apply_canny_edge_detection).pack(pady=10)

    def apply_canny_filter(self, low_threshold, high_threshold):
        """
        Canny kenar algılama filtresini uygular.
        
        Parametreler:
            low_threshold (int): Düşük eşik değeri
            high_threshold (int): Yüksek eşik değeri
        """
        if self.current_image is None:
            return
            
        gray_image = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2GRAY)
        
        # Canny kenar algılama uygula
        edges = cv2.Canny(gray_image, low_threshold, high_threshold)
        
        # Tek kanallı görüntüyü 3 kanallı görüntüye dönüştür (gösterim için)
        self.current_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        self.display_image(self.current_image)

    def apply_laplacian_filter(self):
        """
        Laplace filtresi uygular. Kenarları vurgulamak için kullanılır.
        """
        if self.current_image is None:
            messagebox.showerror("Hata", "Lütfen önce bir görüntü açın.")
            return

        gray_image = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2GRAY)
        laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
        laplacian_abs = cv2.convertScaleAbs(laplacian) # Mutlak değeri alıp 8-bit'e çevir

        self.current_image = cv2.cvtColor(laplacian_abs, cv2.COLOR_GRAY2RGB)
        self.display_image(self.current_image)

    def open_gabor_filter_dialog(self):
        """
        Gabor filtresi parametrelerini ayarlamak için bir dialog penceresi açar.
        """
        if self.current_image is None:
            messagebox.showerror("Hata", "Lütfen önce bir görüntü açın.")
            return

        gabor_dialog = tk.Toplevel(self.root)
        gabor_dialog.title("Gabor Filtresi Ayarları")
        gabor_dialog.geometry("350x480") # Yükseklik 400'den 480'e çıkarıldı
        gabor_dialog.resizable(False, False)

        Label(gabor_dialog, text="Çekirdek Boyutu (ksize):").pack(pady=5)
        ksize_scale = Scale(gabor_dialog, from_=1, to=31, orient=HORIZONTAL, length=300)
        ksize_scale.set(15) # Tek sayı olmalı
        ksize_scale.pack(pady=2)
        
        Label(gabor_dialog, text="Sigma (σ):").pack(pady=5)
        sigma_scale = Scale(gabor_dialog, from_=1.0, to=10.0, resolution=0.1, orient=HORIZONTAL, length=300)
        sigma_scale.set(5.0)
        sigma_scale.pack(pady=2)

        Label(gabor_dialog, text="Theta (θ) - Açı (Derece):").pack(pady=5)
        theta_scale = Scale(gabor_dialog, from_=0, to=180, resolution=15, orient=HORIZONTAL, length=300) # 0, np.pi/4, np.pi/2, 3*np.pi/4
        theta_scale.set(90)
        theta_scale.pack(pady=2)

        Label(gabor_dialog, text="Lambda (λ) - Dalga Boyu:").pack(pady=5)
        lambd_scale = Scale(gabor_dialog, from_=1.0, to=20.0, resolution=0.5, orient=HORIZONTAL, length=300)
        lambd_scale.set(10.0)
        lambd_scale.pack(pady=2)

        Label(gabor_dialog, text="Gamma (γ) - En Boy Oranı:").pack(pady=5)
        gamma_scale = Scale(gabor_dialog, from_=0.1, to=1.0, resolution=0.1, orient=HORIZONTAL, length=300)
        gamma_scale.set(0.5)
        gamma_scale.pack(pady=2)

        # Psi (φ) - Faz Ofseti (Radyan)
        # Genellikle 0 veya np.pi/2 kullanılır. Basitlik için şimdilik 0.
        # Label(gabor_dialog, text="Psi (φ) - Faz Ofseti:").pack(pady=5)
        # psi_scale = Scale(gabor_dialog, from_=0, to=np.pi, resolution=np.pi/4, orient=HORIZONTAL, length=300)
        # psi_scale.set(0)
        # psi_scale.pack(pady=2)

        def apply_gabor():
            ksize = int(ksize_scale.get())
            if ksize % 2 == 0: # Ksize tek olmalı
                ksize +=1
            sigma = float(sigma_scale.get())
            theta = float(theta_scale.get()) * np.pi / 180.0 # Dereceyi radyana çevir
            lambd = float(lambd_scale.get())
            gamma = float(gamma_scale.get())
            psi = 0 # np.pi / 2 # Faz ofseti, genellikle 0 veya pi/2
            self.apply_gabor_filter(ksize, sigma, theta, lambd, gamma, psi)
            gabor_dialog.destroy()

        Button(gabor_dialog, text="Uygula", command=apply_gabor).pack(pady=10)
        
    def apply_gabor_filter(self, ksize, sigma, theta, lambd, gamma, psi):
        """
        Görüntüye Gabor filtresi uygular.
        """
        if self.current_image is None:
            return

        gray_image = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2GRAY)
        
        gabor_kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambd, gamma, psi, ktype=cv2.CV_32F)
        filtered_img = cv2.filter2D(gray_image, cv2.CV_8UC3, gabor_kernel)
        
        self.current_image = cv2.cvtColor(filtered_img, cv2.COLOR_GRAY2RGB)
        self.display_image(self.current_image)

    def open_hough_line_dialog(self):
        """
        Hough Çizgi Dönüşümü için parametreleri ayarlamak üzere bir dialog penceresi açar.
        """
        if self.current_image is None:
            messagebox.showerror("Hata", "Lütfen önce bir görüntü açın.")
            return

        hough_dialog = tk.Toplevel(self.root)
        hough_dialog.title("Hough Çizgi Dönüşümü Ayarları")
        hough_dialog.geometry("300x300") # Pencere boyutu ayarlandı
        hough_dialog.resizable(False, False)

        Label(hough_dialog, text="Rho (Piksel Çözünürlüğü):").pack(pady=5)
        rho_scale = Scale(hough_dialog, from_=1, to=10, resolution=1, orient=HORIZONTAL, length=200)
        rho_scale.set(1)
        rho_scale.pack(pady=5)

        Label(hough_dialog, text="Theta (Açı Çözünürlüğü - Derece):").pack(pady=5)
        theta_accuracy_scale = Scale(hough_dialog, from_=1, to=10, resolution=1, orient=HORIZONTAL, length=200) # Derece cinsinden
        theta_accuracy_scale.set(1) # 1 derece hassasiyet
        theta_accuracy_scale.pack(pady=5)

        Label(hough_dialog, text="Eşik Değeri (Threshold):").pack(pady=5)
        threshold_scale = Scale(hough_dialog, from_=10, to=500, resolution=10, orient=HORIZONTAL, length=200)
        threshold_scale.set(150)
        threshold_scale.pack(pady=5)
        
        # Olasılıksal Hough için minLineLength ve maxLineGap eklenebilir.
        # Şimdilik standart HoughLines kullanılıyor.

        def apply_hough():
            rho = int(rho_scale.get())
            theta_accuracy_degrees = int(theta_accuracy_scale.get())
            theta_accuracy_radians = theta_accuracy_degrees * np.pi / 180.0 # Radyana çevir
            threshold = int(threshold_scale.get())
            self.apply_hough_line_transform(rho, theta_accuracy_radians, threshold)
            hough_dialog.destroy()

        Button(hough_dialog, text="Uygula", command=apply_hough).pack(pady=10)

    def apply_hough_line_transform(self, rho, theta_accuracy, threshold):
        """
        Görüntüye Hough Çizgi Dönüşümü uygular ve bulunan çizgileri çizer.
        """
        if self.current_image is None:
            return

        gray_image = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2GRAY)
        # Kenarları bulmak için Canny uygulanır
        edges = cv2.Canny(gray_image, 50, 150, apertureSize=3)

        lines = cv2.HoughLines(edges, rho, theta_accuracy, threshold)

        img_with_lines = self.current_image.copy() # Çizgileri orijinal (veya o anki işlenmiş) renkli görüntü üzerine çiz

        if lines is not None:
            for line in lines:
                rho_val, theta_val = line[0]
                a = np.cos(theta_val)
                b = np.sin(theta_val)
                x0 = a * rho_val
                y0 = b * rho_val
                # x1, y1, x2, y2 noktalarını hesapla (çizginin başlangıç ve bitiş noktaları)
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))
                cv2.line(img_with_lines, (x1, y1), (x2, y2), (0, 0, 255), 2) # Kırmızı çizgiler

        self.current_image = img_with_lines
        self.display_image(self.current_image)
        
    def open_kmeans_segmentation_dialog(self):
        """
        K-Means segmentasyonu için küme sayısını (K) ayarlamak üzere bir dialog açar.
        """
        if self.current_image is None:
            messagebox.showerror("Hata", "Lütfen önce bir görüntü açın.")
            return

        kmeans_dialog = tk.Toplevel(self.root)
        kmeans_dialog.title("K-Means Segmentasyon Ayarları")
        kmeans_dialog.geometry("300x150")
        kmeans_dialog.resizable(False, False)

        Label(kmeans_dialog, text="Küme Sayısı (K):").pack(pady=5)
        k_scale = Scale(kmeans_dialog, from_=2, to=16, resolution=1, orient=HORIZONTAL, length=200)
        k_scale.set(8) # Varsayılan K değeri
        k_scale.pack(pady=5)

        def apply_kmeans():
            k_clusters = int(k_scale.get())
            self.apply_kmeans_segmentation(k_clusters)
            kmeans_dialog.destroy()

        Button(kmeans_dialog, text="Uygula", command=apply_kmeans).pack(pady=10)

    def apply_kmeans_segmentation(self, k_clusters):
        """
        Görüntüye K-Means kümeleme tabanlı segmentasyon uygular.
        """
        if self.current_image is None:
            return

        img_data = self.current_image.reshape((-1, 3)) # Piksel verilerini (R,G,B) formatına getir
        img_data = np.float32(img_data) # cv2.kmeans için float32 olmalı

        # Kümeleme kriterleri ve uygulama
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0) # 10 iterasyon veya epsilon=1.0
        attempts = 10 # Farklı başlangıç merkezleriyle 10 kez çalıştır
        
        # labels: her pikselin hangi kümeye ait olduğu
        # centers: küme merkezlerinin renkleri
        ret, labels, centers = cv2.kmeans(img_data, k_clusters, None, criteria, attempts, cv2.KMEANS_RANDOM_CENTERS)

        centers = np.uint8(centers) # Renk değerlerini uint8'e çevir
        segmented_data = centers[labels.flatten()] # Her pikseli ait olduğu kümenin merkez rengiyle boya
        
        segmented_image = segmented_data.reshape((self.current_image.shape)) # Veriyi orijinal görüntü boyutuna geri getir

        self.current_image = segmented_image
        self.display_image(self.current_image)

    def open_hough_circle_dialog(self):
        """
        Hough Çember Dönüşümü için parametreleri ayarlamak üzere bir dialog penceresi açar.
        """
        if self.current_image is None:
            messagebox.showerror("Hata", "Lütfen önce bir görüntü açın.")
            return

        hough_circle_dialog = tk.Toplevel(self.root)
        hough_circle_dialog.title("Hough Çember Dönüşümü Ayarları")
        hough_circle_dialog.geometry("350x530") # Pencere boyutu 450'den 530'a çıkarıldı
        hough_circle_dialog.resizable(False, False)

        Label(hough_circle_dialog, text="dp (Ters Akümülatör Oranı):").pack(pady=5)
        dp_scale = Scale(hough_circle_dialog, from_=1.0, to=2.0, resolution=0.1, orient=HORIZONTAL, length=300)
        dp_scale.set(1.2)
        dp_scale.pack(pady=2)

        Label(hough_circle_dialog, text="minDist (Merkezler Arası Min Mesafe):").pack(pady=5)
        min_dist_scale = Scale(hough_circle_dialog, from_=10, to=100, resolution=5, orient=HORIZONTAL, length=300)
        min_dist_scale.set(20)
        min_dist_scale.pack(pady=2)

        Label(hough_circle_dialog, text="param1 (Canny Üst Eşiği):").pack(pady=5)
        param1_scale = Scale(hough_circle_dialog, from_=50, to=250, resolution=10, orient=HORIZONTAL, length=300)
        param1_scale.set(100)
        param1_scale.pack(pady=2)

        Label(hough_circle_dialog, text="param2 (Akümülatör Eşiği):").pack(pady=5)
        param2_scale = Scale(hough_circle_dialog, from_=10, to=100, resolution=5, orient=HORIZONTAL, length=300)
        param2_scale.set(30)
        param2_scale.pack(pady=2)

        Label(hough_circle_dialog, text="minRadius (Minimum Yarıçap):").pack(pady=5)
        min_radius_scale = Scale(hough_circle_dialog, from_=0, to=100, resolution=5, orient=HORIZONTAL, length=300)
        min_radius_scale.set(0)
        min_radius_scale.pack(pady=2)

        Label(hough_circle_dialog, text="maxRadius (Maksimum Yarıçap):").pack(pady=5)
        max_radius_scale = Scale(hough_circle_dialog, from_=0, to=200, resolution=5, orient=HORIZONTAL, length=300)
        max_radius_scale.set(0) # 0 -> maksimum olası yarıçapı kullanır
        max_radius_scale.pack(pady=2)

        def apply_hough_circle():
            dp = float(dp_scale.get())
            min_dist = int(min_dist_scale.get())
            param1 = int(param1_scale.get())
            param2 = int(param2_scale.get())
            min_radius = int(min_radius_scale.get())
            max_radius = int(max_radius_scale.get())
            self.apply_hough_circle_transform(dp, min_dist, param1, param2, min_radius, max_radius)
            hough_circle_dialog.destroy()

        Button(hough_circle_dialog, text="Uygula", command=apply_hough_circle).pack(pady=10)

    def apply_hough_circle_transform(self, dp, minDist, param1, param2, minRadius, maxRadius):
        """
        Görüntüye Hough Çember Dönüşümü uygular ve bulunan çemberleri çizer.
        """
        if self.current_image is None:
            return

        # Görüntüyü gri tonlamaya çevir ve biraz bulanıklaştır (gürültüyü azaltmak için)
        gray_image = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2GRAY)
        gray_image = cv2.medianBlur(gray_image, 5) # Median blur genellikle çember algılamada iyi sonuç verir

        # HoughCircles fonksiyonu ile çemberleri algıla
        circles = cv2.HoughCircles(
            gray_image, 
            cv2.HOUGH_GRADIENT, # Algılama metodu
            dp=dp,              # Ters akümülatör çözünürlük oranı (1 ise aynı çözünürlük)
            minDist=minDist,        # Algılanan çemberlerin merkezleri arasındaki minimum mesafe
            param1=param1,        # Canny kenar algılayıcısının üst eşik değeri
            param2=param2,        # Çember merkezleri için akümülatör eşiği (küçükse daha fazla çember bulunur)
            minRadius=minRadius,    # Minimum çember yarıçapı
            maxRadius=maxRadius     # Maksimum çember yarıçapı
        )

        img_with_circles = self.current_image.copy()

        if circles is not None:
            circles = np.uint16(np.around(circles)) # Çember koordinatlarını ve yarıçapını tam sayıya yuvarla
            for i in circles[0, :]:
                # Dış çemberi çiz (yeşil)
                cv2.circle(img_with_circles, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # Merkez noktasını çiz (mavi)
                cv2.circle(img_with_circles, (i[0], i[1]), 2, (0, 0, 255), 3)
        else:
            messagebox.showinfo("Bilgi", "Belirtilen parametrelerle çember bulunamadı.")

        self.current_image = img_with_circles
        self.display_image(self.current_image)

    def open_morph_dialog(self, operation_type):
        """
        Morfolojik işlemler (Erode, Dilate) için bir dialog penceresi açar.
        Kullanıcının çekirdek boyutunu ve iterasyon sayısını belirlemesini sağlar.
        """
        if self.current_image is None:
            messagebox.showerror("Hata", "Lütfen önce bir görüntü açın.")
            return

        morph_dialog = tk.Toplevel(self.root)
        morph_dialog.title(f"{operation_type} Ayarları")
        morph_dialog.geometry("300x250")
        morph_dialog.resizable(False, False)

        Label(morph_dialog, text="Çekirdek Boyutu (örn: 3, 5):" ).pack(pady=5)
        kernel_size_entry = tk.Entry(morph_dialog, width=10)
        kernel_size_entry.insert(0, "3")
        kernel_size_entry.pack(pady=5)

        Label(morph_dialog, text="İterasyon Sayısı:").pack(pady=5)
        iterations_entry = tk.Entry(morph_dialog, width=10)
        iterations_entry.insert(0, "1")
        iterations_entry.pack(pady=5)

        def apply_operation():
            try:
                k_size = int(kernel_size_entry.get())
                iters = int(iterations_entry.get())
                if k_size <= 0 or iters <= 0:
                    messagebox.showerror("Hata", "Çekirdek boyutu ve iterasyon pozitif olmalıdır.")
                    return
                
                kernel = np.ones((k_size, k_size), np.uint8)

                # Görüntüyü gri tonlama ve ikiliye çevir (isteğe bağlı, ama morfolojik işlemler genelde ikili görüntülerde daha anlamlı)
                # Eğer orijinal görüntü üzerinde çalışmak isteniyorsa bu adım atlanabilir veya kullanıcıya seçenek sunulabilir.
                # Şimdilik orijinal (veya o anki işlenmiş) görüntü üzerinde çalışalım.
                # gray_image = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2GRAY)
                # _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
                # target_image = binary_image

                target_image = self.current_image
                processed_image = None

                if operation_type == "Erode":
                    processed_image = cv2.erode(target_image, kernel, iterations=iters)
                elif operation_type == "Dilate":
                    processed_image = cv2.dilate(target_image, kernel, iterations=iters)
                
                if processed_image is not None:
                    # Eğer işlem ikili görüntü üzerinde yapıldıysa ve sonuç tek kanallıysa RGB'ye çevir
                    # if len(processed_image.shape) == 2:
                    #    self.current_image = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2RGB)
                    # else:
                    #    self.current_image = processed_image
                    self.current_image = processed_image # Direkt ata, display_image zaten RGB bekliyor
                    self.display_image(self.current_image)
                
                morph_dialog.destroy()
            except ValueError:
                messagebox.showerror("Hata", "Lütfen geçerli sayılar girin.")

        Button(morph_dialog, text="Uygula", command=apply_operation).pack(pady=20)

# Ana program başlangıcı
# '__main__' kontrolü, bu dosyanın doğrudan çalıştırıldığında çalışmasını sağlar
# (başka bir dosyadan import edildiğinde çalışmaz)
if __name__ == "__main__":
    root = tk.Tk()  # Ana Tkinter penceresi oluştur
    app = GoruntuIslemeUygulamasi(root)  # Uygulama nesnesini oluştur
    root.mainloop()  # Tkinter olay döngüsünü başlat 