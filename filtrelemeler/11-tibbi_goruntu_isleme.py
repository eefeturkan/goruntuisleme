import numpy as np
import cv2
import matplotlib.pyplot as plt

# MR görüntüsüne Fourier dönüşümü uygulama
image = cv2.imread("tire.png", cv2.IMREAD_GRAYSCALE)
f_transform = np.fft.fft2(image)
f_transform_shifted = np.fft.fftshift(f_transform)

# Alçak geçiren filtre uygula (gürültü azaltma)
lpf_mask = np.zeros(image.shape, np.uint8)
cv2.circle(lpf_mask, (image.shape[1]//2, image.shape[0]//2), 30, 1, -1)
filtered = f_transform_shifted * lpf_mask
filtered_image = np.fft.ifft2(np.fft.ifftshift(filtered)).real

# Görüntüyü göster
plt.imshow(filtered_image, cmap='gray')
plt.title("Fourier LPF ile Gürültü Azaltılmış MR Görüntüsü")
plt.show()
