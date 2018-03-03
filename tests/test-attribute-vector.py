
import unittest
import pyone

class AttributeVectorTests(unittest.TestCase):
    def test_dict_to_attr(self):
        atts = {
            'NAME': 'abc',
            'MEMORY': '1024',
            'ATT1': 'value1'
            }
        self.assertIn(pyone.util.dict2one(atts),[ '''NAME = "abc"\nATT1 = "value1"\nMEMORY = "1024"\n''','''NAME = "abc"\nMEMORY = "1024"\nATT1 = "value1"\n'''])
