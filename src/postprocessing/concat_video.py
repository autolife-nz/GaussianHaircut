# import os
# import glob
# import shutil
# from argparse import ArgumentParser
# import numpy as np
# import torch
# import pickle as pkl
# from plyfile import PlyData, PlyElement
# from scipy.spatial.transform import Rotation, RotationSpline
# import numpy
# from PIL import Image, ImageOps
# from pytorch3d.io import load_obj, save_ply
# import cv2
# from torchvision.transforms import Resize, CenterCrop, InterpolationMode
# from tqdm import tqdm
# import shutil



# def main(input_path, exp_name_3):
#     os.makedirs(f'{input_path}/curves_reconstruction/{exp_name_3}/raw_frames', exist_ok=True)
#     os.system(f'ffmpeg -i {input_path}/raw.mp4 -qscale:v 2 {input_path}/curves_reconstruction/{exp_name_3}/raw_frames/%06d.jpg')
#     os.makedirs(f'{input_path}/curves_reconstruction/{exp_name_3}/frames', exist_ok=True)
#     img_names = sorted(os.listdir(f'{input_path}/curves_reconstruction/{exp_name_3}/train/ours_30000/renders'))
#     print(len(img_names))
#     for i, img_name in tqdm(enumerate(img_names)):
#         img_basename = img_name.split('.')[0]
#         render_3dgs = Image.open(f'{input_path}/curves_reconstruction/{exp_name_3}/train/ours_30000/renders/{img_basename}.png').convert('RGB')
#         render_blender = Image.open(f'{input_path}/curves_reconstruction/{exp_name_3}/blender/results/{img_basename}.png')
#         render_blender_new = Image.new("RGBA", render_blender.size, "WHITE")
#         render_blender_new.paste(render_blender, (0, 0), render_blender)
#         render_blender = render_blender_new.convert('RGB')
#         gt = Image.open(f'{input_path}/curves_reconstruction/{exp_name_3}/raw_frames/%06d.jpg' % (int(img_basename) - 1)).convert('RGB')
#         w, h = render_3dgs.size
#         render_blender_resized = Resize(h, interpolation=InterpolationMode.BICUBIC)(render_blender)
#         render_blender_cropped_resized = CenterCrop((h, w))(render_blender_resized)
#         gt_resized = Resize(w, interpolation=InterpolationMode.BICUBIC)(gt)
#         frame = Image.fromarray(np.concatenate([np.asarray(gt_resized), np.asarray(render_blender_cropped_resized), np.asarray(render_3dgs)], axis=1))
#         frame_resized = Resize(720, interpolation=InterpolationMode.BICUBIC)(frame)
#         frame_resized.save(f'{input_path}/curves_reconstruction/{exp_name_3}/frames/%06d.png' % i)
#     os.system(f'ffmpeg -r 30 -i "{input_path}/curves_reconstruction/{exp_name_3}/frames/%06d.png" -c:v libx264 -vb 20M {input_path}/curves_reconstruction/{exp_name_3}/vis.mp4')
    
#     # Cleanup
#     shutil.rmtree(f'{input_path}/curves_reconstruction/{exp_name_3}/frames')
#     shutil.rmtree(f'{input_path}/curves_reconstruction/{exp_name_3}/raw_frames')

# if __name__ == "__main__":
#     parser = ArgumentParser(conflict_handler='resolve')

#     parser.add_argument('--input_path', default='/home/ezakharov/Datasets/hair_reconstruction/NeuralHaircut/jenya', type=str)
#     parser.add_argument('--exp_name_3', default='stage3_lor=0.1', type=str)

#     args, _ = parser.parse_known_args()

#     main(args.input_path, args.exp_name_3)

import os
import shutil
from argparse import ArgumentParser
import numpy as np
from PIL import Image
from torchvision.transforms import Resize, CenterCrop, InterpolationMode
from tqdm import tqdm

