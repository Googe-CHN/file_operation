#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import sys
import cv2
import re
import numpy as np
from shapely.geometry import *
from struct import unpack
import math

root_path = '/home/birl/data/manvjie/datasets/training'
phase = 'train'
folder_imgs = 'images/'
folder_annotation = 'annotations_txt/'

dataset = {
    'licenses': [],
    'info': {},
    'categories': [],
    'images': [],
    'annotations': []
}

with open(os.path.join(root_path, 'classes.txt')) as f:
  classes = f.read().strip().split()   # stript(): 移除字符串头尾指定的字符（默认为空格或换行符）或字符序列,不能删除中间部分的字符.
                                       # split():  通过指定分隔符对字符串进行切片，如果参数 num 有指定值，则分隔 num+1 个子字符串
for i, cls in enumerate(classes, 1):
  dataset['categories'].append({
      'id': i,
      'name': cls,
      'supercategory': 'pokemon'
  })


def get_category_id(cls):
  for category in dataset['categories']:
    if category['name'] == cls:
      return category['id']

img_list = [f.split('.') for f in os.listdir(os.path.join(root_path, folder_imgs))]
_indexes = sorted(img_list, key=lambda x:int(x[0])) # 排序
indexes = sorted([f.split('.')[0]
                   for f in os.listdir(os.path.join(root_path, folder_imgs))])

j = 0
id_m = 0
max_height = 0
min_height = 1000
max_width = 0
min_width = 1000

for index in indexes:
  print(_indexes[id_m], '----->','Processing: ' + index)
  img_type = _indexes[id_m]
  print('image_type: ', os.path.join(root_path, folder_imgs) + index + '.' + img_type[-1])
  im = cv2.imread(os.path.join(root_path, folder_imgs) + index + '.' + img_type[-1])
  print(im)
  height, width, _ = im.shape

  if height > max_height:
    max_height = height

  if height < min_height:
    min_height = height

  if width > max_width:
    max_width = width

  if width < min_width:
    min_width = width

  dataset['images'].append({
      'coco_url': '',
      'date_captured': '',
      'file_name': index + '.' + img_type[-1],
      'flickr_url': '',
      'id': int(index),
      'license': 0,
      'width': width,
      'height': height
  })

  anno_file = os.path.join(root_path, folder_annotation) + index + '.txt'

  with open(anno_file) as f:
    lines = [line for line in f.readlines() if line.strip()]
    for i, line in enumerate(lines):
      if i==1:
          print('error')
      if '\xef\xbb\xbf' in line:
        line = line.replace('\xef\xbb\xbf','')
      parts = line.strip().split(',')

      parts_x = [float(parts[pp]) for pp in range(0, len(parts)-1, 2)]
      parts_x.sort()

      parts_y = [float(parts[pp]) for pp in range(1, len(parts)-1, 2)]
      parts_y.sort()

      xmin = parts_x[0]
      ymin = parts_y[0]
      xmax = parts_x[len(parts_x)-1]
      ymax = parts_y[len(parts_y)-1]
      width = max(0, xmax - xmin + 1)
      height = max(0, ymax - ymin + 1)

      if width == 0 or height == 0:
        continue
      # add seg 
      segmentations = [float(kkpart) for kkpart in parts[0:(len(parts)-1)]]
      ''' indexing gt
      
      '''
      dataset['annotations'].append({
        'area': width * height,
        'bbox': [xmin, ymin, width, height],
        'category_id': get_category_id(parts[len(parts)-1]),
        'id': (j+1),
        'image_id': int(index),
        'iscrowd': 0,
        'segmentation': [segmentations],
      })
      j += 1
  id_m +=1
print('max_height = ', max_height, '\n min_height = ', min_height, '\n max_width = ', max_width, '\n min_width = ', min_width)

folder = os.path.join(root_path, 'annotations')
if not os.path.exists(folder):
  os.makedirs(folder)

if phase.split('_')[-1] == 'train':
  json_name = os.path.join(root_path, 'annotations/instances_{}2014.json'.format(phase))
else:
  json_name = os.path.join(root_path, 'annotations/instances_{}2014.json'.format(phase))

with open(json_name, 'w') as f:
  json.dump(dataset, f)
