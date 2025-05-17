import cv2
import numpy as np
import matplotlib.pyplot as plt

# Görüntüyü yükle
image = cv2.imread("peppers.png", cv2.IMREAD_GRAYSCALE)

# 5x5 Ortalama Filtresi uygula
mean_filtered = cv2.blur(image, (5,5))

# Görüntüleri göster
plt.figure(figsize=(10,5))
plt.subplot(1,2,1), plt.imshow(image, cmap='gray'), plt.title("Orijinal Görüntü")
plt.subplot(1,2,2), plt.imshow(mean_filtered, cmap='gray'), plt.title("Mean (Ortalama) Filtresi")
plt.show()
