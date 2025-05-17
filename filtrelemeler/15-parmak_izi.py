import numpy as np
import cv2
import matplotlib.pyplot as plt

# Parmak izi görüntüsünü yükle
image = cv2.imread("fingerprint.jpg", cv2.IMREAD_GRAYSCALE)
f_transform = np.fft.fft2(image)
f_transform_shifted = np.fft.fftshift(f_transform)

# Yüksek geçiren filtre uygula
hpf_mask = np.ones(image.shape, np.uint8)
cv2.circle(hpf_mask, (image.shape[1]//2, image.shape[0]//2), 30, 0, -1)

filtered = f_transform_shifted * hpf_mask
filtered_image = np.fft.ifft2(np.fft.ifftshift(filtered)).real

# Görüntüyü göster
plt.imshow(filtered_image, cmap='gray')
plt.title("Fourier HPF ile Keskinleştirilmiş Parmak İzi")
plt.show()
