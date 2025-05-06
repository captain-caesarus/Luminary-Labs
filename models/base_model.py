#!/usr/bin/python3
""" Defines the BaseModel class."""


import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """ Defines all common attributes/methods for other classes."""

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance with Unique ID and timestamps.
        or recreates one from a dictionary.
        """

        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                if key in ("created_at", "updated_at"):
                    setattr(self, key, datetime.fromisoformat(value))
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            storage.new(self)

    def __str__(self):
        """
        Return string representation of the instance.

        Format: [<class name>] (<self.id>) <self.__dict__>
        """

        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """ Update the string representation of the instance. """

        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """
        Return a dictionary representation of the instance.

        Includes __class__ and ISO-formatted datetime strings.
        """

        dict_repr = self.__dict__.copy()
        dict_repr["__class__"] = self.__class__.__name__
        dict_repr["created_at"] = self.created_at.isoformat()
        dict_repr["updated_at"] = self.updated_at.isoformat()

        return dict_repr
