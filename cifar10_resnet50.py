# -*- coding: utf-8 -*-
"""cifar10_resnet50.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1p9fRqUZV8NJWJG5DBBXyLnei7UVAIy_2
"""

import os, re, time, json
import PIL.Image, PIL.ImageFont, PIL.ImageDraw
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50
from matplotlib import pyplot as plt
import tensorflow_datasets as tfds

print("Tensorflow version " + tf.__version__)

batch_size=32
classes=['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

plt.rc("image",cmap="gray")
plt.rc("grid",linewidth=0)
plt.rc('xtick',top=False,bottom=False,labelsize="large")
plt.rc('ytick',left=False,right=False,labelsize="large")
plt.rc('axes', facecolor='F8F8F8', titlesize="large", edgecolor='white')
plt.rc('text', color='a8151a')
plt.rc('figure', facecolor='F0F0F0')# Matplotlib fonts
MATPLOTLIB_FONT_DIR = os.path.join(os.path.dirname(plt.__file__), "mpl-data/fonts/ttf")

def display_images(digits,predictions,labels,title):
  n=10
  indexes=np.random.choice(len(predictions),size=n)
  n_digits=digits[indexes]
  n_predictions=predictions[indexes]
  n_predictions=n_predictions.reshape((n,))
  n_labels=labels[indexes]
  fig=plt.figure(figsize=(20,4))
  plt.title(title)
  plt.xticks([])
  plt.yticks([])

  for i in range (10):
    ax=fig.add_subplot(1,10,i+1)
    class_index=n_predictions[i]
     
    plt.xlabel(classes[class_index])
    plt.xticks([])
    plt.yticks([])
    plt.imshow(n_digits[i])
def plot_metrics(metric_name, title, ylim=5):
  plt.title(title)
  plt.ylim(0,ylim)
  plt.plot(history.history[metric_name],color='blue',label=metric_name)
  plt.plot(history.history['val_' + metric_name],color='green',label='val_' + metric_name)

(training_images,training_labels),(validation_images,validation_labels)=tf.keras.datasets.cifar10.load_data()

display_images(training_images,training_labels,training_labels,"Training Data")

def preprocess_image_input(input_images):
  input_images=input_images.astype("float32")
  output_ims=tf.keras.applications.resnet50.preprocess_input(input_images)
  return output_ims

train_x=preprocess_image_input(training_images)
valid_x=preprocess_image_input(validation_images)

from tensorflow.python import metrics
def feature_extractor(inputs):
  feature_extractor=tf.keras.applications.resnet.ResNet50(input_shape=(224,224,3), include_top=False, weights='imagenet')(inputs)
  return feature_extractor

def classifier(inputs):
  x=tf.keras.layers.GlobalAveragePooling2D()(inputs)
  x=tf.keras.layers.Flatten()(x)
  x=tf.keras.layers.Dense(1024,activation="relu")(x)
  x = tf.keras.layers.Dense(512, activation="relu")(x)
  x=tf.keras.layers.Dense(10,activation="softmax", name="classification")(x)
  return x

def final_model(inputs):

    resize = tf.keras.layers.UpSampling2D(size=(7,7))(inputs)

    resnet_feature_extractor = feature_extractor(resize)
    classification_output = classifier(resnet_feature_extractor)

    return classification_output


def define_compile_model():
  inputs = tf.keras.layers.Input(shape=(32,32,3))
  
  classification_output = final_model(inputs) 
  model = tf.keras.Model(inputs=inputs, outputs = classification_output)
 
  model.compile(optimizer='SGD', 
                loss='sparse_categorical_crossentropy',
                metrics = ['accuracy'])
  
  return model

model=define_compile_model()
model.summary()

epochs=3

history = model.fit(train_x, training_labels, epochs=epochs, validation_data = (valid_x, validation_labels), batch_size=64)

plot_metrics("loss", "Loss")

plot_metrics("accuracy", "Accuracy")

