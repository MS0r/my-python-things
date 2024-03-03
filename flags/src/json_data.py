import os
import json

def get_images_paths(flags_path):
    paths = []
    for root, dirs, files in os.walk(flags_path):
        for file in files:
            paths.append(os.path.join(flags_path,file))
        break
    return paths

def load_json(path,images_path):
    try:
        with open(path,'r') as f:
            return json.load(f)
    except Exception as e:
        return {os.path.basename(name[:name.find('.')]):False for name in images_path}

def save_json(path,data):
    with open(path,'w') as f:
        json.dump(data,f)

# if __name__ == '__main__':
#     cwd = os.getcwd()
#     data = load_json(os.path.join(cwd,'used.json'))
#     print(data)