# gfw : Simple CLI for Global Fishing Watch Data

[![Twitter URL](https://img.shields.io/twitter/follow/samapriyaroy?style=social)](https://twitter.com/intent/follow?screen_name=samapriyaroy)
[![Hits-of-Code](https://hitsofcode.com/github/samapriya/gfw?branch=main)](https://hitsofcode.com/github/samapriya/gfw?branch=main)
[![CI GFW](https://github.com/samapriya/gfw/actions/workflows/CI.yml/badge.svg)](https://github.com/samapriya/gfw/actions/workflows/CI.yml)
![PyPI - License](https://img.shields.io/pypi/l/gfw)
![PyPI](https://img.shields.io/pypi/v/gfw)
[![Downloads](https://pepy.tech/badge/gfw/month)](https://pepy.tech/project/gfw)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5937071.svg)](https://doi.org/10.5281/zenodo.5937071)

The Global Fishing Watch map is the first open-access online platform for visualization and analysis of vessel-based human activity at sea, including fishing activity, encounters between vessels, night light vessel detection and vessel presence. This tool is designed to help interact programmatically with the [Global Fishing Watch data](https://globalfishingwatch.org/datasets-and-code/) and is not based on any official API so expect features to break once in a while.

Disclaimer: This is an unofficial tool. Is not licensed or endorsed by Global Fishing Watch. It is created and maintained by Samapriya Roy.


#### Citation

```
Samapriya Roy. (2022). samapriya/gfw: Simple CLI for Global Fishing Watch Data (0.0.4).
Zenodo. https://doi.org/10.5281/zenodo.5937071
```

Readme Docs [available online](https://samapriya.github.io/gfw)

## Table of contents
* [Getting started](#getting-started)
    * [auth](#auth)
    * [data-list](#data-list)
    * [file-list](#file-list)
    * [download](#download)

## Getting started
The tool is a simple standalone tool and the requirements for the setup are included in the requirements.txt file. Depending on the OS and the python version you should be able to simply run

```pip install -r requirements.txt```

To install gfw: Simple CLI for Global Fishing Watch Data

```
pip install gfw
```

or you can also try

```
git clone https://github.com/samapriya/gfw.git
cd gfw
python setup.py install
```

## Main screen

```
gfw -h
usage: gfw [-h] {auth,data-list,file-list,download} ...

Simple CLI for Global Fishing Watch Data

positional arguments:
  {auth,data-list,file-list,download}
    auth                Authenticates and saves your username and password
    data-list           Generate data list with Dataset ID & timestamp
    file-list           File list for dataset
    download            Download datasets

optional arguments:
  -h, --help            show this help message and exit
```

### auth
The auth or authentication tool allows the user to use their name and password used for logging into Global Fishing Watch. This is stored locally and a bearer token is generated every time the tool is being used from the saved credentials.

![gfw_auth](https://user-images.githubusercontent.com/6677629/151841765-62626278-aaff-4f03-8ba9-03b9e6bd4b58.gif)

### data-list
The data list tool fetches the datasets from the datasets and code page of global fishing watch. It then prints a table with both dataset id and the last updated date and time. Incase the server returns a status code of 500, a last updated datasets.json file is used to generate a dataset list.

![gfw_data-list](https://user-images.githubusercontent.com/6677629/151841764-208d05d6-7fb9-4a09-ac7f-2792b774dfe4.gif)

### file-list
The file list tool fetches files inside a dataset and uses the dataset id to search for and print details about each file in the dataset. The tool also prints file size per file as well as total download size estimate.

![gfw_file-list](https://user-images.githubusercontent.com/6677629/151841763-af1485d1-eaab-4647-b7d2-6f3122e3cf08.gif)


### download
The download tool can only be utilized for area of interest that have been saved to my areas. As such this tool utilizes either the AOI name or ID. This submits the request and then waits for zipping to complete to then download a single zip files with all sources.

![gfw_download](https://user-images.githubusercontent.com/6677629/151841761-37188bf0-fbe5-4562-99d5-667aa7046f59.gif)

You can also download a specific file from the file-list tool

![gfw_download_filename](https://user-images.githubusercontent.com/6677629/151841756-341bc4b6-7ab3-4e97-b733-bd7e70c0f8d9.gif)


## Changelog

#### v0.0.4
- added readme pages
- updated tool description and readme

#### v0.0.3
- added nested check for JSON objects from data list
- auto updation of datasets.json file as new datasets become available
- updated Readme

#### v0.0.2
- added tabulate to print dataset id and last updated table
- added offline JSON parser for 500 Internal Server Error from GFW
- general improvements and cleanup
