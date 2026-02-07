from PIL import Image
import numpy as np

inputImage = Image.open("Lena.png")

# inputImage.show()

print(inputImage)
width, height = inputImage.size
print("Image Width", width)
print("Image Height", height)

pixel_val = list(inputImage.getdata())
# print(pixel_val)

pixels = np.array(inputImage.getdata()).reshape(width, height, 3)
# print(pixels)

# print("pixels at 0, 2", pixels[0, 2])
# print("pixel_val at 1", pixel_val[1])
coordinate = x, y = 1, 1
print(inputImage.getpixel(coordinate))

red_image = Image.fromarray(pixels[:, :, 0])
red_image.show()


im_gray = inputImage.convert('L')
im_gray.show()

im_cmyk = inputImage.convert("CMYK")
im_cmyk.show()

im_hsv = inputImage.convert("HSV")
im_hsv.show()
