import cv2
import numpy as np
import matplotlib.pyplot as plt

# Görüntüyü yükle
image = cv2.imread("peppers.png")

# 5x5 Medyan Filtresi uygula
median_filtered = cv2.medianBlur(image, 5)

# Görüntüleri göster
plt.figure(figsize=(10,5))
plt.subplot(1,2,1), plt.imshow(image, cmap='gray'), plt.title("Orijinal Görüntü")
plt.subplot(1,2,2), plt.imshow(median_filtered, cmap='gray'), plt.title("Median (Medyan) Filtresi")
plt.show()
