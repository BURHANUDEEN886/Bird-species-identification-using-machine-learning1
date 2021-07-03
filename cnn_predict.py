
import numpy as np
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.models import Sequential, load_model
from tkinter import filedialog

#load model
img_width, img_height = 128, 128
model_path = './models/model_25.h5'
model_weights_path = './models/weights_25.h5'
model = load_model(model_path)
model.load_weights(model_weights_path)

#Prediction on a new picture
from keras.preprocessing import image as image_utils

from PIL import Image, ImageTk
import requests
from io import BytesIO
from tkinter import Tk,Label,Canvas,NW,Entry,Button 

def clicked(url):
    url =  filedialog.askopenfilename(initialdir = "E:/Projects 2020/Bird Species/",title = "choose your file")
    test_image = Image.open(url)#BytesIO(response.content))
    put_image = test_image.resize((400,400)) 
    test_image = test_image.resize((128,128))  
    test_image = image_utils.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    
 
    result = model.predict_on_batch(test_image)
    print(result)
    if result[0][0] == 1:
        ans='AFRICAN CROWNED CRANE'        
    elif result[0][1] == 1:
        ans = 'AFRICAN FIREFINCH'
    elif result[0][2] == 1:
        ans='INDIAN BUSTARD'        
    elif result[0][3] == 1:
        ans = 'INDIAN PITTA'       
    elif result[0][4] == 1:
        ans = 'INDIGO BUNTING'   
    print ("prediction",ans)

clicked('2.jpg')



