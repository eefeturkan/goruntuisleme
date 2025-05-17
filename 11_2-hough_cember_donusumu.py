import cv2
import numpy as np
import matplotlib.pyplot as plt

# Görüntüyü yükle ve gri tonlamaya çevir
image = cv2.imread("coins.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Gaussian bulanıklaştırma uygula
blurred = cv2.GaussianBlur(gray, (9, 9), 2)

# Hough Çember Algoritması
circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, 30,
                           param1=50, param2=30, minRadius=10, maxRadius=100)

# Çemberleri çiz
output = image.copy()
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        cv2.circle(output, (i[0], i[1]), i[2], (0, 255, 0), 2)
        cv2.circle(output, (i[0], i[1]), 2, (0, 0, 255), 3)

# Sonucu göster
plt.figure(figsize=(10,5))
plt.subplot(1,2,1), plt.imshow(gray, cmap='gray'), plt.title("Gri Tonlama")
plt.subplot(1,2,2), plt.imshow(output), plt.title("Hough Çember Algılama")
plt.show()
