import cv2
import numpy as np
import matplotlib.pyplot as plt

# Görüntüyü yükle ve gri tonlamaya çevir
image = cv2.imread("coins.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Canny kenar tespiti uygula
edges = cv2.Canny(gray, 50, 150)

# Hough Dönüşümü ile doğruları tespit et
lines = cv2.HoughLines(edges, 1, np.pi/180, 200)

# Doğruları görüntüye çiz
output = image.copy()
for line in lines:
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    cv2.line(output, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Sonucu göster
plt.figure(figsize=(10,5))
plt.subplot(1,2,1), plt.imshow(edges, cmap='gray'), plt.title("Canny Kenarlar")
plt.subplot(1,2,2), plt.imshow(output), plt.title("Hough Dönüşümü Sonucu")
plt.show()
