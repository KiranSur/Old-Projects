from PIL import Image
import numpy as np
 
im = Image.open('img/WithoutEdits.PNG')
im = im.convert('RGBA')
 
data = np.array(im)   # "data" is a height x width x 4 numpy array
red, green, blue, alpha = data.T # Temporarily unpack the bands for readability
 
# Replace white with red... (leaves alpha values alone...)
white_areas = ((red < (colors[0][0])*1.15)&(red > (colors[0][0])*.85)) & ((blue < (colors[0][0])*1.15)&(blue > (colors[0][0])*.85)) & ((green < (colors[0][0])*1.15)&(green > (colors[0][0])*.85))
data[..., :-1][white_areas.T] = (255, 0, 0) # Transpose back needed
 
im2 = Image.fromarray(data)
im2.show()
im2.save("changed.png")