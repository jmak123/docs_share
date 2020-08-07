import re
from docs_share.lkml_parser import lkml_parser
from docs_share.dbt_parser import dbt_parser

LKML_TABLE_PREFIX = 'analytics.'
LKML_FIELD_PREFIX = '${TABLE}.'

class comparer:

    """
    an object that compares a dbt yaml and a view.lkml
    """
    
    def __init__(self, lkml, dbt):
        self.lkml: lkml_parser = lkml
        self.dbt: dbt_parser = dbt
        self.lkml_to_add: list = []
        self.dbt_to_add: list = []
        self.new_lkml: dict = {}
        self.new_dbt: dict = {}
        self.bool_lkml_add: bool = False
        self.bool_dbt_add: bool = False
        self.compare_lkml_to_dbt()
        self.compare_dbt_to_lkml()
        self.add_desc_to_dbt()
        self.add_desc_to_lkml()

    def compare_lkml_to_dbt(self):
        """
        check validity of field descriptions in lkml
        """
        for l in self.lkml.desc:
            if re.search("^[\\w\\d_]+$", l['field']) is not None:
                self.dbt_to_add.append(l)

    def compare_dbt_to_lkml(self):
        """
        check whether descriptions in dbt has a field match in lkml
        """
        for d in self.dbt.desc:
            self.lkml_to_add.append(d)
        
    def add_desc_to_dbt(self):
        self.new_dbt = self.dbt.content
        for l in self.dbt_to_add:
            if 'models' in self.new_dbt: ## check if it's yaml for model
                for j, m in enumerate(self.new_dbt['models']): ## loop models
                    if m['name'] == l['relation']: ## check if model name matches lkml relation
                        if 'columns' in m: ## check if there's any column
                            self.bool_dbt_add = True
                            col_names = [x['name'] for x in m['columns']] ## check if field is found in columns, update if yes, create new column if no
                            if l['field'] in col_names:
                                for k, c in enumerate(m['columns']): ## loop columns
                                    if c['name'] == l['field']: ## check if field name matches column name
                                        self.new_dbt['models'][j]['columns'][k]['description'] = l['description'] ## overwrite description
                            else:
                                self.new_dbt['models'][j]['columns'].append(
                                    {
                                        'name': l['field'],
                                        'description': l['description']
                                    }
                                )

    def add_desc_to_lkml(self):
        self.new_lkml = self.lkml.content
        for d in self.lkml_to_add:
            if 'views' in self.new_lkml: ## check if it's yaml for model
                for j, v in enumerate(self.new_lkml['views']): ## loop models
                    if 'sql_table_name' in v:
                        if v['sql_table_name'] == LKML_TABLE_PREFIX + d['relation']: ## check if model name matches lkml relation
                            if 'dimensions' in v: ## check if there's any column
                                for k, m in enumerate(v['dimensions']): ## loop columns
                                    if 'sql' in m:
                                        if LKML_FIELD_PREFIX + d['field'] == m['sql']: ## check if field name matches column name
                                            self.bool_lkml_add = True
                                            self.new_lkml['views'][j]['dimensions'][k]['description'] = d['description'] ## overwrite description

