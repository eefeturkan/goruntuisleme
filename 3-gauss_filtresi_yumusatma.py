import cv2
import numpy as np
import matplotlib.pyplot as plt
# Görüntüyü oku
image = cv2.imread("peppers.png")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # OpenCV'nin BGR formatını RGB'ye çeviriyoruz

# Orijinal görüntüyü göster
plt.imshow(image)
plt.title("Orijinal Görüntü")
#plt.show()

# 5x5 Gauss filtresi uygula
gaussian_blurred = cv2.GaussianBlur(image, (5,5), 1)

# Görüntüyü göster
plt.imshow(gaussian_blurred)
plt.title("Gaussian Blur (5x5, σ=1)")
#plt.show()

# Farklı Gauss filtreleri uygula
gaussian_3x3 = cv2.GaussianBlur(image, (3,3), 1)
gaussian_7x7 = cv2.GaussianBlur(image, (7,7), 2)
gaussian_9x9 = cv2.GaussianBlur(image, (9,9), 3)

# Görüntüleri yan yana göster
plt.figure(figsize=(12,6))

plt.subplot(1,3,1)
plt.imshow(gaussian_3x3)
plt.title("Gaussian Blur (3x3, σ=1)")

plt.subplot(1,3,2)
plt.imshow(gaussian_7x7)
plt.title("Gaussian Blur (7x7, σ=2)")

plt.subplot(1,3,3)
plt.imshow(gaussian_9x9)
plt.title("Gaussian Blur (9x9, σ=3)")

plt.show()
