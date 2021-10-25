# Written by Mitchell Wiebe - July 19th, 2021

# script to organize training/validation/testing dataset to contain the same slides
# to run in command prompt: ''' python C:\Users\wiebe007\Check_same_testsets.py '''

# the name Sort_to_target is used as we are sorting our datasets such that the WSI's in each of the 
# train/validation/test sets are the same as a target set

import os
from glob import glob

# ******** Required Input *********
# provide the path to the file that contains the training data that you want the new set to emulate
# in our case, this file contains 2 subfolders with the class labels [cancer, Solid_Tissue_Normal]
target_dir = r'C:\\Users\wiebe007\DeepPATH-master-Copy\TESTING\TEST_ALL\2.5x_sorted_2class_512px'
print('Looking in: ', target_dir)

path_to_target_train_file = target_dir + r'\*\train_*'
path_to_target_valid_file = target_dir + r'\*\valid_*'
path_to_target_test_file = target_dir + r'\*\test_*'
#path_to_target_train_file = r'C:\\Users\wiebe007\DeepPATH-master-Copy\TESTING\TEST_ALL\2.5x_sorted_2class_512px\*\train_*'
#path_to_target_valid_file = r'C:\\Users\wiebe007\DeepPATH-master-Copy\TESTING\TEST_ALL\2.5x_sorted_2class_512px\*\valid_*'
#path_to_target_test_file = r'C:\\Users\wiebe007\DeepPATH-master-Copy\TESTING\TEST_ALL\2.5x_sorted_2class_512px\*\test_*'

# we will use these variables just to count how many slides we have of cancer/normal
path_to_target_cancer_file = target_dir + r'\cancer\*'
path_to_target_normal_file = target_dir + r'\Solid_Tissue_Normal\*'

# creates a list of the paths to all train/test/valid tiles
train_files_paths = glob(path_to_target_train_file)
valid_files_paths = glob(path_to_target_valid_file)
test_files_paths = glob(path_to_target_test_file)
#print('Paths to all training tiles: ', train_files_paths)
cancer_files_paths = glob(path_to_target_cancer_file)
normal_files_paths = glob(path_to_target_normal_file)

train_tiles = []
valid_tiles = []
test_tiles = []
cancer_tiles = []
normal_tiles = []

# take just the portion of the name following 'train_' and put it in a list
for item in train_files_paths:
    train_tiles.append(item.split('train_')[1])
# take just the portion of the name following 'valid_' and put it in a list

for item in valid_files_paths:
    valid_tiles.append(item.split('valid_')[1])
    
# take just the portion of the name following 'test_' and put it in a list
for item in test_files_paths:
    test_tiles.append(item.split('test_')[1])

# take the portion of the name that contains just 'TCGA-...' 
# note that we are not taking the porting that says something like '_4_3.jpeg'
for item in cancer_files_paths:    
    cancer_tiles.append(item.split('_')[5])   
    
for item in normal_files_paths:
    normal_tiles.append(item.split('_')[7])

#print(cancer_tiles)
#print(normal_tiles)

# cut off the portion of the name that contains something like '_2_3.jpeg'
for i in range(len(train_tiles)):
    train_tiles[i] = train_tiles[i].split('_',1)[0]
for i in range(len(valid_tiles)):
    valid_tiles[i] = valid_tiles[i].split('_',1)[0]
for i in range(len(test_tiles)):
    test_tiles[i] = test_tiles[i].split('_',1)[0]

# now take just the unique entries to get a list of the unique slides within the sets
train_slides_unique = []
valid_slides_unique = []
test_slides_unique = []
cancer_slides_unique = []
normal_slides_unique = []

for item in train_tiles:
    if item not in train_slides_unique:
        train_slides_unique.append(item)
for item in valid_tiles:
    if item not in valid_slides_unique:
        valid_slides_unique.append(item)
for item in test_tiles:
    if item not in test_slides_unique:
        test_slides_unique.append(item)

print(len(train_slides_unique), 'unique slides found in training dataset')
print(len(valid_slides_unique), 'unique slides found in validation dataset')
print(len(test_slides_unique), 'unique slides found in testing dataset')

# take the unique entries for cancer/normal to determine how many unique slides of each
for item in cancer_tiles:
    if item not in cancer_slides_unique:
        cancer_slides_unique.append(item)
for item in normal_tiles:
    if item not in normal_slides_unique:
        normal_slides_unique.append(item)

#print(cancer_slides_unique)

# ******** Required Input *********
# From here, we now need to re-organize the current dataset such that the tiles from the same slides are contained
# 1. check if basename in current dataset is contained in the list 'train_slides_unique', 'valid_slides_unique', or 'test_slides_unique'
# 2. rename file prefix with either [train, valid, or test] 

cancer_dir = r'C:\Users\wiebe007\DeepPATH-master-Copy\TESTING\TEST_ALL\r1_sorted_2class\cancer'
normal_dir = r'C:\Users\wiebe007\DeepPATH-master-Copy\TESTING\TEST_ALL\r1_sorted_2class\Solid_Tissue_Normal'
#current_files = current_dir + r'\*\*'


# loop through the cancer/normal directory of our sorted tiles, determine where each tile belongs [train, valid, test] according to the target dataset
# rename the tile so that it belongs to this set


#print('\nSorting cancer tiles in: ', cancer_dir)
cancer_train = 0
cancer_valid = 0
cancer_test = 0
# starting with the directory that contains all our cancer tiles
for block in os.walk(cancer_dir): 
    #print(block)
    for file in block:
        #print(file)       
        for tilename in file:
            #print(tilename)
            
            # this if statement is just to handle the fact that the path name gets passed as a part of things
            if len(tilename) == 1:
                continue
            basenames = tilename.split('_')
            
            #print(basenames)
            # just look at a single slide for now
            #if tilename == r'train_TCGA-O2-A52V-01A-03-TSC.BA28F714-8AEE-47B6-8442-E990357446CB_4_2.jpeg':
                #print('Example: ', basenames)
                
            # check which set tile belongs to and rename it appropriately
            if basenames[1] in test_slides_unique and basenames[0]=='test':
                cancer_test+=1
                #check if tile is already in training set
                #if basenames[0] == 'train':
                    #print('Skipped!')
                 #   continue
                
                #print('Tile belongs in test set')
                new_name = basenames[0]+'_'+basenames[1]+'_'+basenames[2]+'_'+basenames[3]                 
                print('\nMatching cancer slide name: ', new_name)
                



#print('\nSorting normal tiles in: ', normal_dir)
normal_train = 0
normal_valid = 0
normal_test = 0
# now for the directory that contains all our normal tiles
for block in os.walk(normal_dir): 
    #print(block)
    for file in block:
        #print(file)       
        for tilename in file:
            #print(tilename)
            
            # this if statement is just to handle the fact that the path name gets passed as a part of things
            if len(tilename) == 1:
                continue
            basenames = tilename.split('_')
            
            #print(basenames)
            # just look at a single slide for now
            #if tilename == r'train_TCGA-O2-A52V-01A-03-TSC.BA28F714-8AEE-47B6-8442-E990357446CB_4_2.jpeg':
                #print('Example: ', basenames)
                
            # check which set tile belongs to and rename it appropriately
            if basenames[1] in test_slides_unique and basenames[0]=='test':
                normal_train+=1
                #check if tile is already in training set
                #if basenames[0] == 'train':
                    #print('Skipped!')
                 #   continue
                
                #print('Tile belongs in training set')
                new_name = basenames[0]+'_'+basenames[1]+'_'+basenames[2]+'_'+basenames[3]                 
                print('\nMatching normal slide name: ', new_name)
                
  