#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import sys
from cv2 import cv2
# import cv2/
import re
import numpy as np
from shapely.geometry import *
from struct import unpack
import math

# if len(sys.argv) < 4:
#   print("Usage: python this_file.py root_path phase image_folder annotation_folder")
#   print("For example: python convert_to_BDN_sequence_free_modified.py /home/birl/Data/PoleRecognition/codes/generate_JSON \
#                               train / test \
#                               p1/p1_training_images/ \
#                               p1/p1_training_annotation/")
#   exit(1)

# root_path = sys.argv[1]
# phase = sys.argv[2]
# # split = int(sys.argv[3])
# folder_imgs = sys.argv[3]
# folder_annotation = sys.argv[4]
root_path = '/home/birl/climbingrobot_ws/src/data_operation/generate_JSON'
phase = 'test'
# split = int(sys.argv[3])
folder_imgs = './p9/training/p5_training_images/'
folder_annotation = './p9/training/store_folder/'

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
      'keypoints': ['mean',
                    'xmin',
                    'x2',
                    'x3',
                    'xmax',
                    'ymin',
                    'y2',
                    'y3',
                    'ymax',
                    'cross']  # only for keypoints
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
  print('image_type: ', os.path.join(root_path, folder_imgs) + index + '.' + img_type[-1])
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
      segs = [float(kkpart) for kkpart in parts[0:8]]  # four points

      xt = [float(segs[ikpart]) for ikpart in range(0, len(segs), 2)]
      yt = [float(segs[ikpart]) for ikpart in range(1, len(segs), 2)]
      # cross
      l1 = LineString([(xt[0], yt[0]), (xt[2], yt[2])])
      l2 = LineString([(xt[1], yt[1]), (xt[3], yt[3])])
      p_l1l2 = l1.intersection(l2)
      poly1 = Polygon([(xt[0], yt[0]), (xt[1], yt[1]),
                       (xt[2], yt[2]), (xt[3], yt[3])])
      if not poly1.is_valid:
        print('Not valid polygon found. This bounding box is removing ...')
        continue
      if not p_l1l2.within(poly1):
        print('Not valid intersection found. This bounding box is removing ...')
        continue
      if poly1.area <= 10:
        print('Text region too small. This bounding box is removing ...')

      mean_x = np.mean(xt) # 求取均值
      mean_y = np.mean(yt)
      xt_sort = np.sort(xt)
      yt_sort = np.sort(yt)
      xt_argsort = list(np.argsort(xt))
      yt_argsort = list(np.argsort(yt))
      # indexing
      ldx = []
      for ildx in range(4):
        ldx.append(yt_argsort.index(xt_argsort[ildx]))
      all_types = [[1,2,3,4],[1,2,4,3],[1,3,2,4],[1,3,4,2],[1,4,2,3],[1,4,3,2],\
                    [2,1,3,4],[2,1,4,3],[2,3,1,4],[2,3,4,1],[2,4,1,3],[2,4,3,1],\
                    [3,1,2,4],[3,1,4,2],[3,2,1,4],[3,2,4,1],[3,4,1,2],[3,4,2,1],\
                    [4,1,2,3],[4,1,3,2],[4,2,1,3],[4,2,3,1],[4,3,1,2],[4,3,2,1]]
      all_types = [[all_types[iat][0]-1,all_types[iat][1]-1,all_types[iat][2]-1,all_types[iat][3]-1] for iat in range(24)]
      match_type = all_types.index(ldx)

      half_x = (xt_sort + mean_x) / 2
      half_y = (yt_sort + mean_y) / 2

      # add key_point
      keypoints = []
      keypoints.append(mean_x)
      keypoints.append(mean_y)
      keypoints.append(2)
      for i in range(4):
        keypoints.append(half_x[i])
        keypoints.append(mean_y)
        keypoints.append(2)
      for i in range(4):
        keypoints.append(mean_x)
        keypoints.append(half_y[i])
        keypoints.append(2)
      try:
        keypoints.append(int(p_l1l2.x))
        keypoints.append(int(p_l1l2.y))
        keypoints.append(2)
      except Exception as e:
        print(e)
        # print('EIntersection found. This bounding is removing ...')
        continue
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
        'match_type': match_type
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
