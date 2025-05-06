#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Unit tests for BaseModel class"""

import unittest
from models.base_model import BaseModel
from datetime import datetime
import uuid
import time
import pycodestyle


class TestBaseModel(unittest.TestCase):
    """Test cases for BaseModel"""

    def test_id_is_string_and_unique(self):
        obj1 = BaseModel()
        obj2 = BaseModel()
        self.assertIsInstance(obj1.id, str)
        self.assertNotEqual(obj1.id, obj2.id)
        uuid_obj = uuid.UUID(obj1.id)
        self.assertEqual(str(uuid_obj), obj1.id)

    def test_created_at_and_updated_at_are_datetime(self):
        obj = BaseModel()
        self.assertIsInstance(obj.created_at, datetime)
        self.assertIsInstance(obj.updated_at, datetime)
        self.assertEqual(obj.created_at, obj.updated_at)

    def test_str_method(self):
        obj = BaseModel()
        output = str(obj)
        self.assertIn(obj.__class__.__name__, output)
        self.assertIn(obj.id, output)
        self.assertIn("created_at", output)
        self.assertIn("updated_at", output)

    def test_save_method_updates_updated_at(self):
        obj = BaseModel()
        old_updated_at = obj.updated_at
        time.sleep(0.01)
        obj.save()
        self.assertNotEqual(old_updated_at, obj.updated_at)
        self.assertGreater(obj.updated_at, old_updated_at)

    def test_to_dict_contains_correct_keys_and_types(self):
        obj = BaseModel()
        d = obj.to_dict()
        self.assertIn("id", d)
        self.assertIn("created_at", d)
        self.assertIn("updated_at", d)
        self.assertIn("__class__", d)
        self.assertEqual(d["__class__"], "BaseModel")
        self.assertEqual(d["id"], obj.id)
        self.assertEqual(d["created_at"], obj.created_at.isoformat())
        self.assertEqual(d["updated_at"], obj.updated_at.isoformat())

    def test_to_dict_is_dict_type_and_not_equal_to___dict__(self):
        obj = BaseModel()
        d = obj.to_dict()
        self.assertIsInstance(d, dict)
        self.assertNotEqual(d, obj.__dict__)

    def test_pep8_conformance_base_model(self):
        """Test that base_model.py conforms to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/base_model.py'])
        self.assertEqual(
            result.total_errors, 0,
            f"Found {result.total_errors} PEP8 style errors or warnings."
        )

if __name__ == "__main__":
    unittest.main()
