import numpy as np
import matplotlib.pyplot as plt

# STEP 1: Make a simple image (a white square on a black background)
img = np.zeros((200, 200))
img[60:140, 60:140] = 1.0

# STEP 2: Go to the frequency domain with the 2D Fourier transform 
F = np.fft.fft2(img)

# STEP 3: Make a grid of frequencies (kx = left-right, ky = up-down)
k = 2 * np.pi * np.fft.fftfreq(200)
KX, KY = np.meshgrid(k, k)

# STEP 4: DIFFERENTIATION = multiply by i*k  -> finds EDGES
gx = np.real(np.fft.ifft2(1j * KX * F))   # change left-right
gy = np.real(np.fft.ifft2(1j * KY * F))   # change up-down
edges = np.hypot(gx, gy)                  # combine both directions

# STEP 5: INTEGRATION (smoothing) = multiply by a low-pass filter -> BLUR
sigma = 3                                 # bigger number = more blur
lowpass = np.exp(-0.5 * sigma**2 * (KX**2 + KY**2))
blurred = np.real(np.fft.ifft2(lowpass * F))

# STEP 6: SHARPEN = blurred image minus its Laplacian (second derivative)
laplacian = np.real(np.fft.ifft2(-(KX**2 + KY**2) * np.fft.fft2(blurred)))
sharpened = blurred - 6 * laplacian

# STEP 7: Show all the results
images = [img, edges, blurred, sharpened]
titles = ["Original", "Edges (differentiation)",
          "Blurred (integration)", "Sharpened (differentiation)"]

for i in range(4):
    plt.subplot(1, 4, i + 1)
    plt.imshow(images[i], cmap="gray")
    plt.title(titles[i], fontsize=9)
    plt.axis("off")
plt.show()
