# https://www.geeksforgeeks.org/reflection-in-python/
import builtins
import json
import types
import inspect

import pygame
from pygeon.core.misc.GameObject import GameObject
from pygeon.core.misc.GameObjectManager import GameObjectManager


class Serializer:
    """A helper for custom serialization with reflections

    ...

    Methods
    -------
    __create_string_representation(data=Any)
        Creates a string representation of the given object
    __create_attribute_string_representation(attribute=str, referenced_object=Any)
        Creates a string representation of the attribute and for the elements in the attribute
    __get_valid_attributes(any_object=Any)
        Iterates through all attributes and returns the ones viable for serialization
    __serialize_intern(any_object=Any)
        Creates the string representation of an object
        Used to serialize objects inside of the object which is serialized
    serialize(any_object=Any)
        Creates the string representation of the given object
    create_object_from_representation(data_array=list)
        Creates the object from the given data
    """

    def __init__(self):
        self.__default_supported = [bool, int, str, float]

    def __create_string_representation(self, data):
        """Creates a string representation of the given object

        Parameters
        ----------
        data : Any
            The object/attribute which will be serialized

        Returns
        -------
        str
            The data as a string
        """

        # If the data can be serialized by default, do so
        if self.__default_supported.__contains__(type(data)):
            return json.dumps(data)
        else:
            # If the data is a custom class it has to be serialized with all of its own attributes
            if inspect.isclass(type(data)):
                return json.dumps(["@"+str(type(data))+"@" + str(self.__serialize_intern(data))])
            return "not_supported"

    def __create_attribute_string_representation(self, attribute, referenced_object):
        """Creates a string representation of the attribute and for the elements in the attribute

        Parameters
        ----------
        attribute : str
            The attribute which will be represented
        referenced_object : Any
            The object which has the attribute

        Returns
        -------
        str
            The attribute represented as a string
        """

        # Use normal json if the attribute type is supported by default
        if self.__default_supported.__contains__(type(referenced_object.__getattribute__(attribute))):
            return json.dumps(referenced_object.__getattribute__(attribute))
        if type(referenced_object.__getattribute__(attribute)) is list:  # Different serialization of lists
            attribute_representation = []
            for data in referenced_object.__getattribute__(attribute):  # All elements of the list will be serialized
                # Will recursively serialize the element if it is an object with own attributes
                attribute_representation.append(self.__create_string_representation(data))
            return json.dumps(attribute_representation)
        # pygame.Vector is not supported by json, so the serialization string will be custom
        if type(referenced_object.__getattribute__(attribute)) is pygame.math.Vector2:
            vector = referenced_object.__getattribute__(attribute)
            return json.dumps("@VECTOR@" + str(vector.x) + "#" + str(vector.y) + "@")

    def __get_valid_attributes(self, any_object):
        """Iterates through all attributes and returns the ones viable for serialization

        Parameters
        ----------
        any_object : Any
            The object which will be serialized
        Returns
        -------
        list : str
            A list of attributes which are required for serialization
        """

        relevant = []
        for attr in dir(any_object):  # Get all attributes of the object
            if attr.endswith("__") and attr.startswith("__"):  # Ignore builtins
                continue
            if attr.__contains__("__attributes"):  # List of all of the objects attributes, only used for deserializing
                continue
            if callable(any_object.__getattribute__(attr)):  # Ignore methods
                continue
            relevant.append(attr)
        return relevant

    def serialize(self, any_object):
        """Creates the string representation of the given object

        Parameters
        ----------
        any_object : Any
            The object which will be serialized
        Returns
        -------
        str
            The serialized object as a string
        """

        attributes_data = []
        # Serialized all attributes
        for attr in self.__get_valid_attributes(any_object):
            attributes_data.append(self.__create_attribute_string_representation(attr, any_object))
        return json.dumps([str(type(any_object)), attributes_data])

    def __serialize_intern(self, any_object):
        """Creates the string representation of an object

        Used to serialize objects inside of the object which is serialized

        Parameters
        ----------
        any_object : Any
            The object to serialize
        Returns
        -------
        str
            The serialized object
        """

        attributes_data = []
        # Iterates over all valid attributes
        for attr in self.__get_valid_attributes(any_object):
            # Creates the data string
            attributes_data.append(self.__create_attribute_string_representation(attr, any_object))
        return [str(type(any_object)), attributes_data]

    # Creates the object from the given data
    # TODO Not finished
    def create_object_from_representation(self, data_array):
        object_attr_list = json.loads(data_array)
        class_type = object_attr_list[0]  # str
        object_attr_list[1].reverse()  # Attributes are in wrongly sorted
        for a in object_attr_list[1]:
            a = a.replace("\"", "")  # Data is still a 'string'
            if a.startswith("@") and a.endswith("@"):  # Custom data
                custom_type = a.split("@")[1]
                custom_data = a.split("@")[2]

                if custom_type == "VECTOR":
                    pass

"""
ser = Serializer()
GameObject(pygame.Vector2(0, 1), "NAME1", True)
GameObject(pygame.Vector2(1, 0), "NAME2", True)
data = []
for obj in GameObjectManager().game_objects:
    data.append(ser.serialize(obj))
json_data = json.dumps(json.dumps(data))
n_data = json.loads(json.loads(json_data))
for e in n_data:
    ser.create_object_from_representation(e)
"""