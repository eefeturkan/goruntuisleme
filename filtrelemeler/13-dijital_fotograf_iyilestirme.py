import numpy as np
import cv2
import matplotlib.pyplot as plt

# Gaussian yüksek geçiren filtre uygula
image = cv2.imread("blurred_photo.jpg", cv2.IMREAD_GRAYSCALE)
f_transform = np.fft.fft2(image)
f_transform_shifted = np.fft.fftshift(f_transform)

# Gaussian HPF maskesi oluştur
ghpf = np.ones(image.shape, np.float32)
cv2.circle(ghpf, (image.shape[1]//2, image.shape[0]//2), 30, 0, -1)

filtered = f_transform_shifted * ghpf
filtered_image = np.fft.ifft2(np.fft.ifftshift(filtered)).real

# Görüntüyü göster
plt.imshow(filtered_image, cmap='gray')
plt.title("Fourier HPF ile Keskinleştirilmiş Fotoğraf")
plt.show()
