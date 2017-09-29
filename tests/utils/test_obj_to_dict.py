# Include standard modules
import unittest

# Include 3rd-party modules
# Include DPL modules
from dpl.utils.obj_to_dict import obj_to_dict


class ExampleClass(object):
    def __init__(self, a, b):
        self._a = a
        self._b = b

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    def hello(self):
        print("Hello!", self._a, self._b)

    @staticmethod
    def hello_static():
        print("Hello!")

    @classmethod
    def hello_class(cls):
        print("Hello from class!")


class TestObjToDict(unittest.TestCase):
    def test_object_serialized(self):
        a = 1
        b = 2

        test_obj = ExampleClass(a, b)

        result = obj_to_dict(test_obj)

        self.assertTrue(isinstance(result, dict))

        self.assertEqual(result["a"], a)
        self.assertEqual(result["b"], b)

    def test_private_hidden(self):
        a = 1
        b = 2

        test_obj = ExampleClass(a, b)

        result = obj_to_dict(test_obj)

        self.assertFalse("_a" in result)
        self.assertFalse("_b" in result)

    def test_callables_hidden(self):
        a = 1
        b = 2

        test_obj = ExampleClass(a, b)

        result = obj_to_dict(test_obj)

        self.assertFalse("hello" in result)
        self.assertFalse("hello_static" in result)
        self.assertFalse("hello_class" in result)


if __name__ == '__main__':
    unittest.main()
