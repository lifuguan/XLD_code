## Preprocess
```
data
├── carlc_pic_0603_Town0N
├────────────|─────────── intrinsics
├────────────|─────────────── | ───────── 0.txt
├────────────|─────────────── | ───────── 1.txt
├────────────|─────────────── | ───────── 2.txt
├────────────|─────────── extrinsics
├────────────|─────────────── | ───────── 0.txt
├────────────|─────────────── | ───────── 1.txt
├────────────|─────────────── | ───────── 2.txt
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
├────────────|─────────────── | ───────── offset_left_4m
├────────────|─────────────── | ─────────────── | ───────── camera_extrinscs_00000N.json
├────────────|─────────────── | ─────────────── | ───────── cameraX_0000N.png
├────────────|─────────────── | ─────────────── | ───────── lidar_0000N.ply
```

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
cd carla_pic_0603_Town01_cam1
CUDA_VISIBLE_DEVICES=1 ns-train nerfacto --pipeline.model.camera-optimizer.mode off --experiment-name nerfacto_offset_1m nerfstudio-data --eval-mode filename  --data ./
CUDA_VISIBLE_DEVICES=2 ns-eval --load-config outputs/nerfacto_offset_1m/nerfacto/2024-06-06_145158/config.yml    --output-path ./nerfacto_offset_1/result.json --render-output-path ./nerfacto_offset_1
## Instant-NGP
cd carla_pic_0603_Town01_cam1
CUDA_VISIBLE_DEVICES=0 ns-train instant-ngp --experiment-name instant_ngp_offset_1 nerfstudio-data --eval-mode filename  --data ./
CUDA_VISIBLE_DEVICES=0 ns-eval --load-config outputs/instant_ngp_offset_1/instant-ngp/2024-06-06_165753/config.yml     --output-path ./instant-ngp_offset_1m/result.json --render-output-path ./instant-ngp_offset_1m


## 3D-GS
#### 预处理
##### 跑代码前，先修改convert_carlc_dnb.py中的数据路径
python convert_carlc_dnb.py && python merge_lidar.py && python transform2colmap.py

mkdir -p carla_pic_0603_Town01_cam3/images
cd carla_pic_0603_Town01_cam3/images 
ln -s ../../data/carla_pic_0603_Town01/train_pic/train_camera0_00* ./ && ln -s ../../data/carla_pic_0603_Town01/train_pic/train_camera1_00* ./
ln -s ../../data/carla_pic_0603_Town01/train_pic/train_camera2_00* ./ && ln -s ../../data/carla_pic_0603_Town01/test_pic/offset_left_0m/eval_camera0_00* ./
cd ../../

mkdir -p carla_pic_0603_Town02_cam3/images
cd carla_pic_0603_Town02_cam3/images 
ln -s ../../data/carla_pic_0603_Town02/train_pic/train_camera0_00* ./ && ln -s ../../data/carla_pic_0603_Town02/train_pic/train_camera1_00* ./
ln -s ../../data/carla_pic_0603_Town02/train_pic/train_camera2_00* ./ && ln -s ../../data/carla_pic_0603_Town02/test_pic/offset_left_0m/eval_camera0_00* ./
cd ../../

mkdir -p carla_pic_0603_Town03_cam3/images
cd carla_pic_0603_Town03_cam3/images 
ln -s ../../data/carla_pic_0603_Town03/train_pic/train_camera0_00* ./ && ln -s ../../data/carla_pic_0603_Town03/train_pic/train_camera1_00* ./
ln -s ../../data/carla_pic_0603_Town03/train_pic/train_camera2_00* ./ && ln -s ../../data/carla_pic_0603_Town03/test_pic/offset_left_0m/eval_camera0_00* ./
cd ../../

mkdir -p carla_pic_0603_Town04_cam3/images
cd carla_pic_0603_Town04_cam3/images 
ln -s ../../data/carla_pic_0603_Town04/train_pic/train_camera0_00* ./ && ln -s ../../data/carla_pic_0603_Town04/train_pic/train_camera1_00* ./
ln -s ../../data/carla_pic_0603_Town04/train_pic/train_camera2_00* ./ && ln -s ../../data/carla_pic_0603_Town04/test_pic/offset_left_0m/eval_camera0_00* ./
cd ../../

