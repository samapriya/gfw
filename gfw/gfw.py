import requests
import time
import sys
import os
import json
import getpass
import argparse
from bs4 import BeautifulSoup as bs
from os.path import expanduser
from tenacity import retry, stop_after_attempt, wait_exponential


# set credentials
def auth(usr):
    home = expanduser("~/pygfw.json")
    if usr is None:
        usr = input("Enter email: ")
    pwd = getpass.getpass("Enter password: ")
    data = {"username": usr, "password": pwd}
    with open(home, "w") as outfile:
        json.dump(data, outfile)


def auth_from_parser(args):
    auth(usr=args.username)


########################## Fetches the auth token and creates an header with JWT ############################################
@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(4))
def tokenizer():
    home = expanduser("~/pygfw.json")
    if not os.path.exists(home):
        auth(usr)
        with open(home) as json_file:
            data = json.load(json_file)
            username = data.get("username")
            pwd = data.get("password")
    else:
        with open(home) as json_file:
            data = json.load(json_file)
            username = data.get("username")
            pwd = data.get("password")

    session = requests.session()
    site = session.get(
        "https://gateway.api.globalfishingwatch.org/auth?client=gfw&callback=https://globalfishingwatch.org/data-download/"
    )
    koa = site.headers["set-cookie"].split(";")
    cookies = {
        "koa:sess": koa[0].split("sess=")[1],
        "koa:sess.sig": koa[2].split("sig=")[1],
    }

    soup = bs(site.content, "html.parser")
    csrf = soup.find("input", {"name": "_csrf"})["value"]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "null",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "TE": "trailers",
    }

    params = (("locale", "en"),)

    data = {"_csrf": csrf, "email": username, "password": pwd}

    time.sleep(1)
    r = session.post(
        "https://gateway.api.globalfishingwatch.org/auth/login",
        headers=headers,
        params=params,
        data=data,
        cookies=cookies,
        allow_redirects=False,
    )
    if r.status_code == 302:
        location = r.headers["location"]
        params = (("access-token", location.split("token=")[1]),)
        r = session.get(
            "https://gateway.api.globalfishingwatch.org/auth/token",
            headers=headers,
            params=params,
        )
        ### setup request headers
        headers = {
            "authority": "gateway.api.globalfishingwatch.org",
            "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
            "authorization": f"Bearer {r.json()['token']}",
            "content-type": "application/json",
            "sec-ch-ua-mobile": "?0",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
            "sec-ch-ua-platform": '"Windows"',
            "accept": "*/*",
            "origin": "https://globalfishingwatch.org",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://globalfishingwatch.org/",
            "accept-language": "en-US,en;q=0.9",
        }

        return headers
    else:
        raise Exception


def list_data():
    headers = tokenizer()
    if headers is None:
        sys.exit("Authentication token not found")
    response = requests.get(
        "https://gateway.api.globalfishingwatch.org/v1/download/dataset",
        headers=headers,
    )
    if response.status_code == 200:
        # print(json.dumps(response.json(), indent=2))
        for items in response.json():
            print(f"{items['id']} ===> Updated: {items['lastUpdated']}")
    else:
        print(f"Failed to get data list with error code :{response.status_code}")


def dl_from_parser(args):
    list_data()


suffixes = ["B", "KB", "MB", "GB", "TB", "PB"]


def humansize(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.0
        i += 1
    f = ("%.2f" % nbytes).rstrip("0").rstrip(".")
    return "%s %s" % (f, suffixes[i])


def list_files(id):
    headers = tokenizer()
    if headers is None:
        sys.exit("Authentication token not found")
    file_size = []
    response = requests.get(
        f"https://gateway.api.globalfishingwatch.org/v1/download/dataset/{id}",
        headers=headers,
    )
    if response.status_code == 200:
        output = response.json()
        for file in output["files"]:
            print(f"{file['name']} of size {humansize(int(file['size']))}")
            file_size.append(int(file["size"]))
        print("\n" + f"Last updated: {response.json()['lastUpdated']}")
        print(f"Estimated Download Size for order: {humansize(sum(file_size))}")
    else:
        print(f"Failed to get file list with error code :{response.status_code}")


def fl_from_parser(args):
    list_files(fid=args.id)


def downloader(url, local_path, headers):
    filename = url.split("/")[-1]
    local_path = os.path.join(local_path, filename)
    url_response = requests.get(url, headers=headers)
    try:
        if not os.path.exists(local_path) and url_response.status_code == 200:
            print(f"Downloading to :{local_path}")
            file_url = url_response.json()["url"]
            response = requests.get(file_url, headers=headers)
            f = open(local_path, "wb")
            for chunk in response.iter_content(chunk_size=512 * 1024):
                if chunk:
                    f.write(chunk)
            f.close()
        elif url_response.status_code == 429:
            raise Exception("rate limit error")
        else:
            if int(url_response.status_code) != 200:
                print(
                    f"Encountered error with code: {result.status_code} for {os.path.split(items['name'])[-1]}"
                )
            elif int(url_response.status_code) == 200:
                print(f"File already exists SKIPPING: {os.path.split(local_path)[-1]}")
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        sys.exit("\n" + "Exited by user")


@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(4))
def data_download(id, filename, local_path):
    headers = tokenizer()
    if filename is None:
        flist = []
        response = requests.get(
            f"https://gateway.api.globalfishingwatch.org/v1/download/dataset/{id}",
            headers=headers,
        )
        if response.status_code == 200:
            output = response.json()
            for file in output["files"]:
                flist.append(file["name"])
        else:
            raise Exception
        if flist:
            for filename in flist:
                url = f"https://gateway.api.globalfishingwatch.org/v1/download/dataset/{id}/download/{filename}"
                downloader(url, local_path, headers)
    else:
        url = f"https://gateway.api.globalfishingwatch.org/v1/download/dataset/{id}/download/{filename}"
        downloader(url, local_path, headers)


def dw_from_parser(args):
    data_download(id=args.id, filename=args.filename, local_path=args.path)


def main(args=None):
    parser = argparse.ArgumentParser(
        description="Simple CLI for Global Fishing Watch Data"
    )
    subparsers = parser.add_subparsers()

    parser_auth = subparsers.add_parser(
        "auth", help="Authenticates and saves your username and password"
    )
    required_named = parser_auth.add_argument_group("Required named arguments.")
    required_named.add_argument("--username", help="Username", required=True)
    parser_auth.set_defaults(func=auth_from_parser)

    parser_dl = subparsers.add_parser("data-list", help="Regenerates your API token")
    parser_dl.set_defaults(func=dl_from_parser)

    parser_fl = subparsers.add_parser("file-list", help="File list for dataset")
    required_named = parser_fl.add_argument_group("Required named arguments.")
    required_named.add_argument("--id", help="Dataset ID", required=True)
    parser_fl.set_defaults(func=fl_from_parser)

    parser_dw = subparsers.add_parser("download", help="Download datasets")
    required_named = parser_dw.add_argument_group("Required named arguments.")
    required_named.add_argument("--id", help="Dataset ID", required=True)
    required_named.add_argument(
        "--path", help="Full path to folder to download datasets", required=True
    )
    optional_named = parser_dw.add_argument_group("Optional named arguments")
    optional_named.add_argument("--filename", help="Username", default=None)
    parser_dw.set_defaults(func=dw_from_parser)

    args = parser.parse_args()

    try:
        func = args.func
    except AttributeError:
        parser.error("too few arguments")
    func(args)


if __name__ == "__main__":
    main()
