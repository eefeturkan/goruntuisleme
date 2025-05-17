import cv2
import numpy as np
import matplotlib.pyplot as plt

def crimmins_speckle_removal(image):
    filtered_image = image.copy()
    shape = image.shape
    
    if len(shape) == 2:  # Gri tonlamalı görüntü
        rows, cols = shape
    else:  # Renkli görüntü
        rows, cols, _ = shape

    for i in range(1, rows-1):
        for j in range(1, cols-1):
            center_pixel = image[i, j]
            neighbors = [image[i-1, j], image[i+1, j], image[i, j-1], image[i, j+1]]
            avg_neighbors = np.mean(neighbors)

            if center_pixel > avg_neighbors + 20:
                filtered_image[i, j] = avg_neighbors
            elif center_pixel < avg_neighbors - 20:
                filtered_image[i, j] = avg_neighbors

    return filtered_image

# Görüntüyü yükle
image = cv2.imread("cameraman.jpg", cv2.IMREAD_GRAYSCALE)

if image is None:
    print("Hata: Görüntü dosyası bulunamadı!")
else:
    print("Görüntü başarıyla yüklendi.")

# Filtreyi uygula
denoised_image = crimmins_speckle_removal(image)

# Görüntüyü göster
plt.figure(figsize=(10,5))
plt.subplot(1,2,1), plt.imshow(image, cmap='gray'), plt.title("Orijinal")
plt.subplot(1,2,2), plt.imshow(denoised_image, cmap='gray'), plt.title("Crimmins Speckle Removal")
plt.show()
