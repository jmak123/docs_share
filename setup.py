from setuptools import find_packages, setup

__version__ = "0.1"

setup(
    name = "docs_share",
    description = "Sharing docus between views.lkml and dbt yamls.",
    packages=find_packages( include=['docs_share', 'docs_share.*']),
    entry_points = {
        'console_scripts': [
            'update_dbt = docs_share.__init__:update_dbt',
            'update_lkml = docs_share.__init__:update_lkml',
            'testcli = docs_share.__init__:cli',
        ]
    },
    install_requires = [
        "bandit",
        "black",
        "flake8",
        "pytest",
        "pyyaml==5.3.1",
        "lkml @ git+ssh://git@github.com/jmak123/lkml@master"
    ]
)