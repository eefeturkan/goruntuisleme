import cv2
import numpy as np
import matplotlib.pyplot as plt

def homomorphic_filter(image, d0=30, h_l=0.5, h_h=2, c=1):
    # Görüntüyü gri tona çevir
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Logaritmik dönüşüm
    log_image = np.log1p(np.float32(gray))

    # Fourier dönüşümü
    f_transform = np.fft.fft2(log_image)
    f_transform_shifted = np.fft.fftshift(f_transform)

    # Homomorfik filtre oluştur
    rows, cols = gray.shape
    center = (cols//2, rows//2)
    H = np.zeros((rows, cols), np.float32)

    for u in range(rows):
        for v in range(cols):
            D = np.sqrt((u - center[1])**2 + (v - center[0])**2)
            H[u, v] = (h_h - h_l) * (1 - np.exp(-c * (D**2 / d0**2))) + h_l

    # Filtreyi uygula
    filtered = f_transform_shifted * H
    filtered_image = np.fft.ifft2(np.fft.ifftshift(filtered)).real

    # Üstel dönüşüm
    final_image = np.expm1(filtered_image)
    final_image = np.clip(final_image, 0, 255)

    return np.uint8(final_image)

# Görüntüyü yükle
image = cv2.imread("coins.png")

# Homomorfik filtreyi uygula
filtered_image = homomorphic_filter(image, d0=50, h_l=0.5, h_h=2.0, c=1)

# Sonucu göster
plt.figure(figsize=(12,6))
plt.subplot(1,2,1), plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)), plt.title("Orijinal Görüntü")
plt.subplot(1,2,2), plt.imshow(filtered_image, cmap='gray'), plt.title("Homomorfik Filtre Sonucu")
plt.show()
