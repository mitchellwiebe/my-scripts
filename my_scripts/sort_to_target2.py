# Written by Mitchell Wiebe - July 19th, 2021 [edited Sept 22nd, 2021]

# script to organize training/validation/testing dataset to contain the same slides
# to run in command prompt: ''' python C:\Users\wiebe007\my_scripts\sort_to_target2.py '''

# the name Sort_to_target is used as we are sorting our datasets such that the WSI's in each of the 
# train/validation/test sets are the same as a target set

import os
from glob import glob

# ******** Required Input *********
# provide the path to the file that contains the training data that you want the new set to emulate
# in our case, this file contains 2 subfolders with the class labels [cancer, Solid_Tissue_Normal]

#target_dir = r'C:\\Users\wiebe007\DeepPATH-master-Copy\TESTING\TEST_ALL\2.5x_sorted_2class_512px'
target_dir = r'C:\Users\wiebe007\DeepPATH-master-Copy\TESTING\TEST_ALL\2.5x\299px\r1_sorted_2class'
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
#print(cancer_files_paths)

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
    cancer_tiles.append(item.split('_')[4])   #*** number may need to be changed depending on the path names
#print(cancer_tiles)
for item in normal_files_paths:
    normal_tiles.append(item.split('_')[6])   #*** number may need to be changed depending on the path names

#print(cancer_tiles)
#print(normal_tiles)
#checkpoint 1.

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

print('unique training slides: ',len(train_slides_unique))
print('unique validation slides: ',len(valid_slides_unique))
print('unique testing slides: ',len(test_slides_unique))

# take the unique entries for cancer/normal to determine how many unique slides of each
for item in cancer_tiles:
    if item not in cancer_slides_unique:
        cancer_slides_unique.append(item)
for item in normal_tiles:
    if item not in normal_slides_unique:
        normal_slides_unique.append(item)

print('cancer_slides_unique: ', len(cancer_slides_unique))
print('normal_slides_unique: ', len(normal_slides_unique))
#checkpoint 2.


# ******** Required Input *********
# From here, we now need to re-organize the current dataset such that the tiles from the same slides are contained
# 1. check if basename in current dataset is contained in the list 'train_slides_unique', 'valid_slides_unique', or 'test_slides_unique'
# 2. rename file prefix with either [train, valid, or test] 

#cancer_dir = r'C:\Users\wiebe007\DeepPATH-master-Copy\TESTING\TEST_ALL\Sorting_Same_Sets\cancer'
#normal_dir = r'C:\Users\wiebe007\DeepPATH-master-Copy\TESTING\TEST_ALL\Sorting_Same_Sets\Solid_Tissue_Normal'
cancer_dir = r'C:\Users\wiebe007\DeepPATH-master-Copy\TESTING\TEST_ALL\0.15625x\128px\Sorted\cancer'
normal_dir = r'C:\Users\wiebe007\DeepPATH-master-Copy\TESTING\TEST_ALL\0.15625x\128px\Sorted\Solid_Tissue_Normal'
#current_files = current_dir + r'\*\*'


# loop through the cancer/normal directory of our sorted tiles, determine where each tile belongs [train, valid, test] according to the target dataset
# rename the tile so that it belongs to this set


