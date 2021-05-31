#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import sys
from cv2 import cv2
# import cv2
import re
import numpy as np
from shapely.geometry import *
from struct import unpack
import math

import matplotlib.pyplot as pp

root_path = '/home/birl/climbingrobot_ws/src/codes/generate_JSON/'
phase = 'train'
folder_imgs = 'p6/p6_training_images/'
folder_annotation = 'p6/p6_training_annotation/'

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
      'supercategory': 'beverage',
      'keypoints': ['left_ahead',
                    'center_ahead',
                    'center',
                    'center_back',
                    'right_back'],  # only for keypoints
      'skeleton':[[0,1],[1,2],[2,3],[3,4],[1,3]]
  })


def get_category_id(cls):
  for category in dataset['categories']:
    if category['name'] == cls:
      return category['id']

# img_list = [re.split('[_.]', f) for f in os.listdir(os.path.join(root_path, 'ch8_training_images'))] # 拆分 googe
# _indexes = sorted(img_list, key=lambda x:int(x[1])) # 排序
# indexes = [(f[0]+'_')+f[1] for f in _indexes] # 组合

img_list = [f.split('.') for f in os.listdir(os.path.join(root_path, folder_imgs))]
_indexes = sorted(img_list, key=lambda x:int(x[0])) # 排序
indexes = sorted([f.split('.')[0]
                   for f in os.listdir(os.path.join(root_path, folder_imgs))])

# if phase == 'train':
#   indexes = [line for line in _indexes if (
#       line) >= split]  # only for this file
# else:
#   indexes = [line for line in _indexes if int(line) <= split] # commentdd by googe

j = 0
id_m = 0
max_height = 0
min_height = 1000
max_width = 0
min_width = 1000
for index in indexes:
  print(_indexes[j], '----->','Processing: ' + index)
  img_type = _indexes[j]
    #   print('image_type: ', os.path.join(root_path, folder_imgs) + index + '.' + img_type[-1])
  im = cv2.imread(os.path.join(root_path, folder_imgs) + index + '.' + img_type[-1])

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
      'id': int(j),
      'license': 0,
      'width': width,
      'height': height
  })
  # anno_file = os.path.join(root_path, 'ch8_training_annotation/') + 'gt_' + index + '.txt'
  anno_file = os.path.join(root_path, folder_annotation) + index + '.txt'
  with open(anno_file) as f:
    lines = [line for line in f.readlines() if line.strip()]

    for i, line in enumerate(lines):
      if '\xef\xbb\xbf' in line:
        line = line.replace('\xef\xbb\xbf','')
      parts = line.strip().split(',')
      # parts_temp = line.strip().split(' ')
      # parts= parts_temp[0:8]
      # parts = list(map(float, parts))

      cls = 'text'

      parts_x = [int(float(parts[0])), int(float(parts[2])), int(float(parts[4])), int(float(parts[6]))]
      parts_x.sort()
      parts_y = [int(float(parts[1])), int(float(parts[3])), int(float(parts[5])), int(float(parts[7]))]
      parts_y.sort()

      xmin = parts_x[0]
      ymin = parts_y[0]
      xmax = parts_x[3]
      ymax = parts_y[3]
      width = max(0, xmax - xmin + 1)
      height = max(0, ymax - ymin + 1)

      if width == 0 or height == 0:
        continue
      # add seg 
      segs = [int(float(kkpart)) for kkpart in parts[0:8]]  # four points

      xt = [float(segs[ikpart]) for ikpart in range(0, len(segs), 2)]
      yt = [float(segs[ikpart]) for ikpart in range(1, len(segs), 2)]

      mean_x = np.mean(xt) # 求取均值
      mean_y = np.mean(yt)

      P2_x = mean_x
      P2_y = mean_y

      ahead_center_x = (xt[0] +xt[1])/2
      ahead_center_y = (yt[0] +yt[1])/2

      # P1_x = (ahead_center_x + P2_x)/2
      # P1_y = (ahead_center_y + P2_y)/2

      # P0_x = (xt[0] + P1_x)/2
      # P0_y = (yt[0] + P1_y)/2

      # back_center_x = (xt[2] + xt[3])/2
      # back_center_y = (yt[2] + yt[3])/2

      # P3_x = (P2_x + back_center_x)/2
      # P3_y = (P2_y + back_center_y)/2

      # P4_x = (P3_x + xt[2])/2
      # P4_y = (P3_y + yt[2])/2

      P1_x = ahead_center_x
      P1_y = ahead_center_y

      P0_x = xt[0]
      P0_y = yt[0]

      back_center_x = (xt[2] + xt[3])/2
      back_center_y = (yt[2] + yt[3])/2

      P3_x = back_center_x
      P3_y = back_center_y

      P4_x = xt[2]
      P4_y = yt[2]


      # add key_point
      keypoints = []
      keypoints.append(P0_x)
      keypoints.append(P0_y)
      keypoints.append(2)

      keypoints.append(P1_x)
      keypoints.append(P1_y)
      keypoints.append(2)

      keypoints.append(P2_x) # center point
      keypoints.append(P2_y)
      keypoints.append(2)

      keypoints.append(P3_x)
      keypoints.append(P3_y)
      keypoints.append(2)

      keypoints.append(P4_x)
      keypoints.append(P4_y)
      keypoints.append(2)
      
      color1 = [0,255, 255]
      color2 = [0, 255, 0]
      for l in range(0,5):
          if l < 3:
              p1 = tuple([segs[2*l], segs[2*l+1]])
              p2 = tuple([segs[2*(l+1)], segs[2*(l+1)+1]])
              cv2.line(im, p1, p2, color1, thickness=2, lineType=cv2.LINE_AA)

              p11 = tuple([int(keypoints[3*l]), int(keypoints[3*l+1])])
              cv2.circle(im, p11, radius=5, color=color1, thickness=-1, lineType=cv2.LINE_AA)
          elif l == 3:
              p1 = tuple([segs[2*l], segs[2*l+1]])
              p2 = tuple([segs[0], segs[1]])
              cv2.line(im, p1, p2, color2, thickness=2, lineType=cv2.LINE_AA)

              p11 = tuple([int(keypoints[3*l]), int(keypoints[3*l+1])])
              cv2.circle(im, p11, radius=5, color=color1, thickness=-1, lineType=cv2.LINE_AA)
          else:
              p11 = tuple([int(keypoints[3*l]), int(keypoints[3*l+1])])
              cv2.circle(im, p11, radius=5, color=color2, thickness=-1, lineType=cv2.LINE_AA)
      
      pp.imshow(im)
      pp.pause(0.5)
      ''' indexing gt
      
      '''
      dataset['annotations'].append({
        'area': width * height,
        'bbox': [xmin, ymin, width, height],
        'category_id': get_category_id(cls),
        'id': (id_m+1),
        'image_id': int(j),
        'iscrowd': 0,
        'segmentation': [segs],
        # 'segmentation_shrink': [segs_shrink],
        'keypoints': keypoints,
        'num_keypoints':4,
        })
      id_m += 1
  j += 1

print('max_height = ', max_height, '\n min_height = ', min_height, '\n max_width = ', max_width, '\n min_width = ', min_width)

folder = os.path.join(root_path, 'annotations')
if not os.path.exists(folder):
  os.makedirs(folder)

if phase.split('_')[-1] == 'train':
  json_name = os.path.join(root_path, 'annotations/{}.json'.format(phase))
else:
  json_name = os.path.join(root_path, 'annotations/{}.json'.format(phase))

with open(json_name, 'w') as f:
  json.dump(dataset, f)
