
import os
import json
import shutil

import numpy as np
from tqdm import tqdm
from transforms3d.quaternions import mat2quat
from scipy.spatial.transform import Rotation as R

def opencv2opengl(w2c):
    w2c[:3, 2] = -w2c[:3, 2]
    w2c[:3, 1] = -w2c[:3, 1]
    return w2c

def process_extrinsics_to_imagestxt(images_txt_file_path, images):
    with open(images_txt_file_path, "w") as images_txt_file:
        for i, img in enumerate(images):
            pose = opencv2opengl(np.asarray(img['transform_matrix']))
            # pose[0:3, 3] -= np.array([749097.778409, 2563728.848426, 11])
            pose = np.linalg.inv(pose)
            camera_id = img['cam_id'] + 1
            quaternion = mat2quat(pose[0:3, 0:3])
            translation = pose[0:3, 3].T
            # IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME
            image_name = img['file_path'].split('/')[-1]
            image_id = i + 1 

            images_txt_file.write("{0} {1} {2} {3} {4} {5} {6} {7} {8} {9}\n\n".format(
                image_id, 
                "%lf"%quaternion[0], "%lf"%quaternion[1], "%lf"%quaternion[2], "%lf"%quaternion[3],
                "%lf"%translation[0], "%lf"%translation[1], "%lf"%translation[2],
                camera_id, "%s"%image_name))
                
def process_camerastxt(images_txt_file_path, cams_colmap):
    with open(images_txt_file_path, 'w') as f:
        i = 0
        for camera_id, intrinsic in cams_colmap.items():
            print(intrinsic)
            fx, fy, cx, cy, w, h = intrinsic[0], intrinsic[1], intrinsic[2], intrinsic[3], \
                    intrinsic[4], intrinsic[5]

            camera_id = i + 1
            line = f'{camera_id} PINHOLE {w} {h} {fx} {fy} {cx} {cy}\n'
            f.write(line)
            i += 1

def process_points3Dtxt(scene_path, points3D_txt_file_path):
    shutil.copy(os.path.join(scene_path, 'merged_cloud.txt'), points3D_txt_file_path)
    

def identify_camera_group(frames):
    camera_group = {}
    cam_names = []
    for f in frames:
        if 'fl_x' not in f.keys(): continue

        fl_x, fl_y = f['fl_x'], f['fl_y']
        cx, cy = f['cx'], f['cy']
        w, h = f['w'], f['h']
        encoded_str = "%.4f %.4f %.4f %.4f %d %d" % (fl_x, fl_y, cx, cy, w, h)
        if encoded_str not in camera_group.keys():
            camera_group[encoded_str] = [fl_x, fl_y, cx, cy, w, h]
        cam_names.append(encoded_str)
    
    cam_ids = {}
    name_lists = list(camera_group.keys())
    for cname in cam_names:
        cam_id = name_lists.index(cname)
        cam_ids[cname] = cam_id

    camera_group_new = {}
    for nl in name_lists:
        camera_group_new[name_lists.index(nl)] = camera_group[nl]
    return camera_group_new, cam_ids

def main(scene_path, json_file, output_dir):
    os.makedirs(os.path.join(scene_path, output_dir), exist_ok=True)

    with open(os.path.join(scene_path, json_file), 'r') as f:
        transforms = json.load(f)

    cams_colmap = {}
    if 'fl_x' in transforms.keys(): # Single cam
        cams_colmap[0] = [transforms['fl_x'], transforms['fl_y'], transforms['cx'], transforms['cy'], transforms['w'], transforms['h']]
    else:
        camera_group, cam_ids = identify_camera_group(transforms['frames'])
    
    process_camerastxt(os.path.join(scene_path, output_dir, "cameras.txt"), camera_group)

    images = []
    for i, f in enumerate(transforms['frames']):
        if 'fl_x' not in f.keys(): continue
        fl_x, fl_y = f['fl_x'], f['fl_y']
        cx, cy = f['cx'], f['cy']
        w, h = f['w'], f['h']
        encoded_str = "%.4f %.4f %.4f %.4f %d %d" % (fl_x, fl_y, cx, cy, w, h)

        f['cam_id'] = cam_ids[encoded_str]
        images.append(f)
    
    process_extrinsics_to_imagestxt(os.path.join(scene_path, output_dir, "images.txt"), images)

    process_points3Dtxt(scene_path, os.path.join(scene_path, output_dir, "points3D.txt"))

if __name__ == "__main__":
    OUTPUT_DIR = './colmap/sparse/0'
    JSON_FILE = 'transforms.json'
    SCENE_PATH = './carla_pic_0603_Town01_cam1'
    main(SCENE_PATH, JSON_FILE, OUTPUT_DIR)
    SCENE_PATH = './carla_pic_0603_Town02_cam1'
    main(SCENE_PATH, JSON_FILE, OUTPUT_DIR)
    SCENE_PATH = './carla_pic_0603_Town03_cam1'
    main(SCENE_PATH, JSON_FILE, OUTPUT_DIR)
    SCENE_PATH = './carla_pic_0603_Town04_cam1'
    main(SCENE_PATH, JSON_FILE, OUTPUT_DIR)
    SCENE_PATH = './carla_pic_0603_Town05_cam1'
    main(SCENE_PATH, JSON_FILE, OUTPUT_DIR)
    SCENE_PATH = './carla_pic_0603_Town10_cam1'
    main(SCENE_PATH, JSON_FILE, OUTPUT_DIR)
    SCENE_PATH = './carla_pic_0603_Town01_cam3'
    main(SCENE_PATH, JSON_FILE, OUTPUT_DIR)
    SCENE_PATH = './carla_pic_0603_Town02_cam3'
    main(SCENE_PATH, JSON_FILE, OUTPUT_DIR)
    SCENE_PATH = './carla_pic_0603_Town03_cam3'
    main(SCENE_PATH, JSON_FILE, OUTPUT_DIR)
    SCENE_PATH = './carla_pic_0603_Town04_cam3'
    main(SCENE_PATH, JSON_FILE, OUTPUT_DIR)
    SCENE_PATH = './carla_pic_0603_Town05_cam3'
    main(SCENE_PATH, JSON_FILE, OUTPUT_DIR)
    SCENE_PATH = './carla_pic_0603_Town10_cam3'
    main(SCENE_PATH, JSON_FILE, OUTPUT_DIR)