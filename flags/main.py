import os
import json

def get_images_paths():
    path = os.path.join(os.getcwd(),'flags_images')
    paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            paths.append(os.path.join(path,file))
        break
    return paths

def load_json(path):
    try:
        with open(path,'r') as f:
            return json.load(f)
    except Exception as e:
        return {os.path.basename(name[:name.find('.')]):False for name in get_images_paths()}

def save_json(path,data):
    with open(path,'w') as f:
        json.dump(data,f)

if __name__ == '__main__':
    cwd = os.getcwd()
    data = load_json(os.path.join(cwd,'used.json'))
    print(data)