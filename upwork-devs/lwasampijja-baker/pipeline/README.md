# Testing all the APIS created in issues.py

This document gives a brief overview on how to setup a virtual environment for running tests in the APIs created to make 
sure they run with out any bugs before a pull request.

## Installation

### Requirements

**Software**:

- Python >3.3
- pip >= 20
- An updated web browser
- Optional: git, virtualenv



### Steps Set up a virtual environment and run the tests locally in bash 


git clone -b lwasampijja-baker/pipeline git@github.com:baker371/k8-data-visualization.git

cd pipeline

python3 -m venv environment

source environment/bin/activate

python setup.py develop

pytest
