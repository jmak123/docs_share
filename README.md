# docs_share

Parse field descriptions in Looker *views* where `sql` is unaltered then update corresponding model in dbt's *schema.yml*. Or the other way round.

# Install

Not available in PyPi, so just install using 

```pip install git+ssh://git@github.com/jmak123/lkml@master```

# Usage

The package can be run on CLI. It takes the root directories of your local dbt repo and local looker repo, parses into json and updates each other.

To update your local dbt repo with descriptions found in your local lkml repo:

```update_dbt -l {path_of_lkml_repo_root} -d {path_of_dbt_repo_root}```

To update your local lkml repo with descriptions found in your local dbt repo:

```update_lkml -l {path_of_lkml_repo_root} -d {path_of_dbt_repo_root}```

Please note that both operations will overwrite files in local repo. This is deemed reversible as it is assumed that users have git applied to repos which allows for reversal of commit/changes.

