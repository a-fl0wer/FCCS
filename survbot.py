from ctypes import *
import cv2
from time import gmtime, strftime, time, sleep
import json
from transmitter import *
from parameters import parameters

class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]

class DETECTION(Structure):
    _fields_ = [("bbox", BOX),
                ("classes", c_int),
                ("prob", POINTER(c_float)),
                ("mask", POINTER(c_float)),
                ("objectness", c_float),
                ("sort_class", c_int)]

class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]

class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]

#lib = CDLL("/home/pjreddie/documents/darknet/libdarknet.so", RTLD_GLOBAL)
lib = CDLL("/home/fl0wer/_FCCS/_CNN/darknet/libdarknet.so", RTLD_GLOBAL)
lib.network_width.argtypes = [c_void_p]
lib.network_width.restype = c_int
lib.network_height.argtypes = [c_void_p]
lib.network_height.restype = c_int

predict = lib.network_predict
predict.argtypes = [c_void_p, POINTER(c_float)]
predict.restype = POINTER(c_float)

set_gpu = lib.cuda_set_device
set_gpu.argtypes = [c_int]

make_image = lib.make_image
make_image.argtypes = [c_int, c_int, c_int]
make_image.restype = IMAGE

get_network_boxes = lib.get_network_boxes
get_network_boxes.argtypes = [c_void_p, c_int, c_int, c_float, c_float, POINTER(c_int), c_int, POINTER(c_int)]
get_network_boxes.restype = POINTER(DETECTION)

make_network_boxes = lib.make_network_boxes
make_network_boxes.argtypes = [c_void_p]
make_network_boxes.restype = POINTER(DETECTION)

# void free_detections(detection *dets, int n)
free_detections = lib.free_detections
free_detections.argtypes = [POINTER(DETECTION), c_int]

free_ptrs = lib.free_ptrs
free_ptrs.argtypes = [POINTER(c_void_p), c_int]

network_predict = lib.network_predict
network_predict.argtypes = [c_void_p, POINTER(c_float)]

reset_rnn = lib.reset_rnn
reset_rnn.argtypes = [c_void_p]

load_net = lib.load_network
load_net.argtypes = [c_char_p, c_char_p, c_int]
load_net.restype = c_void_p

# void do_nms_obj(detection *dets, int total, int classes, float thresh)
do_nms_obj = lib.do_nms_obj
do_nms_obj.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

do_nms_sort = lib.do_nms_sort
do_nms_sort.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

free_image = lib.free_image
free_image.argtypes = [IMAGE]

letterbox_image = lib.letterbox_image
letterbox_image.argtypes = [IMAGE, c_int, c_int]
letterbox_image.restype = IMAGE

load_meta = lib.get_metadata
lib.get_metadata.argtypes = [c_char_p]
lib.get_metadata.restype = METADATA

load_image = lib.load_image_color
load_image.argtypes = [c_char_p, c_int, c_int]
load_image.restype = IMAGE

#void rgbgr_image(image im)
rgbgr_image = lib.rgbgr_image
rgbgr_image.argtypes = [IMAGE]

#float *network_predict_image(network *net, image im)
predict_image = lib.network_predict_image
predict_image.argtypes = [c_void_p, IMAGE]
predict_image.restype = POINTER(c_float)


def cap_img(location):
    #capture from camera
    cam_adjustment_delay = 5
    cap = cv2.VideoCapture(0)
    for i in range(cam_adjustment_delay):
        img = cap.read()
    _, img = img
    cv2.imwrite(location, img)

def json_save(structure,json_loc):
    with open(json_loc, 'w') as outfile:
        json.dump(structure, outfile)

def detect(net, meta, image, thresh=.5, hier_thresh=.5, nms=.45):
    im = load_image(image, 0, 0)
    num = c_int(0)
    pnum = pointer(num)
    predict_image(net, im)

    #DETECTION class structure
    dets = get_network_boxes(net, im.w, im.h, thresh, hier_thresh, None, 0, pnum)
    num = pnum[0]
    if (nms): do_nms_obj(dets, num, meta.classes, nms);

    res = []
    for j in range(num):
        for i in range(meta.classes):
            if dets[j].prob[i] > 0:
                b = dets[j].bbox
                res.append((meta.names[i], dets[j].prob[i], (b.x, b.y, b.w, b.h)))

    res = sorted(res, key=lambda x: -x[1])
    free_image(im)
    free_detections(dets, num)

    return res


[dt,API_ENDPOINT,MAC,data_loc,cfg_loc,weights_loc,cap_loc,json_loc]\
    = parameters()

#All information will be stored here
info = {}

'''LOAD DARKNET'''

net = load_net(cfg_loc, weights_loc, 0)
meta = load_meta(data_loc)

'''DETECT & UPLOAD'''

while True:

    ti0_s = time()

    #Datetime
    ti0 = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    #capturing
    cap_img(cap_loc)

    #analysing
    r = detect(net, meta, cap_loc)

    if r == []:
        info['forest_danger'] = 0
    else:
        info['forest_danger'] = 1

    info['mac'] = MAC
    info['time'] = ti0
    info['detections'] = r

    #saving
    json_save(info, json_loc)

    #POST request
    upload(API_ENDPOINT, info['forest_danger'], cap_loc, json_loc)

    ti1_s = time()
    exec_dt = ti1_s - ti0_s
    sleep(dt - exec_dt)

#
