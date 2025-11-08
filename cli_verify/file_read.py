##########################################################################################
# Functionality:
#   -Opens command file in read mode
#   -Reads all “command value” lines into a list
#   -Splits each line into command and value
#   -Writes a JSON file(response.json) of {command: value} pairs for later verification
###############################################################################################
from pathlib import Path
import json

def file_read(path: Path)->list:
    '''
    Reads *.txt command file and creates list and dic
    '''
    cmd_list = []
    cmd_dict = {}


    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            
            if not line or line.startswith("#"):
                continue

            cmd_list.append(line)

            parts = line.split()
            if len(parts) == 2:
                key, val = parts
                cmd_dict[key] = val

    '''write into json file'''
    json_path = path.with_suffix(".json")
    with open(json_path, "w") as f:
        json.dump(cmd_dict, f, indent=2)

    print("cmd_list:", cmd_list)
    print("cmd_dict:", cmd_dict)
   
    return cmd_list


def main():
    path = Path("D:/python/pytest/python_exercises/command.txt")
    file_read(path)

if __name__ == "__main__":
    main()
    
