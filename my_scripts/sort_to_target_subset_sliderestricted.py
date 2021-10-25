# Written by Mitchell Wiebe - [edited Sept 27th, 2021]

# script to generate a subset of training tiles with equal number of images to another 'target' set
# ie: there will be equal tiles of cancer and normal tiles 
# *** BUT *** 
# we will restric the tiles to come from within the same slides that are available at the low resolution
# to run in command prompt: ''' python C:\Users\wiebe007\my_scripts\sort_to_target_subset_sliderestricted.py '''


import os
from glob import glob
import random

# ******** Required Input *********
# provide the path to the file that contains the training data that you want the new set to emulate
# in our case, this file contains 2 subfolders with the class labels [cancer, Solid_Tissue_Normal]

#target_dir = r'dir_with_less_slides\sorted'
# Here, the 0.312x dir contains many less slides than the 2.5x dir. We will have to skip some slides
target_dir = r'C:\Users\wiebe007\DeepPATH-master-Copy\TESTING\TEST_ALL\0.3125x\512px\Tiles_Sorted'
current_dir = r'C:\Users\wiebe007\DeepPATH-master-Copy\TESTING\TEST_ALL\2.5x\299px\r1_sorted_2class'
new_dir = r'C:\Users\wiebe007\DeepPATH-master-Copy\TESTING\TEST_ALL\2.5x\299px\Subset_testing_slide_restricted'
#os.mkdir(new_dir)
print('Looking in: ', target_dir)

# we will use these variables just to count how many slides we have of cancer/normal
path_to_target_cancer_file = target_dir + r'\cancer\*'
path_to_target_normal_file = target_dir + r'\Solid_Tissue_Normal\*'
path_to_current_cancer_file = current_dir + r'\cancer\*'
path_to_current_normal_file = current_dir + r'\Solid_Tissue_Normal\*'

cancer_files_paths = glob(path_to_target_cancer_file)
normal_files_paths = glob(path_to_target_normal_file)
current_cancer_paths = glob(path_to_current_cancer_file)
current_normal_paths = glob(path_to_current_normal_file)

num_images = 0
for item in cancer_files_paths:
    if '.jpeg' in item:
        num_images += 1
for item in normal_files_paths:
    if '.jpeg' in item:
        num_images += 1
print(num_images, ' total images found')

cancer_train_tiles = [];normal_train_tiles = []
cancer_valid_tiles = [];normal_valid_tiles = []
cancer_test_tiles = []; normal_test_tiles = []
cancer_tiles = [];normal_tiles = []

for item in cancer_files_paths:   
    if 'train' in item:
        cancer_train_tiles.append(item.split('train_')[1])
    if 'valid' in item:
        cancer_valid_tiles.append(item.split('valid_')[1])
    if 'test' in item:
        cancer_test_tiles.append(item.split('test_')[1])
    cancer_tiles.append(item.split('_')[3])   #*** number may need to be changed depending on the path names
    
for item in normal_files_paths:
    if 'train' in item:
        normal_train_tiles.append(item.split('train_')[1])
    if 'valid' in item:
        normal_valid_tiles.append(item.split('valid_')[1])
    if 'test' in item:
        normal_test_tiles.append(item.split('test_')[1])
    normal_tiles.append(item.split('_')[5])   #*** number may need to be changed depending on the path names

print('\n--Tiles--\ncancer_train:', len(cancer_train_tiles), 'cancer_valid:', len(cancer_valid_tiles),
    'cancer_test:', len(cancer_test_tiles), '\tcancer_total:', len(cancer_tiles))
print('normal_train:', len(normal_train_tiles), 'normal_valid:', len(normal_valid_tiles),
    'normal_test:', len(normal_test_tiles), '\tnormal_total:', len(normal_tiles))
#print(cancer_tiles)
#print(normal_tiles)
#checkpoint 1.


# now take just the unique entries to get a list of the unique slides within the sets
cancer_train_slides_unique = []; normal_train_slides_unique = []
cancer_valid_slides_unique = []; normal_valid_slides_unique = []
cancer_test_slides_unique = []; normal_test_slides_unique = []
cancer_slides_unique = [];normal_slides_unique = []

# cut off the portion of the name that contains something like '_2_3.jpeg'
for i in range(len(cancer_train_tiles)):
    cancer_train_tiles[i] = cancer_train_tiles[i].split('_',1)[0]
for i in range(len(cancer_valid_tiles)):
    cancer_valid_tiles[i] = cancer_valid_tiles[i].split('_',1)[0]
for i in range(len(cancer_test_tiles)):
    cancer_test_tiles[i] = cancer_test_tiles[i].split('_',1)[0]
