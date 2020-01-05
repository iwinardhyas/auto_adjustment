import os
import shutil

path = '/home/erwin/Desktop/tes'
path_out = '/home/erwin/Desktop/tes_pindah'

try:
    if not os.path.exists(path_out):
        os.makedirs(path_out)
except OSError:
    print ('Error: Creating directory. ' + path_out)  

for folder in os.listdir(path):
    folder_path = path +'/'+ folder
    try:
        if not os.path.exists(path_out+'/'+folder):
            os.makedirs(path_out+'/'+folder)
    except OSError:
        print ('Error: Creating directory. ' + path_out+'/'+folder)
    counter = 0
    for file_jpg in os.listdir(folder_path):
        folder_path_file = folder_path +'/'+file_jpg
        # shutil.copyfile(folder_path_file,path_out+'/'+folder+'/'+file_jpg) #for copy
        shutil.move(folder_path_file,path_out+'/'+folder+'/'+file_jpg) #for cut
        print(folder_path_file)
        counter += 1
        if counter == 10:
            break