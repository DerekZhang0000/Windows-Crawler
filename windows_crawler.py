import os
import json
import argparse
from colorama import Back

if __name__ == '__main__':
    NEUTRAL_COLOR = Back.BLUE
    UNAUTHORIZED_COLOR = Back.RED
    RESET_COLOR = Back.RESET

    parser = argparse.ArgumentParser(description='Windows Crawler')
    parser.add_argument('--verbose', '-v', action='store_true', help='include authorized files and folders')
    parser.add_argument('--add', '-a', action='store', help='add a directory to the list of directories to check')
    parser.add_argument('--remove', '-r', action='store', help='remove a directory from the list of directories to check')
    parser.add_argument('--update', '-u', action='store_true', help='update the list of directories to check')
    parser.add_argument('--list', '-l', action='store_true', help='list the directories to check')

    args = parser.parse_args()

    if not os.path.isfile('wc_data.json'):
        with open('wc_data.json', 'w') as wc_json:
            data_dict = {}
            default_dirs = ['C://Program Files', 'C://Program Files (x86)', 'C://Windows']
            for dir_path in default_dirs:
                data_dict[dir_path] = os.listdir(dir_path)
            json.dump(data_dict, wc_json)

    data = {}
    with open('wc_data.json', 'r') as wc_json:
        data = json.load(wc_json)

    if args.list:
        print(f"{NEUTRAL_COLOR}Directory list ({len(data)}):{RESET_COLOR}")
        for dir_path in data.keys():
            print(os.path.abspath(dir_path))
        exit(0)

    if args.add:
        dir_to_add = os.path.abspath(args.add)
        data[dir_to_add] = os.listdir(dir_to_add)
        with open('wc_data.json', 'w') as wc_json:
            json.dump(data, wc_json)
        print(f'{NEUTRAL_COLOR}{os.path.abspath(dir_to_add)} added to the list of directories{RESET_COLOR}')
        exit(0)
    
    if args.remove:
        dir_to_remove = os.path.abspath(args.remove)
        data.pop(dir_to_remove, None)
        with open('wc_data.json', 'w') as wc_json:
            json.dump(data, wc_json)
        print(f'{NEUTRAL_COLOR}{os.path.abspath(dir_to_remove)} removed from the list of directories{RESET_COLOR}')
        exit(0)

    if args.update:
        for dir_path in data.keys():
            data[dir_path] = os.listdir(dir_path)
        with open('wc_data.json', 'w') as wc_json:
            json.dump(data, wc_json)
        print(f'{NEUTRAL_COLOR}Directories updated{RESET_COLOR}')
        exit(0)

    unauthorized_found = 0
    for dir_path, files in data.items():
        for file_or_folder in os.listdir(dir_path):
            if file_or_folder not in files:
                if unauthorized_found == 0:
                    print(f'{UNAUTHORIZED_COLOR}Unauthorized files or folders:{RESET_COLOR}')
                bad_file_path = os.path.abspath(os.path.join(dir_path, file_or_folder))
                print(f'{UNAUTHORIZED_COLOR}{bad_file_path}{RESET_COLOR}')
                with open('bad_files.txt', 'a') as out_file:
                    out_file.write(bad_file_path + '\n')
                unauthorized_found += 1
            else:
                if args.verbose:
                    print(f'{os.path.abspath(os.path.join(dir_path, file_or_folder))}')
    if unauthorized_found == 0:
        print(f'{NEUTRAL_COLOR}No unauthorized files or folders found{RESET_COLOR}')
    else:
        print(f'{unauthorized_found} unauthorized files or folders found')