print('\nSorting cancer tiles in: ', cancer_dir)
cancer_train = 0
cancer_valid = 0
cancer_test = 0
renamed_count = 0
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
            if basenames[1] in train_slides_unique:
                cancer_train+=1
                #check if tile is already in training set
                if basenames[0] == 'train':
                    #print('Skipped!')
                    continue
                
                print('Tile belongs in training set')
                new_name = 'train_'+basenames[1]+'_'+basenames[2]+'_'+basenames[3]                 
                print('\nNew name: ', new_name)
                source = cancer_dir +'\\'+ tilename
                dest = cancer_dir +'\\'+new_name
                #print('\nSource: ', source)
                #print('\nDest: ', dest)
                os.rename(source,dest)
                print('Renamed!')
                renamed_count += 1
                
            elif basenames[1] in valid_slides_unique:
                cancer_valid+=1
                #check if tile is already in validation set
                if basenames[0] == 'valid':
                    #print('Skipped!')
                    continue
                    
                print('Tile belongs in validation set')
                new_name = 'valid_'+basenames[1]+'_'+basenames[2]+'_'+basenames[3]                 
                print('New name: ', new_name)
                source = cancer_dir +'\\'+ tilename
                dest = cancer_dir +'\\'+new_name
                #print('\nSource: ', source)
                #print('\nDest: ', dest)
                os.rename(source,dest)
                print('Renamed!')
                renamed_count += 1
                
            else:
                cancer_test+=1
                #check if tile is already in test set
                if basenames[0] == 'test':
                    #print('Skipped!')
                    continue
                    
                print('Tile belongs in testing set')
                new_name = 'test_'+basenames[1]+'_'+basenames[2]+'_'+basenames[3]                 
                print('New name: ', new_name)
                source = cancer_dir +'\\'+ tilename
                dest = cancer_dir +'\\'+new_name
                #print('\nSource: ', source)
                #print('\nDest: ', dest)
                os.rename(source,dest)
                print('Renamed!')
                renamed_count += 1




print('\nSorting normal tiles in: ', normal_dir)
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
            if basenames[1] in train_slides_unique:
                normal_train+=1
                #check if tile is already in training set
                if basenames[0] == 'train':
                    #print('Skipped!')
                    continue
                
                print('Tile belongs in training set')
                new_name = 'train_'+basenames[1]+'_'+basenames[2]+'_'+basenames[3]                 
                print('\nNew name: ', new_name)
                source = normal_dir +'\\'+ tilename
                dest = normal_dir +'\\'+new_name
                #print('\nSource: ', source)
                #print('\nDest: ', dest)
                os.rename(source,dest)
                print('Renamed!')
                renamed_count += 1
                
            elif basenames[1] in valid_slides_unique:
                normal_valid+=1
                #check if tile is already in validation set
                if basenames[0] == 'valid':
                    #print('Skipped!')
                    continue
                    
                print('Tile belongs in validation set')
                new_name = 'valid_'+basenames[1]+'_'+basenames[2]+'_'+basenames[3]                 
                print('New name: ', new_name)
                source = normal_dir +'\\'+ tilename
                dest = normal_dir +'\\'+new_name
                #print('\nSource: ', source)
                #print('\nDest: ', dest)
                os.rename(source,dest)
                print('Renamed!')
                renamed_count += 1
                
            else:
                normal_test+=1
                #check if tile is already in test set
                if basenames[0] == 'test':
                    #print('Skipped!')
                    continue
                    
                print('Tile belongs in testing set')
                new_name = 'test_'+basenames[1]+'_'+basenames[2]+'_'+basenames[3]                 
                print('New name: ', new_name)
                source = normal_dir +'\\'+ tilename
                dest = normal_dir +'\\'+new_name
                #print('\nSource: ', source)
                #print('\nDest: ', dest)
                os.rename(source,dest)
                print('Renamed!')
                renamed_count += 1
                
               
print('\nDone sorting!\n')
print(str(renamed_count), ' tiles renamed') 

print('Cancer test tiles:', cancer_test)  
print('Cancer valid tiles:', cancer_valid)
print('Cancer train tiles:', cancer_train)  
print('Total Cancer tiles: ', cancer_test+cancer_valid+cancer_train)
#print('Total Cancer slides: ', len(cancer_slides_unique))

print('\nNormal test tiles:', normal_test)  
print('Normal valid tiles:', normal_valid)
print('Normal train tiles:', normal_train)   
print('Total Normal tiles: ', normal_test+normal_valid+normal_train)
#print('Total Normal slides: ', len(normal_slides_unique))

print('\nPercent cancer test: ', cancer_test/(cancer_test+cancer_valid+cancer_train))  
print('Percent cancer valid: ', cancer_valid/(cancer_test+cancer_valid+cancer_train))  
print('Percent cancer train: ', cancer_train/(cancer_test+cancer_valid+cancer_train))  
 
