#
# Autolife
# Author Hemy Gulati 22/12/2024
#

import argparse
import os
import shutil

def replace_mesh_final(data_path, flame_mesh_path):
    """
    Replaces mesh_final.obj in the specified directory with the first .obj file found in the data_path.

    Args:
      data_path: Path to the directory containing the .obj files.
      flame_mesh_path: Full path to the mesh_final.obj file to be replaced.
    """

    # Change to the data directory
    os.chdir(data_path)

    # Find the first .obj file in alphabetical order
    obj_files = [f for f in os.listdir('.') if f.endswith('.obj')]
    obj_files.sort()
    if not obj_files:
        print("No .obj files found in", data_path)
        return

    obj_file = obj_files[0]

    # Create "selected_obj" directory if it doesn't exist
    os.makedirs("selected_obj", exist_ok=True)

    # Copy the selected .obj file to the "selected_obj" directory
    shutil.copy(obj_file, os.path.join("selected_obj", obj_file))

    # Replace mesh_final.obj with the selected .obj file
    shutil.copy(os.path.join("selected_obj", obj_file), flame_mesh_path)

    print("Path:", flame_mesh_path)  # Print the path
    print("Replaced mesh_final.obj with", obj_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replace mesh_final.obj with a selected .obj file.")
    parser.add_argument("--data_path", type=str, required=True, help="Path to the directory containing the .obj files.")
    parser.add_argument("--flame_mesh_path", type=str, required=True, help="Full path to the mesh_final.obj file to be replaced.")
    args = parser.parse_args()

    replace_mesh_final(args.data_path, args.flame_mesh_path)