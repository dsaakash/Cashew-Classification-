import cv2
import numpy as np
from skimage import measure
from skimage.measure import label, regionprops, regionprops_table
from skimage.color import rgb2gray
#from skimage.color import rgb2hsv
#from skimage.io import imread
#from skimage.util import img_as_ubyte
#from skimage.feature import greycomatrix, greycoprops


def ShapeSizeFeature(thresh):
    #sz=thresh.shape
    labels = label(thresh)
    """
    unique, counts = np.unique(labels, return_counts=True)
    list_seg = list(zip(unique, counts))[1:]  # the 0 label is by default background so take the rest
    largest = max(list_seg, key=lambda x: x[1])[0]
    labels_max = (labels == largest).astype(int)
    #regions1=regionprops(labels_max)
    """
    props = regionprops_table(thresh, properties=('area','major_axis_length',
                                                  'minor_axis_length','centroid','local_centroid',
                                                'coords','eccentricity','equivalent_diameter',
                                                  'orientation','perimeter','perimeter',
                                                  'solidity'))
    #'area_bbox','area_convex','area_filled','bbox','euler_number','extent','feret_diameter_max','image','image_convex','image_filled',
      #                                            'inertia_tensor','inertia_tensor_eigvals','label','moments','moments_central','moments_hu',
       ##                                           'moments_normalized','slice',
    temparea = props['area']
    tempperimeter = props['perimeter']
    Roundness = (4 * np.pi *temparea)/(tempperimeter ** 2)
    props['Roundness']=Roundness
    tempmajoraxis=props['major_axis_length']
    Compactness=np.sqrt((4*temparea)/np.pi)/tempmajoraxis
    props['Compactness']=Compactness
    tempminoraxis=props['minor_axis_length']
    SF3=temparea/((tempmajoraxis/2)*(tempminoraxis/2)*np.pi)
    props['SF3'] = SF3
    return props



