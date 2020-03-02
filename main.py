import os
#import magic
import urllib.request
import matplotlib.pyplot as plt 
import cv2
from keras.preprocessing import image
from keras.models import load_model
import numpy as np 
import pandas as pd 
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]


app.config["IMAGE_UPLOADS"] = "static/uploads"

model=load_model("Malaria_Model.h5")
print("model Loaded")

@app.route('/')
def homepage():
    return render_template("main.html")



def load_image(img_path, show=False):

    img = image.load_img(img_path, target_size=(50, 50))
    img_tensor = image.img_to_array(img)                    # (height, width, channels)
    img_tensor = np.expand_dims(img_tensor, axis=0)         # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    img_tensor /= 255.                                      # imshow expects values in the range [0, 1]

    if show:
        plt.imshow(img_tensor[0])                           
        plt.axis('off')
        plt.show()

    return img_tensor



def tellme(detectimg):
  new_image =load_image(detectimg)
  pred = model.predict(new_image)
  
  yhat=round(pred[0][1])
  
  if(yhat==1):
    message="Early Stage of Malaria,go For check up as soon as Possible!!"
    return "Given Sample is Infected With Malaria!"+message
  if(yhat==0):
    message="Be Happy and stay Healthy"
    return "Given Sample is not Infected With Malaria"+message
  

#img="static/uploads/test.png"
#loaded=load_image(img)
#print(tellme(loaded,model))

@app.route('/malaria',methods=["GET","POST"])
def malaria():
    if request.method == "POST":

        if request.files:

            image = request.files["image"]
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            print("Image Saved")
            img="static/uploads/"+image.filename
            output=tellme(img)
            return render_template("malaria.html",imga=img,output=output)
    return render_template("malaria.html")


@app.route('/bone',methods=["GET","POST"])
def bone():
    if request.method == "POST":

        if request.files:

            image = request.files["image"]
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            print("Image Saved")
            img="static/uploads/"+image.filename
            output=tellme(img)
            return render_template("bone.html",imga=img,output=output)
    return render_template("bone.html")


@app.route('/cancer',methods=["GET","POST"])
def cancer():
    if request.method == "POST":

        if request.files:

            image = request.files["image"]
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            print("Image Saved")
            img="static/uploads/"+image.filename
            output=tellme(img)
            return render_template("cancer.html",imga=img,output=output)
    return render_template("cancer.html")



@app.route('/diabetes',methods=["GET","POST"])
def diabetes():
    if request.method == "POST":

        if request.files:

            image = request.files["image"]
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            print("Image Saved")
            img="static/uploads/"+image.filename
            output=tellme(img)
            return render_template("diabetes.html",imga=img,output=output)
    return render_template("diabetes.html")





def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route("/upload",methods=["GET","POST"])
def upload():
    if request.method == "POST":

        if request.files:

            image = request.files["image"]


            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            return redirect(request.url)
    return render_template("upload.html")






if __name__ == "__main__":
    app.run(threaded=False)