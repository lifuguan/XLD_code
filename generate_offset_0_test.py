import shutil
import os
import numpy as np
import json
import os
import numpy as np

def generate_test(scene_path):
    if not os.path.exists(f"{scene_path}/test_pic/offset_left_0m"):
        os.mkdir(f"{scene_path}/test_pic/offset_left_0m")
    else:  
        return
    start_timestep, end_timestep, gap = 0, 150, 5
    for i, t in enumerate(range(start_timestep, end_timestep, gap)):
        src_json_file = os.path.join(f"{scene_path}/train_pic", f"train_camera_extrinsics_{t:06d}.json")
        src_png_file = os.path.join(f"{scene_path}/train_pic", f"train_camera0_{t:05d}.png")

        dst_json_file = os.path.join(f"{scene_path}/test_pic/offset_left_0m", f"eval_camera_extrinsics_{i:06d}.json")
        dst_png_file = os.path.join(f"{scene_path}/test_pic/offset_left_0m", f"eval_camera0_{i:05d}.png")
        shutil.copyfile(src_json_file, dst_json_file)
        shutil.copyfile(src_png_file, dst_png_file)

generate_test("data/carla_pic_0603_Town01")
generate_test("data/carla_pic_0603_Town02")
generate_test("data/carla_pic_0603_Town03")
generate_test("data/carla_pic_0603_Town04")
generate_test("data/carla_pic_0603_Town05")
generate_test("data/carla_pic_0603_Town10")
