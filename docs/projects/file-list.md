# Generating file list

The file list tool fetches files inside a dataset and uses the dataset id to search for and print details about each file in the dataset. The tool also prints file size per file as well as total download size estimate.

![gfw_file-list](https://user-images.githubusercontent.com/6677629/151841763-af1485d1-eaab-4647-b7d2-6f3122e3cf08.gif)


```
gfw file-list -h
usage: gfw file-list [-h] --id ID

optional arguments:
  -h, --help  show this help message and exit

Required named arguments.:
  --id ID     Dataset ID
```
