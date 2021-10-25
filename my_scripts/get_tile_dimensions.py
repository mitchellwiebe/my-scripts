# Written by Mitchell Wiebe - Oct 21st, 2021

# script to check the dimensions of all images in a dir

# run in terminal ''' python C:\Users\wiebe007\my_scripts\get_tile_dimensions.py '''

import os
from glob import glob
from PIL import Image
import statistics

# enter path to where the tiles exist
path = r'C:\Users\wiebe007\DeepPATH-master-Copy\TESTING\TEST_ALL\0.3125x\256px\Tiles'
tile_path = path + r'\*\*\*.jpeg'

# creates a list containing the path to all .jpeg tiles in the dir
tile_list = glob(tile_path)

# create list to hold x,y dims of each image
X = [];Y = []; numpixels = [];size = []

count = 0
for image in tile_list:
    im = Image.open(image)
    width, height = im.size
    X.append(width)
    Y.append(height)
    numpixels.append(width*height)
    size.append(im.size)
    
    
    count += 1
    if count % 1000 == 0:
        print('working...')
    if count % 10000 == 0:
        print('working really hard!')
        
        
        

Xindex = Y.index(min(Y))
minIndex = numpixels.index(min(numpixels))

print(count, ' total images')
print('Max Image size: ', max(size))
print('Thinnest images: ', min(size), ' and (', X[Xindex],',', min(Y), ')' )
print('Smallest image: (', X[minIndex],',', Y[minIndex],')')
print('Max pixel image: ', max(numpixels))
print('Min pixel image: ', min(numpixels))
print('Mean X: ', statistics.mean(X), ' Mean Y: ', statistics.mean(Y))
print('Std.Dev X: ', statistics.stdev(X), ' Std.Dev Y: ', statistics.stdev(Y) )