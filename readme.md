# Code Release of "XLD: A Cross-Lane Dataset for Benchmarking Novel Driving View Synthesis"
Hao Li, Ming Yuan, Yan Zhang, Chenming Wu, Chen Zhao, Chunyu Song, Haocheng Feng, Errui Ding, Dingwen Zhang, Jingdong Wang
![Teaser image](assets/teaser.jpg)
## [Project page](https://3d-aigc.github.io/XLD/) | [Paper](https://arxiv.org/abs/2406.18360) | [Data](https://1drv.ms/f/s!Amx_1zEBrKfJg94-bGzJe1PaU8IU6Q?e=uVaFmg)

This repository contains the official authors data preprocess tools for NeRFStudio and Gaussian Splatting methods.

### Data Preprocess
1. Unzip the compressed files (e.g. `carla_pic_0603_Town**.zip`).
2. Download `intrinscis.zip` and `extrinsics.zip` from data link and unzip them. 
3. Then move `intrinscis` and `extrinsics` to the corresponding folder.
```
cp -r intrinsics data/carla_pic_0603_Town01
cp -r extrinsics data/carla_pic_0603_Town01
cp -r intrinsics data/carla_pic_0603_Town02
cp -r extrinsics data/carla_pic_0603_Town02
cp -r intrinsics data/carla_pic_0603_Town03
cp -r extrinsics data/carla_pic_0603_Town03
cp -r intrinsics data/carla_pic_0603_Town04
cp -r extrinsics data/carla_pic_0603_Town04
cp -r intrinsics data/carla_pic_0603_Town05
cp -r extrinsics data/carla_pic_0603_Town05
cp -r intrinsics data/carla_pic_0603_Town10
cp -r extrinsics data/carla_pic_0603_Town10
```
The data tree should look like this:
```
generate_offset_0_test.py
rename.py
convert_XLD_transforms.py
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
Generate test set in 0m offset.
```bash
python generate_offset_0_test.py
```
Rename train images to `train_**` and test images to `eval_**` as the format of NeRFStudio.
```bash
python rename.py
```
Generate `transforms.json` for NeRF and 3D-GS.
```bash
python convert_XLD_transforms.py
```
Notably, change the arguments `num_cams` and `camera_list` for different camera settings, `offset_meters` for different offset settings.
```python
###### multi cameras, offsets=1m     ######
generate_json_file(scene_path = 'data/carla_pic_0603_Town10', num_cams=3, camera_list=[1,0,2], offset_meters=1)
###### front-only camera, offsets=1m ######
generate_json_file(scene_path = 'data/carla_pic_0603_Town10', num_cams=1, camera_list=[0], offset_meters=1)
```
## Model Training
### UC-NeRF training
We provide a modified version of UC-NeRF to train on the XLD dataset flexibly.

Please refer to the `readme.md` of the modified UC-NeRF on this [page](https://github.com/lifuguan/UC-NeRF).

### EmerNeRF training
We provide a modified version of EmerNeRF to train on the XLD dataset flexibly.

Please refer to the `readme.md` of the modified EmerNeRF on this [page](https://github.com/lifuguan/EmerNeRF).

### NeRFacto training
```bash
cd carla_pic_0603_Town01_cam1
#### train #####
CUDA_VISIBLE_DEVICES=1 ns-train nerfacto --pipeline.model.camera-optimizer.mode off --experiment-name nerfacto_offset_1m nerfstudio-data --eval-mode filename  --data ./
#### eval #####
CUDA_VISIBLE_DEVICES=2 ns-eval --load-config outputs/nerfacto_offset_1m/nerfacto/2024-06-06_145158/config.yml    --output-path ./nerfacto_offset_1/result.json --render-output-path ./nerfacto_offset_1
```
### Instant-NGP training
```bash
cd carla_pic_0603_Town01_cam1
#### train #####
CUDA_VISIBLE_DEVICES=0 ns-train instant-ngp --experiment-name instant_ngp_offset_1 nerfstudio-data --eval-mode filename  --data ./
#### eval #####
CUDA_VISIBLE_DEVICES=0 ns-eval --load-config outputs/instant_ngp_offset_1/instant-ngp/2024-06-06_165753/config.yml     --output-path ./instant-ngp_offset_1m/result.json --render-output-path ./instant-ngp_offset_1m
```

### Gaussian methods training
#### Colmap-format data proprocessing
Run python scripts to transforms.json to 3D-GS format.
```bash
python convert_XLD_transforms.py.  # generate transforms.json
python merge_lidar.py              # merge 3D LiDAR point cloud as initialization 
python transform2colmap.py         # transform transforms.json to colmap format
```
create a `images` folder and link the train and test images into it.
```bash
mkdir -p carla_pic_0603_Town01_cam3/images
cd carla_pic_0603_Town01_cam3/images 
ln -s ../../data/carla_pic_0603_Town01/train_pic/train_camera0_00* ./ && ln -s ../../data/carla_pic_0603_Town01/train_pic/train_camera1_00* ./
ln -s ../../data/carla_pic_0603_Town01/train_pic/train_camera2_00* ./ && ln -s ../../data/carla_pic_0603_Town01/test_pic/offset_left_0m/eval_camera0_00* ./
cd ../../
```

#### GaussianPro & 3D-GS training
```bash
cd carla_pic_0603_Town01_cam1
CUDA_VISIBLE_DEVICES=0 python train.py -s carla_pic_0603_Town01_cam1 -m ./carla_pic_0603_Town01_cam1/output --position_lr_init 0.000016 --scaling_lr 0.001 --percent_dense 0.0005 --port 1021 --eval
```

## Acknowledgement
The authors would like to thank [Yuanyuan Gao](https://github.com/gyy456) and [Jingfeng Li](https://github.com/Li-jingfeng) for preparing the experiments.

## Citation
```bibtex
@article{li2024xld,
    title={XLD: A Cross-Lane Dataset for Benchmarking Novel Driving View Synthesis},
    author={Hao Li and Ming Yuan and Yan Zhang and Chenming Wu and Chen Zhao and Chunyu Song and Haocheng Feng and Errui Ding and Dingwen Zhang and Jingdong Wang},
    journal={arXiv},
    year={2024}
}
```
