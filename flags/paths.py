import os
from src.json_data import get_images_paths

cwd = os.getcwd()
dir_name = 'flags'

flags_path = os.path.join(cwd,dir_name,'flags_images')
json_path = os.path.join(cwd,dir_name,'used.json')
images_path = get_images_paths(flags_path)