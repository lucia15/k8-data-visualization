# k8-data-visualization

If you are working on this project via Upwork, see also our [Upwork Rules of Engagement](https://github.com/filetrust/Open-Source/blob/master/upwork/rules-of-engagement.md)


If you are newcomer, then please check [Glasswall newcomers checklist ](https://github.com/filetrust/Open-Source )

## Project Brief
Objective: Consume, process, normalize and visualize GitHub Issues data

* Glasswall ICAP project (see https://github.com/filetrust/program-icap) is currently under active development and there is a need to understand the exact issue status of all sub-projects

* There are a number of sub-projects (each with it's own set of issues)

  * https://github.com/filetrust/mvp-icap-service
  * https://github.com/filetrust/mvp-icap-cloud
  * https://github.com/filetrust/mvp-icap-squid-cache-proxy
  * https://github.com/filetrust/rebuild-k8s-filetypedetection
  * https://github.com/filetrust/icap-performance-tests
  * https://github.com/filetrust/rebuild-k8s
  * https://github.com/filetrust/k8-reverse-proxy

* At the moment we are using https://www.zenhub.com/extension to consolidate and understand the data, but there are a number of workflows that require the creation of data-connectors and custom visualizations

* Here is the recommended workflow for this project:

  * Create API (Python or Node) to consume data from GitHub (all repos are public, so there is no dependency on Glasswall to provide access)
  * Write Tests for all APIs created
  * Create CI Pipeline
  * Use Jupyter notebook to present data
  * Graph Nodes  : GitHub issues, GH repos, Authors and Projects.  And Edges : the relationships between them.
  * Create visualizations using native Jupyter APIs or other Javascript visualization APIs (like https://visjs.org/, https://plantuml.com/ , https://gojs.net/ , https://mermaid-js.github.io/)
  * Transform data into graph-based objects and visualize them
  * Create as much detailed technical documentation as possible (namely architecture and data-flow diagrams)

* Key points   

 * Setup a serverless workflow which gets triggered with GitHub issues events (We should evaluate if we can use github actions or else go with AWS)
 * The event data in JSON format (committed to a GitHub repo) to be injected to the elastic server(e..g what log_to_elk does for JIRA).
 * Leverage osbot_aws api from public APIS https://github.com/owasp-sbot/ managed by GW. The bot API will fetch data from the elastic server. 
 * The raw issue data, to be consumed by the Jupyter Notebooks notebook. 
 * The data stored on a separate repo will allow the Developers working on the visualization to not have to deal with the data collection.
 * For visualisation, use notebooks since they are good for prototyping, but we will need a Web Based UI to access the data.
 * All code should follow Coding guideline, formatted in IDE and static analysis need to be done.


  
## Running Jupyter Notebooks

Add support for running Jupyter Notebooks docker image locally (mounting the current source code as the root of the notebooks folder)

Fire the following command
```
sh run-local-jupyter.sh
```
## Coding Guideline


These are the coding guidelines we tend to follow for Python projects at Glasswall

If you are newcomer, then please check [Glasswall newcomers checklist ](https://github.com/filetrust/Open-Source )

## Project Brief
Objective: Consume, process, normalize and visualize GitHub Issues data

* Glasswall ICAP project (see https://github.com/filetrust/program-icap) is currently under active development and there is a need to understand the exact issue status of all sub-projects

* There are a number of sub-projects (each with it's own set of issues)

  * https://github.com/filetrust/mvp-icap-service
  * https://github.com/filetrust/mvp-icap-cloud
  * https://github.com/filetrust/mvp-icap-squid-cache-proxy
  * https://github.com/filetrust/rebuild-k8s-filetypedetection
  * https://github.com/filetrust/icap-performance-tests
  * https://github.com/filetrust/rebuild-k8s
  * https://github.com/filetrust/k8-reverse-proxy

* At the moment we are using https://www.zenhub.com/extension to consolidate and understand the data, but there are a number of workflows that require the creation of data-connectors and custom visualizations

* Here is the recommended workflow for this project:

  * Create API (Python or Node) to consume data from GitHub (all repos are public, so there is no dependency on Glasswall to provide access)
  * Write Tests for all APIs created
  * Create CI Pipeline
  * Use Jupyter notebook to present data
  * Graph Nodes  : GitHub issues, GH repos, Authors and Projects.  And Edges : the relationships between them.
  * Create visualizations using native Jupyter APIs or other Javascript visualization APIs (like https://visjs.org/, https://plantuml.com/ , https://gojs.net/ , https://mermaid-js.github.io/)
  * Transform data into graph-based objects and visualize them
  * Create as much detailed technical documentation as possible (namely architecture and data-flow diagrams)

* Key points   

 * Setup a serverless workflow which gets triggered with GitHub issues events (We should evaluate if we can use github actions or else go with AWS)
 * The event data in JSON format (committed to a GitHub repo) to be injected to the elastic server(e..g what log_to_elk does for JIRA).
 * Leverage osbot_aws api from public APIS https://github.com/owasp-sbot/ managed by GW. The bot API will fetch data from the elastic server. 
 * The raw issue data, to be consumed by the Jupyter Notebooks notebook. 
 * The data stored on a separate repo will allow the Developers working on the visualization to not have to deal with the data collection.
 * For visualisation, use notebooks since they are good for prototyping, but we will need a Web Based UI to access the data.
 * All code should follow Coding guideline, formatted in IDE and static analysis need to be done.


  
## Running Jupyter Notebooks

Add support for running Jupyter Notebooks docker image locally (mounting the current source code as the root of the notebooks folder)

Fire the following command
```
sh run-local-jupyter.sh
```