def main(input_path, exp_name_3):
    # Create directories for raw frames and processed frames
    raw_frames_dir = f'{input_path}/curves_reconstruction/{exp_name_3}/raw_frames'
    frames_dir = f'{input_path}/curves_reconstruction/{exp_name_3}/frames'
    
    os.makedirs(raw_frames_dir, exist_ok=True)
    os.makedirs(frames_dir, exist_ok=True)
    
    # Extract frames from the raw video
    ffmpeg_cmd = f'ffmpeg -i {input_path}/raw.mp4 -qscale:v 2 {raw_frames_dir}/%06d.jpg'
    print(f"Running ffmpeg command: {ffmpeg_cmd}")
    os.system(ffmpeg_cmd)
    
    # Check if frames were extracted
    if not os.listdir(raw_frames_dir):
        raise FileNotFoundError(f"No frames extracted to {raw_frames_dir}. Check your input video or ffmpeg command.")
    
    # List render images
    renders_dir = f'{input_path}/curves_reconstruction/{exp_name_3}/train/ours_30000/renders'
    blender_dir = f'{input_path}/curves_reconstruction/{exp_name_3}/blender/results'
    img_names = sorted(os.listdir(renders_dir))
    
    if not img_names:
        raise FileNotFoundError(f"No images found in {renders_dir}. Ensure the renders directory is populated.")
    
    print(f"Found {len(img_names)} render images to process.")
    
    # Process each render image
    for i, img_name in tqdm(enumerate(img_names), total=len(img_names)):
        img_basename = img_name.split('.')[0]
        
        # Paths for input files
        render_3dgs_path = os.path.join(renders_dir, f"{img_basename}.png")
        render_blender_path = os.path.join(blender_dir, f"{img_basename}.png")
        raw_frame_path = os.path.join(raw_frames_dir, f"{int(img_basename) - 1:06d}.jpg")
        
        # Check for file existence
        if not os.path.exists(render_3dgs_path):
            print(f"Warning: Missing render 3DGS file: {render_3dgs_path}")
            continue
        if not os.path.exists(render_blender_path):
            print(f"Warning: Missing Blender render file: {render_blender_path}")
            continue
        if not os.path.exists(raw_frame_path):
            print(f"Warning: Missing raw frame: {raw_frame_path}")
            continue
        
        # Open and process images
        render_3dgs = Image.open(render_3dgs_path).convert('RGB')
        render_blender = Image.open(render_blender_path)
        render_blender_new = Image.new("RGBA", render_blender.size, "WHITE")
        render_blender_new.paste(render_blender, (0, 0), render_blender)
        render_blender = render_blender_new.convert('RGB')
        gt = Image.open(raw_frame_path).convert('RGB')
        
        # Resize and concatenate images
        w, h = render_3dgs.size
        render_blender_resized = Resize(h, interpolation=InterpolationMode.BICUBIC)(render_blender)
        render_blender_cropped_resized = CenterCrop((h, w))(render_blender_resized)
        gt_resized = Resize(w, interpolation=InterpolationMode.BICUBIC)(gt)
        frame = Image.fromarray(np.concatenate([np.asarray(gt_resized), np.asarray(render_blender_cropped_resized), np.asarray(render_3dgs)], axis=1))
        frame_resized = Resize(720, interpolation=InterpolationMode.BICUBIC)(frame)
        frame_resized.save(f"{frames_dir}/{i:06d}.png")
    
    # Generate video from processed frames
    vis_video_path = f'{input_path}/curves_reconstruction/{exp_name_3}/vis.mp4'
    ffmpeg_video_cmd = f'ffmpeg -r 30 -i "{frames_dir}/%06d.png" -c:v libx264 -vb 20M {vis_video_path}'
    print(f"Creating video: {ffmpeg_video_cmd}")
    os.system(ffmpeg_video_cmd)
    
    # Cleanup
    print(f"Cleaning up temporary directories...")
    shutil.rmtree(frames_dir)
    shutil.rmtree(raw_frames_dir)
    print("Processing completed successfully.")

if __name__ == "__main__":
    parser = ArgumentParser(conflict_handler='resolve')
    parser.add_argument('--input_path', default='/home/ezakharov/Datasets/hair_reconstruction/NeuralHaircut/jenya', type=str)
    parser.add_argument('--exp_name_3', default='stage3_lor=0.1', type=str)
    args, _ = parser.parse_known_args()
    main(args.input_path, args.exp_name_3)
