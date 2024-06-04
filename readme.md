## Preprocess
data
├── carlc_pic_0603_Town0N
├────────────|─────────── train_pic
├────────────|─────────────── | ───────── camera_extrinscs_00000N.json
├────────────|─────────────── | ───────── cameraX_0000N.png
├────────────|─────────────── | ───────── lidar_0000N.ply
├────────────|─────────── test_pic
├────────────|─────────────── | ───────── offset_left_0m (don't exist, run generate_offset_0_test.py)
├────────────|─────────────── | ─────────────── | ───────── camera_extrinscs_00000N.json
├────────────|─────────────── | ─────────────── | ───────── cameraX_0000N.png
├────────────|─────────────── | ─────────────── | ───────── lidar_0000N.ply
├────────────|─────────────── | ───────── offset_left_1m
├────────────|─────────────── | ─────────────── | ───────── camera_extrinscs_00000N.json
├────────────|─────────────── | ─────────────── | ───────── cameraX_0000N.png
├────────────|─────────────── | ─────────────── | ───────── lidar_0000N.ply
├────────────|─────────────── | ───────── offset_left_2m
├────────────|─────────────── | ─────────────── | ───────── camera_extrinscs_00000N.json
├────────────|─────────────── | ─────────────── | ───────── cameraX_0000N.png
├────────────|─────────────── | ─────────────── | ───────── lidar_0000N.ply

#### 数据预处理
cp -r ../data/carla_pic_0602/intrinsics data/carla_pic_0603_Town01
cp -r ../data/carla_pic_0602/extrinsics data/carla_pic_0603_Town01
cp -r ../data/carla_pic_0602/intrinsics data/carla_pic_0603_Town02
cp -r ../data/carla_pic_0602/extrinsics data/carla_pic_0603_Town02
cp -r ../data/carla_pic_0602/intrinsics data/carla_pic_0603_Town03
cp -r ../data/carla_pic_0602/extrinsics data/carla_pic_0603_Town03
cp -r ../data/carla_pic_0602/intrinsics data/carla_pic_0603_Town04
cp -r ../data/carla_pic_0602/extrinsics data/carla_pic_0603_Town04
cp -r ../data/carla_pic_0602/intrinsics data/carla_pic_0603_Town05
cp -r ../data/carla_pic_0602/extrinsics data/carla_pic_0603_Town05
cp -r ../data/carla_pic_0602/intrinsics data/carla_pic_0603_Town10
cp -r ../data/carla_pic_0602/extrinsics data/carla_pic_0603_Town10


python generate_offset_0_test.py
python rename.py
python convert_dnb_transforms.py


## Multi-GPU
ns-train nerfacto --machine.num-devices 4 --data ./ --pipeline.model.camera-optimizer.mode off

## NeRFacto
CUDA_VISIBLE_DEVICES=1 ns-train nerfacto --experiment-name nerfacto_cam1_offset_0m nerfstudio-data --eval-mode filename  --data ./
CUDA_VISIBLE_DEVICES=3 ns-train nerfacto --experiment-name nerfacto_cam1_offset_1m nerfstudio-data --eval-mode filename  --data ./
CUDA_VISIBLE_DEVICES=0 ns-train nerfacto --experiment-name nerfacto_cam1_offset_2m nerfstudio-data --eval-mode filename  --data ./
CUDA_VISIBLE_DEVICES=3 ns-train nerfacto --experiment-name nerfacto_cam1_offset_4m nerfstudio-data --eval-mode filename  --data ./

CUDA_VISIBLE_DEVICES=1 ns-train nerfacto --experiment-name nerfacto_cam1_offset_0m nerfstudio-data --eval-mode filename  --data ./
CUDA_VISIBLE_DEVICES=3 ns-train nerfacto --experiment-name nerfacto_cam1_offset_1m nerfstudio-data --eval-mode filename  --data ./
CUDA_VISIBLE_DEVICES=1 ns-train nerfacto --experiment-name nerfacto_cam1_offset_2m nerfstudio-data --eval-mode filename  --data ./
CUDA_VISIBLE_DEVICES=3 ns-train nerfacto --experiment-name nerfacto_cam1_offset_4m nerfstudio-data --eval-mode filename  --data ./

## Instant-NGP
cd carla_pic_0603_Town01_cam1
CUDA_VISIBLE_DEVICES=0 ns-train instant-ngp --experiment-name instant_ngp_cam1 nerfstudio-data --eval-mode filename  --data ./
CUDA_VISIBLE_DEVICES=0 ns-eval --load-config outputs/instant_ngp_cam1/instant-ngp/2024-06-04_145815/config.yml --output-path ./instant-ngp_offset_0m/result.json --render-output-path ./instant-ngp_offset_0m

cd carla_pic_0603_Town01_cam3
CUDA_VISIBLE_DEVICES=1 ns-train instant-ngp --experiment-name instant_ngp_cam3 nerfstudio-data --eval-mode filename  --data ./
CUDA_VISIBLE_DEVICES=1 ns-eval --load-config outputs/instant_ngp_cam3/instant-ngp/2024-06-04_145852/config.yml --output-path ./instant-ngp_offset_0m/result.json --render-output-path ./instant-ngp_offset_0m

cd carla_pic_0603_Town02_cam1
CUDA_VISIBLE_DEVICES=2 ns-train instant-ngp --experiment-name instant_ngp_cam1 nerfstudio-data --eval-mode filename  --data ./
CUDA_VISIBLE_DEVICES=2 ns-eval --load-config outputs/instant_ngp_cam1/instant-ngp/2024-06-04_150128/config.yml --output-path ./instant-ngp_offset_0m/result.json --render-output-path ./instant-ngp_offset_0m


cd carla_pic_0603_Town02_cam3
CUDA_VISIBLE_DEVICES=3 ns-train instant-ngp --experiment-name instant_ngp_cam3 nerfstudio-data --eval-mode filename  --data ./
CUDA_VISIBLE_DEVICES=3 ns-eval --load-config outputs/instant_ngp_cam3/instant-ngp/2024-06-04_150137/config.yml --output-path ./instant-ngp_offset_0m/result.json --render-output-path ./instant-ngp_offset_0m

cd carla_pic_0603_Town03_cam1
CUDA_VISIBLE_DEVICES=0 ns-train instant-ngp --experiment-name instant_ngp_cam1 nerfstudio-data --eval-mode filename  --data ./
CUDA_VISIBLE_DEVICES=0 ns-eval --load-config outputs/instant_ngp_cam1/instant-ngp/2024-06-04_164518/config.yml  --output-path ./instant-ngp_offset_0m/result.json --render-output-path ./instant-ngp_offset_0m

cd carla_pic_0603_Town04_cam1
CUDA_VISIBLE_DEVICES=1 ns-train instant-ngp --experiment-name instant_ngp_cam1 nerfstudio-data --eval-mode filename  --data ./
CUDA_VISIBLE_DEVICES=1 ns-eval --load-config outputs/instant_ngp_cam1/instant-ngp/2024-06-04_164544/config.yml --output-path ./instant-ngp_offset_0m/result.json --render-output-path ./instant-ngp_offset_0m

cd carla_pic_0603_Town05_cam1
CUDA_VISIBLE_DEVICES=2 ns-train instant-ngp --experiment-name instant_ngp_cam1 nerfstudio-data --eval-mode filename  --data ./
CUDA_VISIBLE_DEVICES=2 ns-eval --load-config outputs/instant_ngp_cam1/instant-ngp/2024-06-04_164601/config.yml --output-path ./instant-ngp_offset_0m/result.json --render-output-path ./instant-ngp_offset_0m

cd carla_pic_0603_Town10_cam1
CUDA_VISIBLE_DEVICES=3 ns-train instant-ngp --experiment-name instant_ngp_cam1 nerfstudio-data --eval-mode filename  --data ./
CUDA_VISIBLE_DEVICES=3 ns-eval --load-config outputs/instant_ngp_cam1/instant-ngp/2024-06-04_164626/config.yml --output-path ./instant-ngp_offset_0m/result.json --render-output-path ./instant-ngp_offset_0m

## 3D-GS
#### 预处理
##### 跑代码前，先修改convert_carlc_dnb.py中的数据路径

mkdir -p carla_pic_0603_Town01_cam1/images
cd carla_pic_0603_Town01_cam1/images 
ln -s ../../data/carla_pic_0603_Town01/train_pic/train_camera0_00* ./ && ln -s ../../data/carla_pic_0603_Town01/train_pic/train_camera1_00* ./
ln -s ../../data/carla_pic_0603_Town01/train_pic/train_camera2_00* ./ && ln -s ../../data/carla_pic_0603_Town01/test_pic/offset_left_0m/eval_camera0_00* ./
python convert_carlc_dnb.py && python merge_lidar.py && python transform2colmap.py

mkdir -p carla_pic_0603_Town02_cam1/images
cd carla_pic_0603_Town02_cam1/images 
ln -s ../../data/carla_pic_0603_Town02/train_pic/train_camera0_00* ./ && ln -s ../../data/carla_pic_0603_Town02/train_pic/train_camera1_00* ./
ln -s ../../data/carla_pic_0603_Town02/train_pic/train_camera2_00* ./ && ln -s ../../data/carla_pic_0603_Town02/test_pic/offset_left_0m/eval_camera0_00* ./

mkdir -P carla_pic_0603_Town03_cam1/images
mkdir -P carla_pic_0603_Town04_cam1/images
mkdir -P carla_pic_0603_Town05_cam1/images

#### 跑代码
cd carla_pic_0603_Town02_cam1
CUDA_VISIBLE_DEVICES=5 ns-train splatfacto --experiment-name gsplat_cam1 colmap --eval-mode filename  --data ./ --downscale-factor 1

cd carla_pic_0603_Town02_cam1
CUDA_VISIBLE_DEVICES=6 ns-train splatfacto --experiment-name gsplat_cam1 colmap --eval-mode filename  --data ./ --downscale-factor 1
ns-eval --load-config outputs/gsplat_w_pc/splatfacto/2024-06-03_235733/config.yml --output-path ./gsplat_offset_1m/result.json --render-output-path ./gsplat_offset_1m

