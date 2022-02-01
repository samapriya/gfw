# General Installation

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
