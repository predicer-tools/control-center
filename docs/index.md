# Welcome to Elexia Control Center Documentation

Control center is a cross-platform desktop application for running 
[Predicer](https://github.com/predicer-tools/Predicer). It supports fetching input data from [Center Denmark
Dataportal](https://portal.centerdenmark.com/da-DK/), storing it into InFluxDb and displaying it in a Grafana 
dashboard. The input data can be fetched from other sources as well. Control center sends the input data to the 
Predicer model for processing and once it's finished, retrieves the output data and stores it into files or sends
it to Grafana via InFluxDb for displaying.

## 1. Overview
**Name:** Elexia Control Center  
**Purpose:** A desktop application for using Predicer.  
**Status:** alpha  
**Repo(s):** https://github.com/predicer-tools/control-center  
**Lead developer/Maintainer:** Pekka Savolainen (Research Scientist, VTT)  
**Developers:** Pekka Savolainen (VTT), Essi Nousiainen (VTT), Dennis Sundell (VTT), 
Antti Soininen (VTT), Esa Pursiheimo (VTT)  

## 2. Architecture
- UI Layer
    - PySide6
- Core Logic:
    - Python (business logic, data processing)
Inter-process Communication (IPC):
    - InfluxDb server/client architecture
    - Grafana server/client architecture
    - GraphQL
Database:
    - InFluxDb
Auth:
    - Credentials required from Center Denmark Data Portal
Packaging / Build
    - PyInstaller
Deployment:
    - Distributed as a Windows installer (.msi or .exe with NSIS)

## 3. Installation instructions
See installation instructions in the Control Center repository (https://github.com/predicer-tools/control-center).

## 4. Core Features

Feature A: Retrieving input data from data portal and other sources
Feature B: Storing data to InFluxDb
Feature C: Viewing data using Grafana
Feature D: Communicating input/output data with Predicer using GraphQL
Feature E: Executing Predicer model
Feature F: Retrieving Output data from Predicer
