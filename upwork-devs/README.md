# Repositories:
- [Pappaterra Lucia](#pappaterra-lucia)
- [Lwasampijja Baker](#lwasampijja-baker)
- [Moses Mugo](#moses-mugo)


<a id="pappaterra-lucia"></a>
## Pappaterra Lucia

- [1. Pull Request Report](#pull-request-report)
- [2. Generate Files needed for Visualizations and Presentations](#generate-files)
- [3. Organization Chart Visualization](#org-chart-visual)
- [4. Make Power Point Presentation](#make-power-point)

<a id="pull-request-report"></a>
## 1. Pull Request Report

Create a Pull Request report for all current projects by running PR_report.ipynb
jupyter-notebook. Name, link, reviewers and creation date of each PR are listed.

<a id="generate-files"></a>
## 2. Generate Files needed for Visualizations and Presentations

Before running next two notebooks, it's necessary to generate csv and yaml files 
from the sheets in 

https://docs.google.com/spreadsheets/d/1GCDWsyRc2CIkunovZ2-zZaqOdaienEBy/view

that are constantly being updated. 

To do so jupyter-notebook Generate_files.ipynb must be run.

This generates the required files that will be saved in the folders *csv_files* 
and *yaml_files* respectively, for later use in updated visualizations and power
point presentations.


<a id="org-chart-visual"></a>
## 3. Organization Chart Visualization

The jupyter-notebook Org_Chart_Vis.pynb generates visualizations from the 
previously generated files.


<a id="make-power-point"></a>
## 4. Make Power Point Presentation

The jupyter-notebook Make_PowerPoint_Presentation.pynb autocreate power point 
presentation for 'Project Team Structure' sheet.


## 5. Folders:

- *modules* folder contains the codes that work behind notebooks

- csv and yaml files are saved in *csv_files* and *yam_files* respectively, 
these folders must be created locally since they may contain sensitive information

- *images* folder contains images needed to make presentations

- Easy to consume outputs are save in *outputs* folder


<a id="lwasampijja-baker"></a>
## Lwasampijja Baker

- [1. Github Issue Visualisations](#git-issue-vis)
- [2. Zenhub Pipeline Visualisations](#zen-pipe)
- [3. Visualising Issues Accross Multiple Platforms](#vis-plat)


<a id="git-issue-vis"></a>
## 1. Github Issue Visualisations
This project is aimed at comming up with useful visuals and insights to the gitbub issues that are generated on different repositores.
#### Files created
- issues.py: a python script that contains the class and methods that drive the visualisations
- issues.ipynb: jupyter notebook with all the visualisations
#### Required
Generate a github token to be inserted into issues.py, line 19 
![token](https://user-images.githubusercontent.com/8102313/93817512-c37d0880-fc61-11ea-98f3-9a9386ab028d.png)

#### Flow Diagram
![Issue_vis](https://user-images.githubusercontent.com/8102313/93816881-cfb49600-fc60-11ea-9723-47b0ad70d378.png)

#### Usage
(i)  Import dependencies e.g from issues import Issues
(ii) List  repositories to be visualised 
- e.g repos = ['mvp-icap-service', 'mvp-icap-cloud', 'mvp-icap-squid-cache-proxy','c-icap']

(iii) Initialise eg
- issues = Issues(repos)  -> To call issues
- df = issues.get_df()    -> creates dataframe
- issues.important()      -> Select important columns

(iv) Plot visualisations e.g
- issues.show_pie('state') -> pie chart showing open/closed issues
- issues.show_bar_chart_by_repo() -> bar graph showing number of issues per repo
- issues.show_bar_chart_by_date() -> bar graph showing number issues per day
- issues.show_bar_chart_by_user() -> bar graph showing number of issues generated by users
- issues.table_project_state() -> table showing number of open/closed issues per repo
- issues.show_state_user() -> bar graph showing open/closed issues per user

<a id="zen-pipe"></a>
## 2. Zenhub Pipeline Visualisations
This section visualises the different pipelines setup within Zenhub to come up with this visualisation. 
![vis](https://user-images.githubusercontent.com/8102313/94304172-be78cb80-ff77-11ea-9577-9fb63011311d.png)
#### Files created
- issues.py
- Visualise_Zenhub_Pipelines.ipynb

#### Usage
(i)  Import dependencies e.g from from issues import *
(ii) Show tables as indicated in Visualise_Zenhub_Pipelines.ipynb


<a id="zen-pipe"></a>
## 3. Visualising Issues Accross Multiple Platforms

![plat](https://user-images.githubusercontent.com/8102313/94736551-18610300-0375-11eb-83d9-285577873479.png)

The report is in a Google colab notebook and you will need to be invited by Gmail to have access. A preview of the code is available on github for review.

#### File created
- All Progress Issues.ipynb

#### Usage
(i)  On invite, got to the Runtime menu and select Run all, for an updated report.

(ii) To filter, click on filter on top of the table to fiter for the required field accordingly. The last part of the report, has a multiple filter section: To filter by person or repo, fill in the desired filter below. For example.

(If my person of intrest is baker371, filter = "baker371". Note, the filter can take in multiple inputs e.g 

filter = "baker371", "GiuseMSD" 

The same principal applies even when searching for a particular repo e.g 

filter = "k8-data-visualization"

Now run the corresponding two code blocks.

(iii) To export the filtered report to excel, run the last code block, open the folder to the left to download the csv file named report.csv.


<a id="moses-mugo"></a>
## Moses Mugo

Run the command below to create and activate a virtual environment

$python -m venv k8-venv`

$source k8-venv/bin/activate`

Run the command below to install dependencies

$pip install -r requirements.txt

main.py pulls all the pull requests and issues from all the repos and downloads them to data as a csv files


