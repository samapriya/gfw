# Generating data list

The data list tool fetches the datasets from the datasets and code page of global fishing watch. It then prints a table with both dataset id and the last updated date and time. Incase the server returns a status code of 500, a last updated datasets.json file is used to generate a dataset list.

![gfw_data-list](https://user-images.githubusercontent.com/6677629/151841764-208d05d6-7fb9-4a09-ac7f-2792b774dfe4.gif)

```
gfw data-list -h
usage: gfw data-list [-h]

optional arguments:
  -h, --help  show this help message and exit
```
