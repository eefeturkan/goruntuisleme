import cv2
import numpy as np
import matplotlib.pyplot as plt

def gaussian_filter(shape, D0, highpass=False):
    rows, cols = shape
    mask = np.zeros((rows, cols), np.float32)
    center = (cols//2, rows//2)

    for u in range(rows):
        for v in range(cols):
            D = np.sqrt((u - center[1])**2 + (v - center[0])**2)
            H = np.exp(-(D**2) / (2 * (D0**2))) if not highpass else 1 - np.exp(-(D**2) / (2 * (D0**2)))
            mask[u, v] = H

    return mask

image = cv2.imread("peppers.png", cv2.IMREAD_GRAYSCALE)
f_transform = np.fft.fft2(image)
f_transform_shifted = np.fft.fftshift(f_transform)

# Gaussian LPF
glpf = gaussian_filter(image.shape, D0=30)
filtered_glpf = f_transform_shifted * glpf
filtered_image_glpf = np.fft.ifft2(np.fft.ifftshift(filtered_glpf)).real

# Gaussian HPF
ghpf = gaussian_filter(image.shape, D0=30, highpass=True)
filtered_ghpf = f_transform_shifted * ghpf
filtered_image_ghpf = np.fft.ifft2(np.fft.ifftshift(filtered_ghpf)).real

# Görüntüleri göster
plt.figure(figsize=(12,6))
plt.subplot(1,3,1), plt.imshow(image, cmap='gray'), plt.title("Orijinal")
plt.subplot(1,3,2), plt.imshow(filtered_image_glpf, cmap='gray'), plt.title("Gaussian LPF")
plt.subplot(1,3,3), plt.imshow(filtered_image_ghpf, cmap='gray'), plt.title("Gaussian HPF")
plt.show()
