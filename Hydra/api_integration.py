from picterra import APIClient
import picterra
import skimage.draw as skdraw
import numpy as np
import pylab as pl
from skimage import io
from PIL import Image

def api_call(username, filler):

    #Places that say filler are where you put the original image and input files
    #This first part is to connect with the API client and generate a raster id for the picture

    client = APIClient(api_key='d5c4771b812979b65262606e2fb0786d58449e897b60921f06900b0067716e36')
    raster_id = client.upload_raster(filler, name='FILLER')

    #This is the premade detector ID for our Picterra detector

    detector_id = '98e6510d-d268-4c72-a54f-39cf73fee473'

    #This is the ID for the resultant file that has already been detected on
    result_id = client.run_detector(detector_id, raster_id)
    client.download_result_to_file(result_id, 'FILLER.geojson') #<--Make sure to leave the .geojson extension of the result file even if the input image is a PNG
    #The FILLER part here is just whatever name you want to give the file

    #This is to turn the geojson file into a polygon to make the detection areas more accessible
    polygons = picterra.nongeo_result_to_pixel('FILLER.geojson')

    ogFILE = io.imread(filler) #Read in the original without edits file here

    #This is to transfer the detection areas from the polygons onto the ogFILE
    for polygon in polygons:
        outer_ring = polygon[0]
        # Only outer ring
        p = np.array(outer_ring)
        rr, cc = skdraw.polygon(p[:, 1], p[:, 0])
        ogFILE[rr, cc] = 0

    #This is to convert the detected ogFILE into an Image file type
    ogDET = Image.fromarray(ogFILE)
    # ogDET.show() 

    justgrass = Image.open(filler) #Read in the original without edits file here
    # justgrass.show()

    width, height = ogDET.size
    for x in range(width):
        for y in range(height):
            r,g,b,a = ogDET.getpixel((x,y))
            # if (a != 3):
            if (a != 0):
                justgrass.putpixel((x,y), (0, 0, 0, 0))

    #The justgrass file is now just an Image file with just the grass and everything else having an alpha value of 0

    # justgrass.show()

    new_filename = f'static/images/{username}_justgrass.png'

    justgrass.save(new_filename)


