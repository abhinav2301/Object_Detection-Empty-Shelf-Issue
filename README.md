# Object Detection Module to counter Empty Shelf Issue (Retail)

## Introduction
  Creating accurate machine learning models capable of localizing and identifying multiple objects in
a single image remains a core challenge in computer vision. The TensorFlow Object Detection API
is an open source framework built on top of TensorFlow that makes it easy to construct, train and
deploy object detection models.
  ImageAI is a python library built to empower developers, researchers and students to build
applications and systems with self-contained Deep Learning and Computer Vision capabilities
using simple and few lines of code. This documentation is provided to provide detailed insight into
all the classes and functions available in ImageAI, coupled with a number of code
examples. ImageAI is a project developed by Moses Olafenwa and John Olafenwa , the DeepQuest
AI team.

## Methodology
[Image1](https://github.com/abhinav2301/Object_Detection/blob/master/Images/Object_Detection%20Methodology.PNG)
  Object Detection module takes a live camera feed, the camera can be attached to any port and will be
automatically mapped to the module. The image once feed into the module is then passed through the
object detection module, the cropping module and then finally the image classification module. The final
result is the csv with the list of all items and another csv with the list of items that are out of place if any.



# Result
