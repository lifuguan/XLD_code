import os



def rename_files(directory):
    for filename in os.listdir(directory):
        os.rename(os.path.join(directory, filename), os.path.join(directory, "eval_"+filename))

def rename_scenes(directory):
    # test_pic
    
    test_pic_dir = os.path.join(directory, "test_pic")
    for test_sub_dir in os.listdir(test_pic_dir):
        test_sub_dir = os.path.join(test_pic_dir, test_sub_dir)
        for filename in os.listdir(test_sub_dir):
            if os.path.exists(os.path.join(test_sub_dir, "eval_"+filename)):
                print("This folder already has eval file.")
                return
            print(os.path.join(test_sub_dir, "eval_"+filename))
            os.rename(os.path.join(test_sub_dir, filename), os.path.join(test_sub_dir, "eval_"+filename))

    # train_pic
    train_pic_dir = os.path.join(directory, "train_pic")
    for train_sub_dir in os.listdir(train_pic_dir):
        if os.path.exists(os.path.join(train_pic_dir, "train_"+train_sub_dir)):
            print("This folder already has train file.")
            return
        os.rename(os.path.join(train_pic_dir, train_sub_dir), os.path.join(train_pic_dir, "train_"+train_sub_dir))

if __name__ == '__main__':
    rename_scenes("data/carla_pic_0603_Town01")
    rename_scenes("data/carla_pic_0603_Town02")
    rename_scenes("data/carla_pic_0603_Town03")
    rename_scenes("data/carla_pic_0603_Town04")
    rename_scenes("data/carla_pic_0603_Town05")
    rename_scenes("data/carla_pic_0603_Town10")