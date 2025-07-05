'''
Cut images to 4x4 grid

'''

from PIL import Image
import os 

def cut_image_into_4x4(image_path, output_prefix="patch", output_dir="data"):
    img = Image.open(image_path)
    width, height = img.size
    patch_width = width // 4
    patch_height = height // 4

    for i in range(4):
        for j in range(4):
            left = j * patch_width
            upper = i * patch_height
            right = (j + 1) * patch_width
            lower = (i + 1) * patch_height
            box = (left, upper, right, lower)
            patch = img.crop(box)
            patch.save(os.path.join(output_dir,f"{output_prefix}_{i}_{j}.png")) # Save patches with a naming convention

# Example usage:
input_dir = "data/images"
images = os.listdir(input_dir)
for i in images:
    data_path = os.path.join(input_dir,i)
    files = os.listdir(data_path)
    file_path = os.path.join(data_path,files[0])
    op_path = os.path.join(data_path,"patches")
    os.makedirs(op_path,exist_ok=True)
    cut_image_into_4x4(file_path,output_dir=op_path)
