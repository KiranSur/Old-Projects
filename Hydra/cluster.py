import cv2
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from PIL import Image

class DominantColors:

    CLUSTERS = None
    IMAGE = None
    COLORS = None
    LABELS = None
    
    def __init__(self, image, clusters=3):
        self.CLUSTERS = clusters
        self.IMAGE = image

    def dominantColors(self):
    
        img = cv2.imread(self.IMAGE)
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
        img = img.reshape((img.shape[0] * img.shape[1], 3))
        
        self.IMAGE = img
        
        kmeans = KMeans(n_clusters = self.CLUSTERS)
        kmeans.fit(img)
        
        self.COLORS = kmeans.cluster_centers_
        
        self.LABELS = kmeans.labels_
        
        return self.COLORS.astype(int)

# img = 'justgrass.png'
# clusters = 6

def change_image(username, orig, img, clusters):

    dc = DominantColors(img, clusters) 
    colors = dc.dominantColors()
    print(colors)   

    im = Image.open(img)
    im = im.convert('RGBA')
    
    data = np.array(im)   
    red, green, blue, alpha = data.T 


    color_high = 2
    color_low = .5
    print(colors[1])

    row_zero = 0

    temp = colors[0]

    for i in range(clusters):
        if(i!=0):
            j=i-1
            while(j>=0):
                print(i, j, colors[i][1], colors[j][1])
                if(colors[i][1]<colors[j][1]):
                    temp = colors[j].copy()
                    colors[j]=colors[i]
                    colors[i] = temp
                    i=j
                j=j-1

    print(colors)

    count = clusters-1

    color_list = ((220,20,60), (255,127,80), (173,255,47), (60,179,113), (0,206,209))

    while(count>0):
        white_areas = ((red < (colors[count][0])*color_high)&(red > (colors[count][0])*color_low)) & ((blue < (colors[count][1])*color_high)&(blue > (colors[count][1])*color_low)) & ((green < (colors[count][2])*color_high)&(green > (colors[count][2])*color_low))
        data[..., :-1][white_areas.T] = color_list[(clusters-count)-1]
        print(color_list[(clusters-count)-1])
        count = count-1

    im2 = Image.fromarray(data)
    # im2.show()

    new_filename = f'static/images/{username}_changed.png'

    im2.save(new_filename)


    #Overlay

    # creating a image object 
    im1 = Image.open(orig) 
    
    # copying image to another image object 
    first_image = im1.copy() 
    # first_image.show()
    second_image = Image.open(new_filename)
    # second_image.show()
    first_image.paste(second_image, (0,0), second_image)
    # first_image.show()
    first_image.save(new_filename)
