import pycocotools.coco as cocoapi
import sys
from cv2 import cv2
import numpy as np
import pickle
import json

#######################################################
## Note: this file needs to run in VerticeNet for the "pycocotools" lib
#######################################################
# SPLITS = ['val', 'train']
# ANN_PATH = '../data/coco/annotations/instances_{}2017.json'
# OUT_PATH = '../data/coco/annotations/instances_vertice_{}2017.json'
# IMG_DIR = '../data/coco/{}2017/'

SPLITS = ['test', 'train']
ANN_PATH = './p6/annotations/p6_{}.json'
OUT_PATH = './p6/annotations/p6_vertice_{}.json'
IMG_DIR = './datasets/p6/p6_{}_images/'
DEBUG = True

from scipy.spatial import ConvexHull

def _coco_box_to_bbox(box):
    bbox = np.array([box[0], box[1], box[0] + box[2], box[1] + box[3]],
                    dtype=np.int32)
    return bbox

def _get_vertice_points(pts):
    # 对于与水平线的夹角在±3°内的杆件轴线，选择x值较小的中点作为轴线向量的终点
    # 其他情况，选取y值较小的中点作为轴线向量的终点
    # 顶点顺序：轴线向量终点左侧的点作为起点，其他点以顺时针顺序排列
    thresh = 0.02

    V_end_temp = (pts[0,:] + pts[1,:])/2
    V_start_temp = (pts[2,:] + pts[3,:])/2

    if (V_end_temp[0] - V_start_temp[0]) > 0 and \
        (V_end_temp[1] - V_start_temp[1]) <= thresh * (V_end_temp[0] - V_start_temp[0]):
        v0 = pts[2,:]
        v1 = pts[3,:]
        v2 = pts[0,:]
        v3 = pts[1,:]
    else:
        v0 = pts[0,:]
        v1 = pts[1,:]
        v2 = pts[2,:]
        v3 = pts[3,:]

    return np.array([v0, v1, v2, v3])

if __name__ == '__main__':
    for split in SPLITS:
        data = json.load(open(ANN_PATH.format(split), 'r'))
        coco = cocoapi.COCO(ANN_PATH.format(split))
        img_ids = coco.getImgIds()
        num_images = len(img_ids)
        num_classes = 80
        tot_box = 0
        print('num_images', num_images)
        anns_all = data['annotations']
        for i, ann in enumerate(anns_all):
            tot_box += 1
            bbox = ann['bbox']
            seg = ann['segmentation']
            if type(seg) == list:
                if len(seg) == 1:
                    pts = np.array(seg[0]).reshape(-1, 2)
                else:
                    pts = []
                    for v in seg:
                        pts += v
                    pts = np.array(pts).reshape(-1, 2)
            else:
                mask = coco.annToMask(ann) * 255
                tmp = np.where(mask > 0)
                pts = np.asarray(tmp).transpose()[:, ::-1].astype(np.int32)
            vertice_points = _get_vertice_points(pts).astype(np.int32)
            anns_all[i]['vertice_points'] = vertice_points.copy().tolist()
            if DEBUG:
                img_id = ann['image_id']
                img_info = coco.loadImgs(ids=[img_id])[0]
                img_path = IMG_DIR.format(split) + img_info['file_name']
                img = cv2.imread(img_path)
                if type(seg) == list:
                    mask = np.zeros((img.shape[0], img.shape[1], 1), dtype=np.uint8)
                    cv2.fillPoly(mask, [pts.astype(np.int32).reshape(-1, 1, 2)], (255,0,0))
                else:
                    mask = mask.reshape(img.shape[0], img.shape[1], 1)
                img = (0.4 * img + 0.6 * mask).astype(np.uint8)
                bbox = _coco_box_to_bbox(ann['bbox'])
                cl = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255)]
                for j in range(vertice_points.shape[0]):
                    cv2.circle(img, (vertice_points[j, 0], vertice_points[j, 1]),
                                    5, cl[j], -1)
                cv2.imshow('img', img)
                cv2.waitKey()
        print('tot_box', tot_box)   
        data['annotations'] = anns_all
        json.dump(data, open(OUT_PATH.format(split), 'w'))