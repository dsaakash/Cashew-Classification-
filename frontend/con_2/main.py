import pandas as pd
import os
import cv2
from featureExtraction import ShapeSizeFeature
from skimage.color import rgb2gray
import numpy as np
from pathlib import Path

# Define the feature extraction function
def extract_features(image_path):
    I = cv2.imread(image_path)
    Ig = rgb2gray(I)     
    normIg = np.zeros(Ig.shape)
    Ig1=cv2.normalize(Ig,normIg, 0, 255, cv2.NORM_MINMAX)
    blur = cv2.GaussianBlur(np.uint8(Ig1), (15, 15), 0)
    ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    thresh=np.invert(thresh)
    number_of_white_pix = np.sum(thresh == 255)

    S = ShapeSizeFeature(thresh)
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
                   
    features = np.array([[a,b,c,d,e,f,g,h,i,j,k,l,m,n,o]])
    return features

# Define the directory containing the images
image_dir = Path(r'C:\Users\USER\Desktop\images-old')
image_path = image_dir

# Create a new Excel file
excel_file = 'image_features.xlsx'
writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')

# Define the columns for the dataframe
columns = ['Image Name', 'Compactness', 'Roundness', 'SF3', 'Area', 'Centroid-0', 'Centroid-1', 'Eccentricity', 'Equivalent_diameter', 'Local_centroid-0', 'Local_centroid-1', 'Major_axis_length', 'Minor_axis_length', 'Orientation', 'Perimeter', 'Solidity']

# Create an empty list to store the dataframes for each image
dfs = []

# Loop over the images and extract their features
for filename in os.listdir(image_dir):
    if filename.endswith('.bmp') or filename.endswith('.jpg') or filename.endswith('.png'):
        # Construct the image path
        image_path = os.path.join(image_dir, filename)
        
        # Extract the features for the current image
        features = extract_features(image_path)
        
        # Construct a new row with the image name and its features
        row = [filename] + features.tolist()[0]
        
        # Create a new dataframe with the row data
        df = pd.DataFrame([row], columns=columns)
        
        # Add the dataframe to the list of dataframes
        dfs.append(df)
        
        
# Concatenate all dataframes into a single one
df = pd.concat(dfs, ignore_index=True)

# Write the dataframe to an Excel file
df.to_excel(writer, sheet_name='Sheet1', index=False)
writer.save()
