import cv2
import numpy as np
import matplotlib.pyplot as plt
# Görüntüyü gri tonlamaya çevir ve yükle
image = cv2.imread("cameraman.jpg", cv2.IMREAD_GRAYSCALE)

# Fourier dönüşümünü uygula
f_transform = np.fft.fft2(image)
f_transform_shifted = np.fft.fftshift(f_transform)  # Düşük frekansları merkeze al

# Fourier görüntüsünü göster
magnitude_spectrum = np.log(np.abs(f_transform_shifted))

plt.figure(figsize=(12,6))
plt.subplot(1,4,1)
plt.imshow(image, cmap='gray')
plt.title("Orijinal Görüntü")

plt.subplot(1,4,2)
plt.imshow(magnitude_spectrum, cmap='gray')
plt.title("Fourier Magnitude Spectrum")
#plt.show()
# Band geçiren filtre için parametreler
rows, cols = image.shape
mask = np.zeros((rows, cols), np.uint8)

D1, D2 = 20, 50  # Band genişliği belirleme
center = (cols//2, rows//2)

# Band geçiren filtre maskesi oluştur
for u in range(rows):
    for v in range(cols):
        D = np.sqrt((u - center[1])**2 + (v - center[0])**2)
        if D1 <= D <= D2:
            mask[u, v] = 1  # Sadece belirli aralıktaki frekansları geçir

# Filtreyi uygula
filtered = f_transform_shifted * mask
filtered_image = np.fft.ifft2(np.fft.ifftshift(filtered)).real

plt.subplot(1,4,3)
plt.imshow(filtered_image, cmap='gray')
plt.title("Band Geçiren Filtre Sonucu")
#plt.show()
# Band durduran filtre maskesi oluştur
mask = np.ones((rows, cols), np.uint8)

# Orta frekansları engelle
for u in range(rows):
    for v in range(cols):
        D = np.sqrt((u - center[1])**2 + (v - center[0])**2)
        if D1 <= D <= D2:
            mask[u, v] = 0  # Orta frekansları durdur

# Filtreyi uygula
filtered = f_transform_shifted * mask
filtered_image = np.fft.ifft2(np.fft.ifftshift(filtered)).real

plt.subplot(1,4,4)
plt.imshow(filtered_image, cmap='gray')
plt.title("Band Durduran Filtre Sonucu")
plt.show()

