#!/usr/bin/python3
"""
FileStorage class that serializes instances to a JSON file and deserializes a
JSON file to instances.
"""


import json
import os


class FileStorage:
    """
    Represents an abstacted storage engine.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.

    """

    __file_path = "models/engine/storage/file.json"
    __objects = {}


    def all(self):
        """
        Returns the dictionary __objects.
        """

        return FileStorage.__objects


    def new(self, obj):
        """
        Set in __objects obj with key <obj_class_name>.id
        """

        obj_name = obj.__class__.__name__
        key = f"{obj_name}.{obj.id}"
        FileStorage.__objects[key] = obj


    def save(self):
        """
        Serializes __objects to the JSON file __file_path.
        """
        os.makedirs(os.path.dirname(FileStorage.__file_path), exist_ok=True)

        obj_dict_to_save = {
            key: obj.to_dict()
            for key, obj in FileStorage.__objects.items()
        }

        with open(FileStorage.__file_path, "w") as f:
            json.dump(obj_dict_to_save, f)

    def reload(self):
        """
        Deserializes the JSON file to __objects, if it exists.
        """

        if not os.path.isfile(FileStorage.__file_path):
            return

        try:
            with open(FileStorage.__file_path, "r") as f:
                obj_dict_read = json.load(f)

                for key, val in obj_dict_read.items():
                    class_name = val.get("__class__")
                    del val["__class__"]
                    
                    self.new(eval(class_name)(**val))
       
        except Exception as e:
            print(f"Error loading from file: {e}")
