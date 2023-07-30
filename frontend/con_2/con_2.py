import csv
import glob
import numpy as np
import pickle
import os
import time
import sys
import pathlib
import shutil
import subprocess
import datetime
import joblib
import time
import subprocess
import datetime
import pandas as pd
import serial
import cv2
import sqlite3
#import pandas as pd
import skimage
from skimage.color import rgb2gray
from featureExtraction import ShapeSizeFeature
#from featureExtraction import ColourFeatureExtract

com_port='COM4'
# img_path="D:\\APPLICATION\\Database\\images\\Con2\\"
img_path=r"C:\Users\USER\Desktop\images-old"
model_path="D:\\AI_Model\\BestClassifier.model"
excel_file_path = r'C:\Users\USER\Desktop\excel_files'




value_list=list()


for val in range(1,7):
    l=len(sys.argv[val])
    if l<4:
        zero='0'*(4-l)
        value_list.append(zero+sys.argv[val])
        print(zero+sys.argv[val])
    else:
        value_list.append(sys.argv[val])
        print(sys.argv[val])

c1_400=value_list[0]
c1_320=value_list[1]
c1_240=value_list[2]
c1_180=value_list[3]
c1_defect=value_list[4]
c1_error=value_list[5]
'''

#Con Speed = 29.99  Trigar Delay = 130000

c1_400='0010'
c1_320='0010'
c1_240='0010'
c1_180='0010'
c1_defect='0010' 
c1_error=0

'''
#Con Speed = 39.97  triger delay = 100000

##c1_400='1300'
##c1_320='1030'
##c1_240='0770'
##c1_180='0490'
##c1_defect='0220' 
##c1_error=0

#Con Speed = 49.96  triger delay = 100000
##c1_400='1050'
##c1_320='0800'
##c1_240='0610'
##c1_180='0380'
##c1_defect='0150' 
##c1_error=0

#to comminicate with arduino

# arduino = serial.Serial(port=com_port, baudrate=115200, timeout=1)

# arduino.write(bytes("99!", 'utf-8'))
# time.sleep(5)





########################################## Grading Code #######################################################
temp_count=5
filename=''
command=''
S,a,b=0,0,0

x=os.listdir(img_path)
if len(x)>0:
    for i in x:
        os.remove(img_path+"\\"+i)



#prediction and rejection
grade=[]
features_list = []
path = img_path
print("path=",path)
model = joblib.load(open(model_path,"rb"))
os.chdir(path)

# columns = ['Compactness', 'Roundness', 'SF3', 'Area', 'Centroid-0', 'Centroid-1', 'Eccentricity', 'Equivalent_diameter', 'Local_centroid-0', 'Local_centroid-1', 'Major_axis_length', 'Minor_axis_length', 'Orientation', 'Perimeter', 'Solidity', 'Grade']
# df = pd.DataFrame(columns=columns)


while True:
    grade=[]
    filelist = os.listdir(path)

    if not filelist:
        #print("\n\nwaiting for images")
        continue
    else:
        filename = os.path.join(path, filelist[0])
        # start_time = datetime.time().now()
        # end_time = datetime.datetime.now()
        # processing_time = end_time - start_time

        # print("Processing time:", processing_time.total_seconds(), "seconds")
        import timeit

        code_to_measure = '''
        # Your code here
        '''

        processing_time = timeit.timeit(code_to_measure, number=100)

        print("Processing time:", processing_time, "seconds")


        
        #print("\n\n",filename,"\n\n")
        
        I = cv2.imread(filename)


        

                   
        
        
        #print("type = ",type(I))
        
        try:
            
           

            Ig = rgb2gray(I)
            
            normIg = np.zeros(Ig.shape)
            Ig1=cv2.normalize(Ig,normIg, 0, 255, cv2.NORM_MINMAX)
            blur = cv2.GaussianBlur(np.uint8(Ig1), (15, 15), 0)
            ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            thresh=np.invert(thresh)
            number_of_white_pix = np.sum(thresh == 255)





            # print("white pixels = ",number_of_white_pix)
            # command = 'rm -f '+ filename
            # print("time for preprocessing = ",end1-start1," seconds")


            if number_of_white_pix<10000:
                #print("Blank")
                os.remove(filename)
                continue
            else:


                #print("Complete")
                S = ShapeSizeFeature(thresh)
                #print("size calculated")
                a = S['Compactness'][0]
                b = S['Roundness'][0]
                c = S['SF3'][0]
                d = S['area'][0]
                e = S['centroid-0'][0]
                f = S['centroid-1'][0]
                g = S['eccentricity'][0]
                h = S['equivalent_diameter'][0]
                i = S['local_centroid-0'][0]
                j = S['local_centroid-1'][0]
                k = S['major_axis_length'][0]
                l = S['minor_axis_length'][0]
                m = S['orientation'][0]
                n = S['perimeter'][0]
                o = S['solidity'][0]
            
               
                


                 





                #print('b : ',b)
                #print('d : ',d)

                if b<0.4:

                    if d>100000:
                        print("Blank")
                        os.remove(filename)
                        continue
                    if d>40000 and b>0.1:
                        print("Double")
                        os.remove(filename)
                        continue
                    else:
                        grade=[1000]
                        print("reject") 

                elif grade==[]:
                    print("pass", end=" --> ")
                    
                   
                    features = np.array([[a,b,c,d,e,f,g,h,i,j,k,l,m,n,o]])

                    # subprocess.run(["python", "main.py"])
                    
                    grade = model.predict(features)
                    print(grade[0])

                    
                    

                
                    # col_names = ['Compactness', 'Roundness', 'SF3', 'Area', 'Centroid-0', 'Centroid-1', 'Eccentricity', 'Equivalent_diameter', 'Local_centroid-0', 'Local_centroid-1', 'Major_axis_length', 'Minor_axis_length', 'Orientation', 'Perimeter', 'Solidity','grade']
                    # df = pd.DataFrame(columns=col_names)

                   
                    
                    

                    # for row in filename:

                    #     for col in  features:
                    #        df[row][col] = df.append(pd.Series(row, index=df.columns), ignore_index=True)

                    #     # write the DataFrame to an Excel file
                    # filepath = 'my_excel_file.xlsx'
                    # df.to_excel(filepath, index=False)



                    

                    
                    
                    
                    

                    

                    
                   

            
            st=''  
            if temp_count!=0:
                
##                c1_400='1050'
##                c1_320='0800'
##                c1_240='0610'
##                c1_180='0380'
##                c1_defect='0150' 
##                c1_error=0
 
                st="00"+c1_400+c1_320+c1_240+c1_180+c1_defect
                #st=c1_400+c1_320+c1_240+c1_180+c1_defect
                temp_count-=1
            #st+="11|"
            
            if grade[0] == 1000:
                st+='11|'
            elif grade[0] == 210 or grade[0] == 180:
                st+='12|'
            elif grade[0] == 240:
                st+='13|'
            elif grade[0] == 320:
                st+='14|'
            elif grade[0] == 400:
                st+='15|'
            else:
                st+='|'
            # arduino.write(bytes(st, 'utf-8'))

            os.remove(filename)
            #arduino_write(st)
            #print(st)
            #print('c_400 : ',counter_400,'	c_320 : ',counter_320,  '  c_240 : ',counter_240,'  c_180 : ',counter_180,'  c_reject : ',counter_reject,'  c_double : ',counter_double,'  c_blank : ',counter_blank)            
            
        except:
            #print("error occured")
            e = sys.exc_info()[0]
            #print("error = ",e)
        #finally:
            #os.remove(filename)










