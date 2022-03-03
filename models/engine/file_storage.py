#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json

from sqlalchemy import delete


class FileStorage:
    """Class manages storage of HBNB models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of the models currently in storage"""
        if cls != None:
            class_objects = {}
            for item in FileStorage.__objects:
                if type(self.__objects[item]) == cls:
                    class_objects[item] = self.__objects[item]
            return class_objects
        else:
            return FileStorage.__objects

    def new(self, obj):
        """Adds a new object to the storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves the storage dictionary to a file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from a file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                        self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes an object from __objects if argument matches a valid
        instance.
        """
        if obj == None:
            return
        elif obj in self.__objects.values():
            objk = obj.__class__.__name__ + "." + obj.id
            self.__objects.pop(objk, None)
