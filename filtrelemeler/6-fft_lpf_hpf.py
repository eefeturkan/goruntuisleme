import cv2
import numpy as np
import matplotlib.pyplot as plt
# Görüntüyü yükle ve gri tonlamaya çevir
image = cv2.imread("cameraman.jpg", cv2.IMREAD_GRAYSCALE)

# Fourier dönüşümü uygula
f_transform = np.fft.fft2(image)
f_transform_shifted = np.fft.fftshift(f_transform)  # Düşük frekansları merkeze getir

# Fourier görüntüsünü log ölçeğinde göster
magnitude_spectrum = np.log(np.abs(f_transform_shifted))

# Görüntüyü çiz
plt.figure(figsize=(12,6))
plt.subplot(1,4,1)
plt.imshow(image, cmap='gray')
plt.title("Orijinal Görüntü")

plt.subplot(1,4,2)
plt.imshow(magnitude_spectrum, cmap='gray')
plt.title("Fourier Magnitude Spectrum")
#plt.show()

# Filtre boyutu
rows, cols = image.shape
mask = np.zeros((rows, cols), np.uint8)

# Merkez noktasına yakın düşük frekansları bırak, yüksek frekansları sıfır yap
r = 30  # Filtrenin kesme çapı
center = (cols//2, rows//2)
cv2.circle(mask, center, r, 1, -1)

# Filtreyi uygula
filtered = f_transform_shifted * mask
filtered_image = np.fft.ifft2(np.fft.ifftshift(filtered)).real

# Görüntüyü çiz
plt.subplot(1,4,3)
plt.imshow(filtered_image, cmap='gray')
plt.title("Low-Pass Filter Sonucu")
#plt.show()

# High-pass filter maskesi
mask = np.ones((rows, cols), np.uint8)
cv2.circle(mask, center, r, 0, -1)  # Düşük frekansları sıfırla

# Filtreyi uygula
filtered = f_transform_shifted * mask
filtered_image = np.fft.ifft2(np.fft.ifftshift(filtered)).real

# Görüntüyü çiz
plt.subplot(1,4,4)
plt.imshow(filtered_image, cmap='gray')
plt.title("High-Pass Filter Sonucu")
plt.show()


