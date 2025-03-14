import os
import tkinter as tk
from tkinter import filedialog, Scale, Label, Button, Frame, HORIZONTAL, RIDGE, SUNKEN, RAISED
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GoruntuIslemeUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Görüntü İşleme Uygulaması")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        
        # Ana görüntü değişkenleri
        self.original_image = None
        self.current_image = None
        self.file_path = None
        
        # Arayüz bileşenlerini oluştur
        self.create_widgets()
        
    def create_widgets(self):
        # Ana çerçeveler
        self.left_frame = Frame(self.root, width=300, bg="#e0e0e0", relief=RIDGE, borderwidth=2)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        self.right_frame = Frame(self.root, bg="#e0e0e0", relief=RIDGE, borderwidth=2)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Görüntü gösterme alanı
        self.image_frame = Frame(self.right_frame, bg="white", relief=SUNKEN, borderwidth=2)
        self.image_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.image_label = Label(self.image_frame, bg="white")
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        # Histogram gösterme alanı
        self.histogram_frame = Frame(self.right_frame, height=200, bg="white", relief=SUNKEN, borderwidth=2)
        self.histogram_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Kontrol butonları
        self.create_control_buttons()
        
    def create_control_buttons(self):
        # Dosya işlemleri
        file_frame = Frame(self.left_frame, bg="#e0e0e0", relief=RAISED, borderwidth=1)
        file_frame.pack(fill=tk.X, padx=5, pady=5)
        
        Label(file_frame, text="Dosya İşlemleri", bg="#e0e0e0", font=("Arial", 10, "bold")).pack(pady=5)
        
        Button(file_frame, text="Görüntü Aç", command=self.open_image, width=20).pack(pady=2)
        Button(file_frame, text="Görüntüyü Kaydet", command=self.save_image, width=20).pack(pady=2)
        
        # Temel işlemler
        basic_frame = Frame(self.left_frame, bg="#e0e0e0", relief=RAISED, borderwidth=1)
        basic_frame.pack(fill=tk.X, padx=5, pady=5)
        
        Label(basic_frame, text="Temel İşlemler", bg="#e0e0e0", font=("Arial", 10, "bold")).pack(pady=5)
        
        Button(basic_frame, text="Orijinal Görüntü", command=self.show_original, width=20).pack(pady=2)
        Button(basic_frame, text="Gri Tonlama", command=self.convert_to_gray, width=20).pack(pady=2)
        Button(basic_frame, text="RGB Kanallara Ayır", command=self.split_channels, width=20).pack(pady=2)
        Button(basic_frame, text="Negatif", command=self.negative_image, width=20).pack(pady=2)
        
        # Parlaklık ayarı
        brightness_frame = Frame(self.left_frame, bg="#e0e0e0", relief=RAISED, borderwidth=1)
        brightness_frame.pack(fill=tk.X, padx=5, pady=5)
        
        Label(brightness_frame, text="Parlaklık Ayarı", bg="#e0e0e0", font=("Arial", 10, "bold")).pack(pady=5)
        
        self.brightness_scale = Scale(brightness_frame, from_=-100, to=100, orient=HORIZONTAL, 
                                     command=self.adjust_brightness, length=200)
        self.brightness_scale.set(0)
        self.brightness_scale.pack(pady=2)
        
        # Eşikleme
        threshold_frame = Frame(self.left_frame, bg="#e0e0e0", relief=RAISED, borderwidth=1)
        threshold_frame.pack(fill=tk.X, padx=5, pady=5)
        
        Label(threshold_frame, text="Eşikleme", bg="#e0e0e0", font=("Arial", 10, "bold")).pack(pady=5)
        
        self.threshold_scale = Scale(threshold_frame, from_=0, to=255, orient=HORIZONTAL, 
                                    command=self.apply_threshold, length=200)
        self.threshold_scale.set(127)
        self.threshold_scale.pack(pady=2)
        
        # Histogram işlemleri
        histogram_frame = Frame(self.left_frame, bg="#e0e0e0", relief=RAISED, borderwidth=1)
        histogram_frame.pack(fill=tk.X, padx=5, pady=5)
        
        Label(histogram_frame, text="Histogram İşlemleri", bg="#e0e0e0", font=("Arial", 10, "bold")).pack(pady=5)
        
        Button(histogram_frame, text="Histogram Göster", command=self.show_histogram, width=20).pack(pady=2)
        Button(histogram_frame, text="Histogram Eşitleme", command=self.equalize_histogram, width=20).pack(pady=2)
        
        # Kontrast ayarı
        contrast_frame = Frame(self.left_frame, bg="#e0e0e0", relief=RAISED, borderwidth=1)
        contrast_frame.pack(fill=tk.X, padx=5, pady=5)
        
        Label(contrast_frame, text="Kontrast Ayarı", bg="#e0e0e0", font=("Arial", 10, "bold")).pack(pady=5)
        
        self.contrast_scale = Scale(contrast_frame, from_=0.1, to=3.0, resolution=0.1, orient=HORIZONTAL, 
                                   command=self.adjust_contrast, length=200)
        self.contrast_scale.set(1.0)
        self.contrast_scale.pack(pady=2)
        
    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        
        if file_path:
            self.file_path = file_path
            # OpenCV ile görüntüyü oku
            self.original_image = cv2.imread(file_path)
            # BGR'den RGB'ye dönüştür
            self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            self.current_image = self.original_image.copy()
            self.display_image(self.current_image)
            
    def save_image(self):
        if self.current_image is None:
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if file_path:
            # RGB'den BGR'ye dönüştür (OpenCV için)
            save_image = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(file_path, save_image)
            
    def display_image(self, image):
        if image is None:
            return
            
        # Görüntüyü yeniden boyutlandır
        h, w = image.shape[:2]
        max_size = 700
        
        if h > max_size or w > max_size:
            if h > w:
                new_h, new_w = max_size, int(w * max_size / h)
            else:
                new_h, new_w = int(h * max_size / w), max_size
                
            display_img = cv2.resize(image, (new_w, new_h))
        else:
            display_img = image.copy()
            
        # NumPy dizisini PIL Image'e dönüştür
        pil_img = Image.fromarray(display_img)
        # PIL Image'i Tkinter PhotoImage'e dönüştür
        tk_img = ImageTk.PhotoImage(pil_img)
        
        # Görüntüyü göster
        self.image_label.configure(image=tk_img)
        self.image_label.image = tk_img  # Referansı koru
        
    def show_original(self):
        if self.original_image is not None:
            self.current_image = self.original_image.copy()
            self.display_image(self.current_image)
            
    def convert_to_gray(self):
        if self.original_image is None:
            return
            
        gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2GRAY)
        # Gri görüntüyü 3 kanallı RGB'ye dönüştür (gösterim için)
        self.current_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB)
        self.display_image(self.current_image)
        
    def split_channels(self):
        if self.original_image is None:
            return
            
        # Yeni pencere oluştur
        channels_window = tk.Toplevel(self.root)
        channels_window.title("RGB Kanalları")
        channels_window.geometry("800x600")
        
        # Kanalları ayır
        r, g, b = cv2.split(self.original_image)
        
        # Tek kanallı görüntüleri 3 kanallı görüntülere dönüştür
        r_img = np.zeros_like(self.original_image)
        g_img = np.zeros_like(self.original_image)
        b_img = np.zeros_like(self.original_image)
        
        r_img[:,:,0] = r
        g_img[:,:,1] = g
        b_img[:,:,2] = b
        
        # Görüntüleri göster
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
        
        # Yeniden boyutlandır
        pil_r = pil_r.resize((200, 200))
        pil_g = pil_g.resize((200, 200))
        pil_b = pil_b.resize((200, 200))
        
        tk_r = ImageTk.PhotoImage(pil_r)
        tk_g = ImageTk.PhotoImage(pil_g)
        tk_b = ImageTk.PhotoImage(pil_b)
        
        # Etiketlere yerleştir
        label_r = Label(frame_r, image=tk_r)
        label_r.image = tk_r
        label_r.pack()
        
        label_g = Label(frame_g, image=tk_g)
        label_g.image = tk_g
        label_g.pack()
        
        label_b = Label(frame_b, image=tk_b)
        label_b.image = tk_b
        label_b.pack()
        
    def negative_image(self):
        if self.original_image is None:
            return
            
        self.current_image = 255 - self.original_image
        self.display_image(self.current_image)
        
    def adjust_brightness(self, val):
        if self.original_image is None:
            return
            
        brightness = int(val)
        if brightness > 0:
            self.current_image = cv2.add(self.original_image, np.ones_like(self.original_image) * brightness)
        else:
            self.current_image = cv2.subtract(self.original_image, np.ones_like(self.original_image) * abs(brightness))
            
        self.display_image(self.current_image)
        
    def apply_threshold(self, val):
        if self.original_image is None:
            return
            
        threshold = int(val)
        gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2GRAY)
        _, thresholded = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
        
        # Tek kanallı görüntüyü 3 kanallı görüntüye dönüştür
        self.current_image = cv2.cvtColor(thresholded, cv2.COLOR_GRAY2RGB)
        self.display_image(self.current_image)
        
    def show_histogram(self):
        if self.original_image is None:
            return
            
        # Histogram çerçevesini temizle
        for widget in self.histogram_frame.winfo_children():
            widget.destroy()
            
        # Matplotlib figürü oluştur
        fig = plt.Figure(figsize=(10, 2), dpi=100)
        ax = fig.add_subplot(111)
        
        # Gri tonlamalı görüntü için histogram
        if len(self.current_image.shape) == 2 or (len(self.current_image.shape) == 3 and np.array_equal(self.current_image[:,:,0], self.current_image[:,:,1]) and np.array_equal(self.current_image[:,:,0], self.current_image[:,:,2])):
            gray_img = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2GRAY) if len(self.current_image.shape) == 3 else self.current_image
            hist = cv2.calcHist([gray_img], [0], None, [256], [0, 256])
            ax.plot(hist, color='black')
            ax.set_xlim([0, 256])
            ax.set_title('Gri Tonlama Histogramı')
        else:
            # Renkli görüntü için histogram
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
        if self.original_image is None:
            return
            
        # Görüntüyü gri tonlamaya çevir
        gray_img = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2GRAY)
        
        # Histogram eşitleme uygula
        equalized = cv2.equalizeHist(gray_img)
        
        # Tek kanallı görüntüyü 3 kanallı görüntüye dönüştür
        self.current_image = cv2.cvtColor(equalized, cv2.COLOR_GRAY2RGB)
        self.display_image(self.current_image)
        
        # Histogramı göster
        self.show_histogram()
        
    def adjust_contrast(self, val):
        if self.original_image is None:
            return
            
        contrast = float(val)
        self.current_image = cv2.convertScaleAbs(self.original_image, alpha=contrast, beta=0)
        self.display_image(self.current_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = GoruntuIslemeUygulamasi(root)
    root.mainloop() 