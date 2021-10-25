# Mitch W. - Aug. 11 2021

# Convert rgb pathology tiles to black/white for training
# ----- indicates code areas that may need to be updated depending on where the files are located
# python C:\\Users\wiebe007\convert_rgb2bw.py

import os
from os import mkdir
from glob import glob
from PIL import Image

# ----- path to rgb pathology files 
file_path = r'C:\\Users\wiebe007\DeepPATH-master-Copy\TESTING\TEST_ALL\2.5x\Tiles\images\299px_Tiled'

# to get to actual tiles
tile_path = file_path + '\*\*\*'

# ----- output folder
output_path = file_path + '_BW'

# access the images in the tile_path
tilecount = 0
for image in glob(tile_path):
    tilecount+=1
    
    basename = 'TCGA' + image.split('TCGA')[1]
    #print(len(basename.split('2.5')))
    
    # looks a bit dumb but it handles the issue of a '2.5' occuring somewhere else in the name
    if len(basename.split('2.5')) >= 3:
        #print('problem')
        out_dir = basename.split('2.5')[0] + '2.5' + basename.split('2.5')[1]          # -----
        jpeg_name = basename.split('2.5')[2]            # -----
    else:
        #print('good')
        out_dir = basename.split('2.5')[0]              # -----
        jpeg_name = basename.split('2.5')[1]            # -----
        
    #print('B '+ basename)
    #print('O ' + out_dir)
    #print('J ' + jpeg_name)
        
    filedir1 = output_path + '\\' + out_dir
    filedir2 = filedir1 + '\\2.5'                   # -----
    
    # check if dir's already exist, if not, make them
    try:
        mkdir(filedir1)
    except:
        pass
    try:
        mkdir(filedir2)
    except:
        pass
    
    
    # opens the image file, converts it to bw and saves it 
    tile = Image.open(image)
    tile_BW = tile.convert('L')
    tile_BW.save(filedir2 + jpeg_name)
    
    
    #print(basename)
    #print(out_dir)
    #print('Save as: ' + filedir2 + jpeg_name)
    #if tilecount == 4:
     #   break
    
print(tilecount, ' tiles converted to BW')