mkdir -p carla_pic_0603_Town05_cam3/images
cd carla_pic_0603_Town05_cam3/images 
ln -s ../../data/carla_pic_0603_Town05/train_pic/train_camera0_00* ./ && ln -s ../../data/carla_pic_0603_Town05/train_pic/train_camera1_00* ./
ln -s ../../data/carla_pic_0603_Town05/train_pic/train_camera2_00* ./ && ln -s ../../data/carla_pic_0603_Town05/test_pic/offset_left_0m/eval_camera0_00* ./
cd ../../

mkdir -p carla_pic_0603_Town10_cam3/images
cd carla_pic_0603_Town10_cam3/images 
ln -s ../../data/carla_pic_0603_Town10/train_pic/train_camera0_00* ./ && ln -s ../../data/carla_pic_0603_Town10/train_pic/train_camera1_00* ./
ln -s ../../data/carla_pic_0603_Town10/train_pic/train_camera2_00* ./ && ln -s ../../data/carla_pic_0603_Town10/test_pic/offset_left_0m/eval_camera0_00* ./
cd ../../


#### 跑代码
cd carla_pic_0603_Town01_cam1
CUDA_VISIBLE_DEVICES=7 ns-eval --load-config outputs/gsplat_cam1/splatfacto/2024-06-04_184542/config.yml --output-path ./gsplat_offset_1m/result.json --render-output-path ./gsplat_offset_1m

cd carla_pic_0603_Town02_cam1
CUDA_VISIBLE_DEVICES=7 ns-eval --load-config outputs/gsplat_cam1/splatfacto/2024-06-04_171316/config.yml --output-path ./gsplat_offset_1m/result.json --render-output-path ./gsplat_offset_1m

cd carla_pic_0603_Town03_cam1
CUDA_VISIBLE_DEVICES=6 ns-eval --load-config outputs/gsplat_cam1/splatfacto/2024-06-04_173618/config.yml --output-path ./gsplat_offset_1m/result.json --render-output-path ./gsplat_offset_1m

cd carla_pic_0603_Town04_cam1
CUDA_VISIBLE_DEVICES=5 ns-eval --load-config outputs/gsplat_cam1/splatfacto/2024-06-04_174532/config.yml --output-path ./gsplat_offset_1m/result.json --render-output-path ./gsplat_offset_1m

cd carla_pic_0603_Town05_cam1
CUDA_VISIBLE_DEVICES=4 ns-eval --load-config outputs/gsplat_cam1/splatfacto/2024-06-04_174638/config.yml --output-path ./gsplat_offset_1m/result.json --render-output-path ./gsplat_offset_1m

cd carla_pic_0603_Town10_cam1
CUDA_VISIBLE_DEVICES=4 ns-eval --load-config outputs/gsplat_cam1/splatfacto/2024-06-04_184924/config.yml --output-path ./gsplat_offset_1m/result.json --render-output-path ./gsplat_offset_1m

cd carla_pic_0603_Town01_cam3
CUDA_VISIBLE_DEVICES=5 ns-train splatfacto --experiment-name gsplat_offset_0m colmap --eval-mode filename  --data ./ --downscale-factor 1
CUDA_VISIBLE_DEVICES=5 ns-eval --load-config outputs/gsplat_offset_0m/splatfacto/2024-06-04_184542/config.yml --output-path ./gsplat_offset_0m/result.json --render-output-path ./gsplat_offset_0m

cd carla_pic_0603_Town02_cam3
CUDA_VISIBLE_DEVICES=6 ns-train splatfacto --experiment-name gsplat_offset_0m colmap --eval-mode filename  --data ./ --downscale-factor 1
CUDA_VISIBLE_DEVICES=6 ns-eval --load-config outputs/gsplat_offset_0m/splatfacto/2024-06-04_171316/config.yml --output-path ./gsplat_offset_0m/result.json --render-output-path ./gsplat_offset_0m

cd carla_pic_0603_Town03_cam3
CUDA_VISIBLE_DEVICES=7 ns-train splatfacto --experiment-name gsplat_offset_0m colmap --eval-mode filename  --data ./ --downscale-factor 1
CUDA_VISIBLE_DEVICES=7 ns-eval --load-config outputs/gsplat_offset_0m/splatfacto/2024-06-04_173618/config.yml --output-path ./gsplat_offset_0m/result.json --render-output-path ./gsplat_offset_0m

cd carla_pic_0603_Town04_cam3
CUDA_VISIBLE_DEVICES=5 ns-train splatfacto --experiment-name gsplat_offset_0m colmap --eval-mode filename  --data ./ --downscale-factor 1
CUDA_VISIBLE_DEVICES=7 ns-eval --load-config outputs/gsplat_offset_0m/splatfacto/2024-06-04_174532/config.yml --output-path ./gsplat_offset_0m/result.json --render-output-path ./gsplat_offset_0m

