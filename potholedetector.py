# Ignore  the warnings
import warnings
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')

# data visualisation and manipulation
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns
 

#model selection
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score,precision_score,recall_score,confusion_matrix,roc_curve,roc_auc_score
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import LabelEncoder

#preprocess.
from keras.preprocessing.image import ImageDataGenerator

#dl libraraies
from keras import backend as K
from keras import regularizers
from keras.models import Sequential
from keras.models import load_model
from keras.models import Model
from keras.layers import Dense
from keras.optimizers import Adam,SGD,Adagrad,Adadelta,RMSprop
from keras.utils import to_categorical
from keras.callbacks import ReduceLROnPlateau

# specifically for cnn
from keras.layers import Dropout, Flatten,Activation
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
from keras.layers import InputLayer
 
import tensorflow as tf
import random as rn

# specifically for manipulating zipped images and getting numpy arrays of pixel values of images.
import cv2                  
import numpy as np  
from tqdm import tqdm
import os                   
from random import shuffle  
from zipfile import ZipFile
from PIL import Image
import keras.preprocessing.image as img
from keras.applications.resnet50 import ResNet50


#calling model
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','project.settings')
import django
django.setup()

from app1.models import complaint, pothole


model = Sequential()
model = load_model(r'C:/Users/GITANSHU/DjangoAPI/Pothole-Detector-Model.h5')


def Image():

    #calling database model
    current_complaint = complaint.objects.get(complaint_id = complaint_id)

    path = "C:/Users/GITANSHU/DjangoAPI/project/media/" + complaint_id + ".jpg"
    files = os.listdir(path)
    for i in tqdm(files):
        pth = os.path.join(path,i)
        X = cv2.imread(pth,cv2.IMREAD_COLOR)
        X = cv2.resize(X,(256,256))
        plt.figure()
        plt.imshow(X[:,:,::-1]) 
        plt.show()  

        X = np.array(X)
        X = np.expand_dims(X, axis=0)

        y_pred = np.round(model.predict(X))
       if y_pred[0][0] == 1:
            print("Plain Road")
        else:
            print("Pothole Road")

    
    
