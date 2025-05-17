import cv2
import numpy as np

# Seçilen noktaları saklayacak liste
selected_points = []

def select_points(event, x, y, flags, param):
    """ Fare tıklamalarını kaydeden fonksiyon """
    global selected_points
    if event == cv2.EVENT_LBUTTONDOWN:
        selected_points.append((x, y))
        print(f"Nokta Seçildi: {x}, {y}")

        if len(selected_points) == 4:
            cv2.destroyAllWindows()

# Görüntüyü yükle
image = cv2.imread("peppers.png")
cv2.imshow("Orijinal Görüntü - Noktalari Sec", image)

# Mouse callback fonksiyonunu bağla
cv2.setMouseCallback("Orijinal Görüntü - Noktalari Sec", select_points)

cv2.waitKey(0)
cv2.destroyAllWindows()

# Kullanıcının seçtiği noktaları numpy array'e çevir
pts1 = np.float32(selected_points)

# Düzeltme sonrası köşeleri belirle (örnek: 500x500 px)
width, height = 500, 500
pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

# Perspektif dönüşüm matrisini hesapla
matrix = cv2.getPerspectiveTransform(pts1, pts2)

# Perspektif dönüşümünü uygula
warped_image = cv2.warpPerspective(image, matrix, (width, height))

# Sonucu göster
cv2.imshow("Perspektif Düzeltilmiş Görüntü", warped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
