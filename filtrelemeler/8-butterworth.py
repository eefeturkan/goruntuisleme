import cv2
import numpy as np
import matplotlib.pyplot as plt

def butterworth_filter(shape, D0, n, highpass=False):
    rows, cols = shape
    mask = np.zeros((rows, cols), np.float32)
    center = (cols//2, rows//2)

    for u in range(rows):
        for v in range(cols):
            D = np.sqrt((u - center[1])**2 + (v - center[0])**2)
            H = 1 / (1 + (D/D0)**(2*n)) if not highpass else 1 - (1 / (1 + (D/D0)**(2*n)))
            mask[u, v] = H

    return mask

# Görüntüyü yükle
image = cv2.imread("peppers.png", cv2.IMREAD_GRAYSCALE)
f_transform = np.fft.fft2(image)
f_transform_shifted = np.fft.fftshift(f_transform)

# Butterworth alçak geçiren filtre uygula
blpf = butterworth_filter(image.shape, D0=30, n=2)
filtered_blpf = f_transform_shifted * blpf
filtered_image_blpf = np.fft.ifft2(np.fft.ifftshift(filtered_blpf)).real

# Butterworth yüksek geçiren filtre uygula
bhpf = butterworth_filter(image.shape, D0=30, n=2, highpass=True)
filtered_bhpf = f_transform_shifted * bhpf
filtered_image_bhpf = np.fft.ifft2(np.fft.ifftshift(filtered_bhpf)).real

# Görüntüleri göster
plt.figure(figsize=(12,6))
plt.subplot(1,3,1), plt.imshow(image, cmap='gray'), plt.title("Orijinal")
plt.subplot(1,3,2), plt.imshow(filtered_image_blpf, cmap='gray'), plt.title("Butterworth LPF")
plt.subplot(1,3,3), plt.imshow(filtered_image_bhpf, cmap='gray'), plt.title("Butterworth HPF")
plt.show()