cd carla_pic_0603_Town05_cam3
CUDA_VISIBLE_DEVICES=3 ns-train splatfacto --experiment-name gsplat_offset_0m colmap --eval-mode filename  --data ./ --downscale-factor 1
CUDA_VISIBLE_DEVICES=1 ns-eval --load-config outputs/gsplat_offset_0m/splatfacto/2024-06-04_174638/config.yml --output-path ./gsplat_offset_0m/result.json --render-output-path ./gsplat_offset_0m

cd carla_pic_0603_Town10_cam3
CUDA_VISIBLE_DEVICES=3 ns-train splatfacto --experiment-name gsplat_offset_0m colmap --eval-mode filename  --data ./ --downscale-factor 1
CUDA_VISIBLE_DEVICES=4 ns-eval --load-config outputs/gsplat_offset_0m/splatfacto/2024-06-04_184924/config.yml --output-path ./gsplat_offset_0m/result.json --render-output-path ./gsplat_offset_0m


cd carla_pic_0603_Town01_cam3
CUDA_VISIBLE_DEVICES=1 ns-train splatfacto --experiment-name gsplat_offset_0m colmap --eval-mode filename  --data ./ --downscale-factor 1
CUDA_VISIBLE_DEVICES=1 ns-eval --load-config outputs/gsplat_offset_0m/splatfacto/2024-06-04_222959/config.yml  --output-path ./gsplat_offset_0m/result.json --render-output-path ./gsplat_offset_0m
CUDA_VISIBLE_DEVICES=1 ns-eval --load-config outputs/gsplat_offset_0m/splatfacto/2024-06-04_222959/config.yml  --output-path ./gsplat_offset_1m/result.json --render-output-path ./gsplat_offset_1m


cd carla_pic_0603_Town02_cam3
CUDA_VISIBLE_DEVICES=2 ns-train splatfacto --experiment-name gsplat_offset_0m colmap --eval-mode filename  --data ./ --downscale-factor 1
CUDA_VISIBLE_DEVICES=2 ns-eval --load-config outputs/gsplat_offset_0m/splatfacto/2024-06-04_223007/config.yml  --output-path ./gsplat_offset_0m/result.json --render-output-path ./gsplat_offset_0m
CUDA_VISIBLE_DEVICES=2 ns-eval --load-config outputs/gsplat_offset_0m/splatfacto/2024-06-04_223007/config.yml  --output-path ./gsplat_offset_1m/result.json --render-output-path ./gsplat_offset_1m


cd carla_pic_0603_Town03_cam3
CUDA_VISIBLE_DEVICES=3 ns-train splatfacto --experiment-name gsplat_offset_0m colmap --eval-mode filename  --data ./ --downscale-factor 1
CUDA_VISIBLE_DEVICES=6 ns-eval --load-config outputs/gsplat_offset_0m/splatfacto/2024-06-04_223017/config.yml  --output-path ./gsplat_offset_0m/result.json --render-output-path ./gsplat_offset_0m


cd carla_pic_0603_Town04_cam3
CUDA_VISIBLE_DEVICES=4 ns-train splatfacto --experiment-name gsplat_offset_0m colmap --eval-mode filename  --data ./ --downscale-factor 1
CUDA_VISIBLE_DEVICES=7 ns-eval --load-config outputs/gsplat_offset_0m/splatfacto/2024-06-04_223026/config.yml  --output-path ./gsplat_offset_0m/result.json --render-output-path ./gsplat_offset_0m


cd carla_pic_0603_Town05_cam3
CUDA_VISIBLE_DEVICES=5 ns-train splatfacto --experiment-name gsplat_offset_0m colmap --eval-mode filename  --data ./ --downscale-factor 1
CUDA_VISIBLE_DEVICES=4 ns-eval --load-config outputs/gsplat_offset_0m/splatfacto/2024-06-04_223034/config.yml  --output-path ./gsplat_offset_0m/result.json --render-output-path ./gsplat_offset_0m


cd carla_pic_0603_Town10_cam3
CUDA_VISIBLE_DEVICES=6 ns-train splatfacto --experiment-name gsplat_offset_0m colmap --eval-mode filename  --data ./ --downscale-factor 1
CUDA_VISIBLE_DEVICES=4 ns-eval --load-config outputs/gsplat_offset_0m/splatfacto/2024-06-04_223044/config.yml  --output-path ./gsplat_offset_0m/result.json --render-output-path ./gsplat_offset_0m