for i in range(len(normal_train_tiles)):
    normal_train_tiles[i] = normal_train_tiles[i].split('_',1)[0]
for i in range(len(normal_valid_tiles)):
    normal_valid_tiles[i] = normal_valid_tiles[i].split('_',1)[0]
for i in range(len(normal_test_tiles)):
    normal_test_tiles[i] = normal_test_tiles[i].split('_',1)[0]

for item in cancer_train_tiles:
    if item not in cancer_train_slides_unique:
        cancer_train_slides_unique.append(item)
for item in cancer_valid_tiles:
    if item not in cancer_valid_slides_unique:
        cancer_valid_slides_unique.append(item)
for item in cancer_test_tiles:
    if item not in cancer_test_slides_unique:
        cancer_test_slides_unique.append(item)
for item in normal_train_tiles:
    if item not in normal_train_slides_unique:
        normal_train_slides_unique.append(item)
for item in normal_valid_tiles:
    if item not in normal_valid_slides_unique:
        normal_valid_slides_unique.append(item)
for item in normal_test_tiles:
    if item not in normal_test_slides_unique:
        normal_test_slides_unique.append(item)
        
# take the unique entries for cancer/normal to determine how many unique slides of each
for item in cancer_tiles:
    if item not in cancer_slides_unique:
        cancer_slides_unique.append(item)
for item in normal_tiles:
    if item not in normal_slides_unique:
        normal_slides_unique.append(item)

print('\n--Slides--\ncancer_train:', len(cancer_train_slides_unique), 'cancer_valid:', len(cancer_valid_slides_unique),
    'cancer_test:', len(cancer_test_slides_unique), '\tcancer_total:', len(cancer_slides_unique))
print('normal_train:', len(normal_train_slides_unique), 'normal_valid:', len(normal_valid_slides_unique),
    'normal_test:', len(normal_test_slides_unique), '\tnormal_total:', len(normal_slides_unique))
#checkpoint 2.


#---------------------------- Now for the tricky part
# We need to choose a subset of our current dataset, such that:
# - total number of images equal to len(cancer_train_tiles) + len(normal_train_tiles)
# - the images are only coming from tiles listed in cancer_slides_unique or normal_slides_unique
tiles_needed = len(cancer_train_tiles) + len(normal_train_tiles)
print('\nSubset of ', tiles_needed, ' from ', current_dir)

# Makes a list of ALL available tiles that we can pull a subset from
cancer_tiles_available = []; normal_tiles_available = [];
for item in current_cancer_paths:   
    if 'train' in item:
        slide_name = item.split('train_')[1]
        slide_name = slide_name.split('_')[0]
        if slide_name in cancer_train_slides_unique:
            cancer_tiles_available.append(item.split('train_')[1])
for item in current_normal_paths:  
    if 'train' in item:
        slide_name = item.split('train_')[1]
        slide_name = slide_name.split('_')[0]
        if slide_name in normal_train_slides_unique:
            normal_tiles_available.append(item.split('train_')[1])
#print(len(normal_slides_unique), len(normal_tiles_available))

print(r'Sampling from ', len(cancer_tiles_available), r' cancer tiles & ' , len(normal_tiles_available), r' normal tiles')
         
# lists that will hold the names of tiles that make up our training subsets
cancer_tiles_subset = []; normal_tiles_subset = []

# random number lists that will be used to index random samples without duplicates
# should be of length equal to the target training set but of values equal to the available tiles list
cancer_random = random.sample(range(int(len(cancer_tiles_available))),len(cancer_train_tiles))
normal_random = random.sample(range(int(len(normal_tiles_available))),len(normal_train_tiles))
#print(normal_random)

# index the available tiles list using the random values, then pull that value and place it into the subset
for i in range(0,len(cancer_train_tiles)):
    cancer_tiles_subset.append(cancer_tiles_available[int(cancer_random[i])])
for i in range(0,len(normal_train_tiles)):
    normal_tiles_subset.append(normal_tiles_available[int(normal_random[i])])
#print(normal_tiles_subset, len(normal_tiles_subset))
 
 
 
#------------------------- Now we just need to put the subsets into another folder!

# ** Note ** 
# Make sure that you are writing these files to empty directories. Otherwise the will 'pile-up'
os.mkdir(new_dir + '\cancer')
os.mkdir(new_dir + '\Solid_Tissue_Normal')

for item in cancer_tiles_subset:
    source = current_dir + r'\cancer\train_' + item
    dest = new_dir + r'\cancer\train_' + item 
    os.symlink(source,dest)
for item in normal_tiles_subset:
    source = current_dir + r'\Solid_Tissue_Normal\train_' + item
    dest = new_dir + r'\Solid_Tissue_Normal\train_' + item 
    os.symlink(source,dest)
    
    
    
