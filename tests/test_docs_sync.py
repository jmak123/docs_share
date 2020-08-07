
import unittest
from docs_share.lkml_parser import lkml_parser
from docs_share.dbt_parser import dbt_parser
from docs_share.comparer import comparer

class test_docs_sync(unittest.TestCase):

    def __init__(self, methodName="runTest"):
        unittest.TestCase.__init__(self, methodName)
        self.dbt = dbt_parser('tests/resources/sample_dbt.yml')
        self.lkml = lkml_parser('tests/resources/sample_lkml.lkml')
        self.comp = comparer(self.lkml, self.dbt)
        print('')

    def test_lkml_parse(self):
        self.assertTrue(self.lkml.content is not None)

    def test_lkml_get_desc(self):
        self.assertTrue(len(self.lkml.desc) == 2)

    def test_dbt_parse(self):
        self.assertTrue(self.dbt.content is not None)
    
    def test_dbt_get_desc(self):
        self.assertTrue(len(self.dbt.desc) == 3)

    def test_dbt_compare(self):
        self.assertTrue(len(self.comp.dbt_to_add) == 2)

    def test_lkml_compare(self):
        self.assertTrue(len(self.comp.lkml_to_add) == 3)

    def test_add_desc_to_lkml(self):
        self.assertTrue(self.comp.new_lkml['views'][0]['dimensions'][1]['description'] == 'blah blah')

    def test_add_desc_to_dbt(self):
        self.assertTrue(self.comp.new_dbt['models'][1]['columns'][1]['description'] == 'new docs from lkml')


if __name__ == '__main__':
    unittest.main()
