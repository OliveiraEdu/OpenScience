import json
import os
from ipfs_functions import upload_json_to_ipfs, download_json_from_ipfs, upload_file_to_ipfs

def extract_file_name(obj):
    global file_names
    if 'file_name' in obj:  # Check if the object has a 'file_name' key
        file_names.append(obj['file_name'])  # Extract the value of that key

def get_object(objs):
    global objects_list
    for obj in objs:
        extract_file_name(obj)  # Call the function to extract the file name
        if isinstance(obj, dict):  # Check if the object is a dictionary (JSON object)
            objects_list.append(obj)