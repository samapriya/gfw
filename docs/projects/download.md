# Dataset or file download

The download tool can only be utilized for area of interest that have been saved to my areas. As such this tool utilizes either the AOI name or ID. This submits the request and then waits for zipping to complete to then download a single zip files with all sources.

![gfw_download](https://user-images.githubusercontent.com/6677629/151841761-37188bf0-fbe5-4562-99d5-667aa7046f59.gif)

You can also download a specific file from the file-list tool

![gfw_download_filename](https://user-images.githubusercontent.com/6677629/151841756-341bc4b6-7ab3-4e97-b733-bd7e70c0f8d9.gif)


```
gfw download -h
usage: gfw download [-h] --id ID --path PATH [--filename FILENAME]

optional arguments:
  -h, --help           show this help message and exit

Required named arguments.:
  --id ID              Dataset ID
  --path PATH          Full path to folder to download datasets

Optional named arguments:
  --filename FILENAME  Username
```
