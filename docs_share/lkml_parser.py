import lkml

LKML_TABLE_PREFIX = 'analytics.'
LKML_FIELD_PREFIX = '${TABLE}.'

class lkml_parser:

    """
    base object of a *.lkml file
    """
    
    def __init__(self, file_path):
        self.file_path: str = file_path
        self.content: dict = {}
        self.desc: list = []
        self.parse()
        self.get_desc()

    def parse(self):
        """
        open file and load lkml as json
        """
        with open(self.file_path, 'r') as f:
            self.content = lkml.load(f)
        return(self.content)

    def get_desc(self):

        """
        parse all json and get all non-null description field info in views-dimensions
        """

        if 'views' in self.content: ## only read lkml views
            for v in self.content['views']:
                if 'dimensions' in v: ## only read dimensions because we target "sql:" fields
                    for d in v['dimensions']:
                        if 'description' in d and 'sql' in d and 'sql_table_name' in v: ## check if key identifiers are all there otherwise skip
                            self.desc.append(
                                {
                                    'relation': v['sql_table_name'].replace(LKML_TABLE_PREFIX, ''),
                                    'field': d['sql'].replace(LKML_FIELD_PREFIX, ''),
                                    'description': d['description']
                                }
                            )
