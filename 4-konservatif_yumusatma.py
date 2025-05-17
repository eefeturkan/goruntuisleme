import cv2
import numpy as np
import matplotlib.pyplot as plt

def conservative_smoothing(image):
    filtered_image = image.copy()
    shape = image.shape
    
    if len(shape) == 2:  # Gri tonlamalı görüntü
        rows, cols = shape
        channels = 1
    else:  # Renkli görüntü
        rows, cols, channels = shape

    for i in range(1, rows-1):
        for j in range(1, cols-1):
            if channels == 1:  # Gri tonlamalı görüntü
                region = image[i-1:i+2, j-1:j+2]
                min_val = np.min(region)
                max_val = np.max(region)
                if image[i, j] < min_val:
                    filtered_image[i, j] = min_val
                elif image[i, j] > max_val:
                    filtered_image[i, j] = max_val
            else:  # Renkli görüntü (BGR)
                for c in range(channels):
                    region = image[i-1:i+2, j-1:j+2, c]
                    min_val = np.min(region)
                    max_val = np.max(region)
                    if image[i, j, c] < min_val:
                        filtered_image[i, j, c] = min_val
                    elif image[i, j, c] > max_val:
                        filtered_image[i, j, c] = max_val

    return filtered_image

# Görüntüyü yükle
image = cv2.imread("peppers.png")

if image is None:
    print("Hata: Görüntü dosyası bulunamadı!")
    exit()

# Filtreyi uygula
smoothed_image = conservative_smoothing(image)

# Görüntüyü göster
plt.figure(figsize=(10,5))
plt.subplot(1,2,1), plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)), plt.title("Orijinal")
plt.subplot(1,2,2), plt.imshow(cv2.cvtColor(smoothed_image, cv2.COLOR_BGR2RGB)), plt.title("Konservatif Yumuşatma")
plt.show()
