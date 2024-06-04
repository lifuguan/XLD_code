import numpy as np
import os, shutils, json
from plyfile import PlyData, PlyElement
from scipy.spatial.transform import Rotation as R


def pose_unreal2opengl(c2w_mat):

    translation = c2w_mat[:3, 3]
    rot = R.from_matrix(c2w_mat[:3, :3])
    rot_vec = rot.as_rotvec()

    rot_vec_new = rot_vec[[1, 2, 0]]
    rot_vec_new[0] *= -1
    rot_vec_new[2] *= -1

    rot = R.from_rotvec(rot_vec_new)

    
    translation_new = translation[[1, 2, 0]]
    translation_new[1] *= -1

    c2w_mat = np.eye(4)
    c2w_mat[:3, :3] = rot.as_matrix()
    c2w_mat[:3, 3] = translation_new

    rot = np.eye(4)
    rot[1,1]=-1
    rot[2, 2] = -1
    c2w_mat = c2w_mat @ rot
    return c2w_mat

# 读取PLY文件
def read_ply(file_path):
    with open(file_path, 'rb') as f:
        plydata = PlyData.read(f)
    vertex_data = plydata['vertex']
    points = np.vstack([vertex_data['x'], vertex_data['y'], vertex_data['z']]).T
    return points

# 将点云应用于位姿
def transform_point_cloud(points, pose):
    transformed_points = np.hstack([points, np.ones((points.shape[0], 1))])
    transformed_points = np.dot(transformed_points, pose[:3, :].T)
    return transformed_points[:, :3]

# 合并点云
def merge_point_clouds(point_clouds):
    merged_cloud = np.vstack(point_clouds)
    return merged_cloud

# 保存PLY文件
def save_ply(xyz, file_path):
    if 'txt' in file_path:
        rgb = np.random.randint(0, 255, size=(xyz.shape[0], 3))
        with open(file_path, 'w') as f:
            for i in range(len(xyz)):
                f.write(f"{int(i)} {xyz[i][0]} {xyz[i][1]} {xyz[i][2]} {rgb[i][0]} {rgb[i][1]} {rgb[i][2]}\n")
    else:
        # Define the dtype for the structured array
        dtype = [('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
                ('nx', 'f4'), ('ny', 'f4'), ('nz', 'f4'),
                ('red', 'u1'), ('green', 'u1'), ('blue', 'u1')]
        
        normals = np.zeros_like(xyz)
        rgb = np.random.random((xyz.shape[0], 3))
        elements = np.empty(xyz.shape[0], dtype=dtype)
        attributes = np.concatenate((xyz, normals, rgb), axis=1)
        elements[:] = list(map(tuple, attributes))

        # Create the PlyData object and write to file
        el = PlyElement.describe(elements, 'vertex')
        PlyData([el]).write(file_path)



def generate_point_cloud_text(scene_path):
    start_timestep, end_timestep = 5, 155
    point_cloud_files = []
    poses = [] 
    for t in range(start_timestep, end_timestep):
        with open(os.path.join(scene_path, "train_pic", f"train_camera_extrinsics_{t:06d}.json"), 'r') as file:
            ego_to_world_current = np.array(json.load(file)['transform_matrix'])
            lidar_to_world = pose_unreal2opengl(ego_to_world_current)
            # lidar_to_world = ego_to_world_current
        lidar_file = os.path.join(scene_path, "train_pic", f"train_lidar_{t:05d}.ply")
        poses.append(lidar_to_world)
        point_cloud_files.append(lidar_file)

    # 读取并转换点云
    point_clouds = []
    for file, pose in zip(point_cloud_files, poses):
        points = read_ply(file)
        opengl_point_cloud = points.copy()
        opengl_point_cloud[:, 0] = points[:, 0]
        opengl_point_cloud[:, 1] = points[:, 2]
        opengl_point_cloud[:, 2] = points[:, 1]
        transformed_points = transform_point_cloud(opengl_point_cloud, pose)
        point_clouds.append(transformed_points)

    # 合并点云
    merged_cloud = merge_point_clouds(point_clouds)
    # 保存合并后的点云
    save_ply(merged_cloud, f'{scene_path.split("/")[-1]+"_cam1"}/merged_cloud.txt')
    save_ply(merged_cloud, f'{scene_path.split("/")[-1]+"_cam3"}/merged_cloud.txt')

generate_point_cloud_text('data/carla_pic_0603_Town01')
print("Done processing carla_pic_0603_Town01.")
generate_point_cloud_text('data/carla_pic_0603_Town02')
print("Done processing carla_pic_0603_Town02.")
generate_point_cloud_text('data/carla_pic_0603_Town03')
print("Done processing carla_pic_0603_Town03.")
generate_point_cloud_text('data/carla_pic_0603_Town04')
print("Done processing carla_pic_0603_Town04.")
generate_point_cloud_text('data/carla_pic_0603_Town05')
print("Done processing carla_pic_0603_Town05.")
generate_point_cloud_text('data/carla_pic_0603_Town10')
print("Done processing carla_pic_0603_Town10.")
