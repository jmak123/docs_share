import yaml


class dbt_parser:

    """
    base object of a source/schema yaml in dbt repo
    """

    def __init__(self, file_path):
        self.file_path: str = file_path
        self.content: dict = {}
        self.desc: list = []
        self.parse()
        self.get_desc()

    def parse(self):
        """
        open file and load dbt yaml as json
        """
        with open(self.file_path, "r") as f:
            self.content = yaml.safe_load(f)
        return self.content

    def get_desc(self):
        """
        parse all json and get all description field info in views-dimensions
        """
        if (
            "models" in self.content
        ):  ## only consider schema yamls as we ignore source yamls here
            for m in self.content["models"]:
                if "columns" in m:  ## skip models with no columns
                    for c in m["columns"]:
                        if "description" in c:
                            self.desc.append(
                                {
                                    "relation": m["name"],
                                    "field": c["name"],
                                    "description": c["description"],
                                }
                            )
