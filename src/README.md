# actions script

## Description
The `Actions` script is a tool used to deploy workflows to a repository that contains specific topics.

The `Actions` script checks what topics are in the repository and finds a workflow for them.

## Usage
```shell
usage: main.py [-h] [--org "organization"] --dest "destination" --type "repository|topic"

File push to github repository

optional arguments:
  -h, --help            show this help message and exit
  --org "organization"  organization of github repository (Default=cloudforet-io)
  --dest "destination"  destination of workflows
  --type "repository|topic"
                        type of destination

Examples:
    python src/main.py --org exam-org --dest inventory --type repository
    python src/main.py --dest inventory --type repository
    python src/main.py --dest config --type repository
    python src/main.py --dest core/console --type topic
```
