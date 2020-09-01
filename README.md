# k8-data-visualization

If you are working on this project via Upwork, see also our [Upwork Rules of Engagement](https://github.com/filetrust/Open-Source/blob/master/upwork/rules-of-engagement.md)

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

  * create API (Python or Node) to consume data from GitHub (all repos are public, so there is no dependency on Glasswall to provide access)
  * write Tests for all APIs created
  * create CI Pipeline
  * use Jupyter notebook to present data
  * create visualizations using native Jupyter APIs or other Javascript visualization APIs (like https://visjs.org/, https://plantuml.com/ , https://gojs.net/ , https://mermaid-js.github.io/)
  * transform data into graph-based objects and visualize them
  * create as much detailed technical documentation as possible (namely architecture and data-flow diagrams)
