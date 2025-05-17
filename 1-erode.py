import cv2
import numpy as np

# Görüntüyü gri tonlamalı olarak yükleyelim
image = cv2.imread('rice.png', cv2.IMREAD_GRAYSCALE)

# Yapısal eleman (3x3'lük bir kare)
kernel = np.ones((3, 3), np.uint8)

# Aşındırma işlemi
eroded_image = cv2.erode(image, kernel, iterations=1)

# Görüntüleri göster
cv2.imshow("Orijinal Görüntü", image)
cv2.imshow("Aşındırılmış Görüntü", eroded_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
