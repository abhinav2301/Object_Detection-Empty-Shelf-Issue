import numpy as np
import argparse
import time
import datetime
import cv2
import os
#import PySimpleGUI as sg
from PIL import Image
from imageai.Prediction.Custom import CustomImagePrediction
import glob
import random
from Image_capture import videocap
from Image_det import detection
import Image_capture
import object_detection.ssd
from object_detection.ssd import cropped
import csv
from shutil import copyfile

direc = os.getcwd()
i = -1
classes = ['Time']
global bound
bound = []


n = 0
duck = []
for j in os.listdir(direc + '/Dataset/train'):
    n += 1
    classes.append(j)
with open("Results.csv", "w") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(classes)
model_name=os.listdir(direc + '/Dataset/models')
model_name.sort()
for i in range(0,len(model_name)-1):
        os.remove(direc + '/Dataset/models/'+model_name[i])
while 1:

    for fil in os.listdir(direc + '/images/crop'):
        os.remove(direc + '/images/crop/' + fil)

    i = i + 1
    direct = direc
    os.chdir(direct)
    videocap(i)
    # When everything done, release the capture
    print('[Process] Detecting Objects : ')
    img = str(i)+'.jpg'
    cropped(direct, img)
    print('[Process] Classifying the Images ')
    detection(i, n)

    copyfile('Results.csv', 'Database/Results_' +
             str(str(datetime.datetime.now())[:-16])+'.csv')
    os.chdir(direc)
