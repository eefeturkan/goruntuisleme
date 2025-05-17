import numpy as np
import cv2
import matplotlib.pyplot as plt

# Uydu görüntüsüne Fourier dönüşümü uygulama
image = cv2.imread("satellite.jpg", cv2.IMREAD_GRAYSCALE)
f_transform = np.fft.fft2(image)
f_transform_shifted = np.fft.fftshift(f_transform)

# Band durduran filtre uygula (atmosferik gürültüyü kaldır)
bsf_mask = np.ones(image.shape, np.uint8)
cv2.circle(bsf_mask, (image.shape[1]//2, image.shape[0]//2), 50, 0, -1)
filtered = f_transform_shifted * bsf_mask
filtered_image = np.fft.ifft2(np.fft.ifftshift(filtered)).real

# Görüntüyü göster
plt.imshow(filtered_image, cmap='gray')
plt.title("Fourier BSF ile Gürültü Azaltılmış Uydu Görüntüsü")
plt.show()
