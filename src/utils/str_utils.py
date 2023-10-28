import json
from pathlib import Path
import subprocess

def json_acceptable_string(string: str):
    json_acceptable_string = string.replace("'", "\"")
    data = json.loads(json_acceptable_string)
    return data

def get_current_path():
    current_path = Path().absolute()
    return current_path

def remove_list_dups(_list):
    res = [*set(_list)]
    return res

def splitAction_getName(selected_option):
    split_name = str(selected_option).split('_')
    _name = split_name[-1]
    return _name

def add_letter(string, target_length, letter):
  # Check the length of the string
  if len(string) < target_length:
    # Add the letter to the beginning of the string
    string = letter + string
  return string

def stop_mediTracker_service(service_name):
    command = "sudo systemctl stop {}".format(service_name)
    subprocess.run(command.split())
    
def start_mediTracker_service(service_name):
    command = "sudo systemctl start {}".format(service_name)
    subprocess.run(command.split())