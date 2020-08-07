from docs_share.dbt_parser import dbt_parser
from docs_share.lkml_parser import lkml_parser
from docs_share.comparer import comparer
import os
import argparse 
import yaml
import lkml 

"""
test cmd:

update_dbt -l /Users/jonathan.mak/github/looker -d /Users/jonathan.mak/github/dbt-dw-snowflake/models

update_lkml -l /Users/jonathan.mak/github/looker -d /Users/jonathan.mak/github/dbt-dw-snowflake/models
"""

def cli():
    parser = argparse.ArgumentParser() 
    parser.add_argument("-d", "--dbt", help = "dbt repo root directory") 
    parser.add_argument("-l", "--lkml", help = "lkml repo root directory") 
    args = parser.parse_args() 
    
    # LKML_PATH = args.lkml
    LKML_PATH = '/Users/jonathan.mak/github/looker'
    # DBT_PATH = args.dbt
    DBT_PATH = '/Users/jonathan.mak/github/dbt-dw-snowflake/models'

    return([LKML_PATH, DBT_PATH])

def load(LKML_PATH, DBT_PATH):

    lkml_files = [LKML_PATH + '/' + x for x in os.listdir(LKML_PATH) if '.view.lkml' in x]

    paths = [(root, files) for root, dirs, files in os.walk(DBT_PATH)]
    dbt_files = [z[0] for z in [['/'.join([x[0], y]) for y in x[1] if y == 'schema.yml'] for x in paths] if len(z) > 0]

    dbts = [dbt_parser(d) for d in dbt_files]
    lkmls = [lkml_parser(l) for l in lkml_files]

    return([dbts, lkmls])

def update_dbt():

    LKML_PATH, DBT_PATH = cli()
    dbts, lkmls = load(LKML_PATH, DBT_PATH)

    for dbt in dbts:
        if 'sources' not in dbt.content:
            for lk in lkmls:
                print(f'{dbt.file_path} ----- {lk.file_path}')
                comp = comparer(lk, dbt)
                if len(comp.dbt_to_add) > 0:
                    with open(dbt.file_path, 'w') as f:
                        f.write(yaml.dump(comp.new_dbt, default_flow_style=False, width=4096, sort_keys = False))

def update_lkml():

    LKML_PATH, DBT_PATH = cli()
    dbts, lkmls = load(LKML_PATH, DBT_PATH)

    for lk in lkmls:
        for dbt in dbts:
            if 'sources' not in dbt.content:
                print(f'{lk.file_path} ----- {dbt.file_path}')
                comp = comparer(lk, dbt)
                if len(comp.lkml_to_add) > 0:
                    with open(lk.file_path, 'w') as f:
                        f.write(lkml.dump(comp.new_lkml))

update_dbt()