print('\nPercent normal test: ', normal_test/(normal_test+normal_valid+normal_train))  
print('Percent normal valid: ', normal_valid/(normal_test+normal_valid+normal_train))  
print('Percent normal train: ', normal_train/(normal_test+normal_valid+normal_train))

#print('\nTotal test slides: ', len(test_slides_unique))  
#print('Total validation slides: ', len(valid_slides_unique))
#print('Total train slides: ', len(train_slides_unique))

#checkpoint 3.

# All this below is just to confirm the number of slides in each of the following categories
# train, valid, test, cancer, & normal
print('___________________')
current_dir = cancer_dir.split('cancer')[0]
path_to_current_train_file = current_dir + r'\*\train_*'
path_to_current_valid_file = current_dir + r'\*\valid_*'
path_to_current_test_file = current_dir + r'\*\test_*'
# we will use these variables just to count how many slides we have of cancer/normal
path_to_current_cancer_file = current_dir + r'\cancer\*'
path_to_current_normal_file = current_dir + r'\Solid_Tissue_Normal\*'

# creates a list of the paths to all train/test/valid tiles
train_current_paths = glob(path_to_current_train_file)
valid_current_paths = glob(path_to_current_valid_file)
test_current_paths = glob(path_to_current_test_file)
cancer_current_paths = glob(path_to_current_cancer_file)
normal_current_paths = glob(path_to_current_normal_file)

currenttrain_tiles = []
currentvalid_tiles = []
currenttest_tiles = []
currentcancer_tiles = []
currentnormal_tiles = []

# take just the portion of the name following 'train_' and put it in a list
for item in train_current_paths:
    currenttrain_tiles.append(item.split('train_')[1])
# take just the portion of the name following 'valid_' and put it in a list
for item in valid_current_paths:
    currentvalid_tiles.append(item.split('valid_')[1])
# take just the portion of the name following 'test_' and put it in a list
for item in test_current_paths:
    currenttest_tiles.append(item.split('test_')[1])

# take the portion of the name that contains just 'TCGA-...' 
# note that we are not taking the porting that says something like '_4_3.jpeg'
for item in cancer_current_paths:    
    currentcancer_tiles.append(item.split('_')[3])   #*** number may need to be changed depending on the path names
for item in normal_current_paths:
    currentnormal_tiles.append(item.split('_')[5])   #*** number may need to be changed depending on the path names

#print(currentcancer_tiles)
#print(currentnormal_tiles)
#checkpoint 4.

# cut off the portion of the name that contains something like '_2_3.jpeg'
for i in range(len(currenttrain_tiles)):
    currenttrain_tiles[i] = currenttrain_tiles[i].split('_',1)[0]
for i in range(len(currentvalid_tiles)):
    currentvalid_tiles[i] = currentvalid_tiles[i].split('_',1)[0]
for i in range(len(currenttest_tiles)):
    currenttest_tiles[i] = currenttest_tiles[i].split('_',1)[0]

# now take just the unique entries to get a list of the unique slides within the sets
currenttrain_slides_unique = []
currentvalid_slides_unique = []
currenttest_slides_unique = []
currentcancer_slides_unique = []
currentnormal_slides_unique = []

for item in currenttrain_tiles:
    if item not in currenttrain_slides_unique:
        currenttrain_slides_unique.append(item)
for item in currentvalid_tiles:
    if item not in currentvalid_slides_unique:
        currentvalid_slides_unique.append(item)
for item in currenttest_tiles:
    if item not in currenttest_slides_unique:
        currenttest_slides_unique.append(item)

print('current unique training slides: ',len(currenttrain_slides_unique))
print('current unique validation slides: ',len(currentvalid_slides_unique))
print('current unique testing slides: ',len(currenttest_slides_unique))

# take the unique entries for cancer/normal to determine how many unique slides of each
for item in currentcancer_tiles:
    if item not in currentcancer_slides_unique:
        currentcancer_slides_unique.append(item)
for item in currentnormal_tiles:
    if item not in currentnormal_slides_unique:
        currentnormal_slides_unique.append(item)

print('currentcancer_slides_unique: ', len(currentcancer_slides_unique))
print('currentnormal_slides_unique: ', len(currentnormal_slides_unique))
  