import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import cv2
from distutils.version import StrictVersion
from collections import defaultdict
from io import StringIO
from PIL import Image

# This is needed since the notebook is stored in the object_detection folder.

from object_detection.utils import ops as utils_ops

if StrictVersion(tf.__version__) < StrictVersion('1.12.0'):
  raise ImportError('Please upgrade your TensorFlow installation to v1.12.*.')

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

# What model to download.
MODEL_NAME = 'object_detection/Models/faster_rcnn_inception_resnet_v2_atrous_oid_v4_2018_12_12'

 #Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_FROZEN_GRAPH = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('object_detection/training', 'object-detection.pbtxt')

detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

#For the sake of simplicity we will use only 2 images:
# image1.jpg
# image2.jpg
# If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.
# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)

def run_inference_for_single_image(image, graph):
  with graph.as_default():
    with tf.Session() as sess:
      # Get handles to input and output tensors
      ops = tf.get_default_graph().get_operations()
      all_tensor_names = {output.name for op in ops for output in op.outputs}
      tensor_dict = {}
      for key in [
          'num_detections', 'detection_boxes', 'detection_scores',
          'detection_classes', 'detection_masks'
      ]:
        tensor_name = key + ':0'
        if tensor_name in all_tensor_names:
          tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
              tensor_name)
      if 'detection_masks' in tensor_dict:
        # The following processing is only for single image
        detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
        detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
        # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
        real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
        detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
        detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
            detection_masks, detection_boxes, image.shape[1], image.shape[2])
        detection_masks_reframed = tf.cast(
            tf.greater(detection_masks_reframed, 0.5), tf.uint8)
        # Follow the convention by adding back the batch dimension
        tensor_dict['detection_masks'] = tf.expand_dims(
            detection_masks_reframed, 0)
      image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

      # Run inference
      output_dict = sess.run(tensor_dict,
                             feed_dict={image_tensor: image})

      # all outputs are float32 numpy arrays, so convert types as appropriate
      output_dict['num_detections'] = int(output_dict['num_detections'][0])
      output_dict['detection_classes'] = output_dict[
          'detection_classes'][0].astype(np.int64)
      output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
      output_dict['detection_scores'] = output_dict['detection_scores'][0]
      if 'detection_masks' in output_dict:
        output_dict['detection_masks'] = output_dict['detection_masks'][0]
  return output_dict

def cropped(direct,k):
	PATH_TO_TEST_IMAGES_DIR = str(direct)+'/images'
	TEST_IMAGE_PATHS = PATH_TO_TEST_IMAGES_DIR + '/' + k
	image_path = str(TEST_IMAGE_PATHS)
	print(image_path)	
	image = Image.open(image_path)
	w,h = image.size
# the array based representation of the image will be used later in order to prepare the
# result image with boxes and labels on it.
	image_np = load_image_into_numpy_array(image)
# Expand dimensions since the model expects images to have shape: [1, None, None, 3]
	image_np_expanded = np.expand_dims(image_np, axis=0)
# Actual detection.
	output_dict = run_inference_for_single_image(image_np_expanded, detection_graph)
# Visualization of the results of a detection.
	vis_util.visualize_boxes_and_labels_on_image_array(
    	image_np,
    	output_dict['detection_boxes'],
    	output_dict['detection_classes'],
    	output_dict['detection_scores'],
    	category_index,
    	instance_masks=output_dict.get('detection_masks'),
   	use_normalized_coordinates=True,
    	line_thickness=8)
	cv2.imwrite(direct+'/images/bounded/'+k,image_np)
	n = 0
	n1=0	
	xmin=[]
	ymin=[]
	xmax=[]
	ymax=[]
	cenx=[]
	ceny=[]	
	pos=1
	a=0
	img = cv2.imread(image_path)
	#print(output_dict['detection_scores'])
	for i in output_dict['detection_scores']:
		if int(i*100) > 10:
			xmin.append(w * output_dict['detection_boxes'][n][1])
			ymin.append(h * output_dict['detection_boxes'][n][0])
			xmax.append(w * output_dict['detection_boxes'][n][3])
			ymax.append(h * output_dict['detection_boxes'][n][2])
			n += 1
	n2 = len(xmin)
	#zipped = list(zip(xmin,ymin,xmax,ymax))
	#zipped.sort()
	#xmin,ymin,xmax,ymax = zip(*zipped)
	#t = []
	#for i in range(n2):
	#	t.append(tuple((xmin[i],ymin[i],xmax[i],ymax[i])))
	#t = t.sort()
	#print(t)
	#for i in range(n2):
	#	xmin[i] = t[0][i]
	#	ymin[i] = t[1][i]
	#	xmax[i] = t[2][i]
	#	ymax[i] = t[3][i]
	
	for i in range(n2):
        # Last i elements are already in place
			for j in range(0, n2-i-1):
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
				if xmin[j]*ymin[j] > xmin[j+1]*ymin[j+1]:
					xmin[j],xmin[j+1] = xmin[j+1],xmin[j]
					ymin[j],ymin[j+1] = ymin[j+1],ymin[j]
					xmax[j],xmax[j+1] = xmax[j+1],xmax[j]
					ymax[j],ymax[j+1] = ymax[j+1],ymax[j]
					#output_dict['detection_scores'][j],output_dict['detection_scores'][j+1] = output_dict['detection_scores'][j+1],output_dict['detection_scores'][j]
	for i in range(n2):
		print(xmin[i],ymin[i],xmax[i],ymax[i])	    
	for i in range(0,len(xmin)):
		cenx.append(float(xmin[i])+(float(xmax[i])-float(xmin[i]))/2)
		ceny.append(float(ymin[i])+(float(ymax[i])-float(ymin[i]))/2)
#	cenx.append(0)
#	ceny.append(0)	
	#print(cenx,ceny)
	#pos = xmax.index(max(xmax)) 
	print(output_dict['detection_scores'])
	for i in range(0,len(cenx)):
		pos=1
		for j in range(0,len(cenx)):
			if cenx[i]>xmin[j] and cenx[i]<xmax[j] and cenx[i]!=cenx[j] and ceny[i]>ymin[j] and ceny[i]<ymax[j] and ceny[i]!=ceny[j]:
				if ((xmax[i]-xmin[i]) * (ymax[i]-ymin[i]))  < ((xmax[j]-xmin[j]) * (ymax[j]-ymin[j]))  :
				#if output_dict['detection_scores'][i] < output_dict['detection_scores'][j]:		
					pos=0				
		if pos==1:	
			im = img[int(ymin[i]):int(ymax[i]), int(xmin[i]):int(xmax[i])]
			cv2.imwrite(direct+'/images/crop/image'+ str(n1)+'.jpg',im)
			n1+=1

