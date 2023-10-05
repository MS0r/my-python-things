import sys
import clipboard
import json

SAVED_DATA = 'clipboard.json'


def save_data(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f)


def load_data(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except:
        return {}


def main(command):
    data = load_data(SAVED_DATA)

    if command == 'save':
        key = input("Insert a key to save clipboard: ")
        data[key] = clipboard.paste()
        save_data(SAVED_DATA, data)
    elif command == 'load':
        key = input("Insert a key to get saved clipboard: ")
        if key in data:
            clipboard.copy(data[key])
            print('data copied')
        else:
            print('key not found')
    elif command == 'list':
        print(data)
    else:
        print('Unknown command')


if __name__ == '__main__':
    args = sys.argv

    if len(args) != 2:
        raise Exception("You must pass one argument")

    main(args[1])
