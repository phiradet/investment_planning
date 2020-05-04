import os
import json
import fire
import requests
from typing import *

from bs4 import BeautifulSoup


data_source = os.environ["FUND_DATA_SRC"]


def extract_symbol_info(page_source: str) -> Dict[str, str]:
    soup = BeautifulSoup(page_source, "html.parser")

    sym_name = soup.find(id="sec-name").text
    sym_id = soup.find(id="sec-id").text

    return {"name": sym_name, "id": sym_id}


def extract_symbol_nav(sym_name: str, sym_id: str) -> List[Dict[str, Union[str, int]]]:
    req_url = f"{data_source}/fn3/api/fund/nav/q?fund={sym_id}&range=SI"
    response = requests.get(req_url)
    response_json = response.json()

    for i in range(len(response_json)):
        response_json[i]["name"] = sym_name
        response_json[i]["morningstar_id"] = sym_id
        response_json[i]["value"] = float(response_json[i]["value"])
    return response_json


def get_nav(fund: str, output_dir: Optional[str] = None, verbose: bool = True):
    url = f"{data_source}/fund/{fund}"
    if verbose:
        print("Start getting information from", url)
    page_source_res = requests.get(url)
    page_source = page_source_res.text

    if verbose:
        print("Extract symbol information")
    info = extract_symbol_info(page_source)

    if verbose:
        print("Extract symbol NAVs", url)
    nav = extract_symbol_nav(info["name"], info["id"])

    if output_dir is None:
        output_dir = "./"
    open_file = os.path.join(output_dir, f"{info['name']}.json")
    if verbose:
        print(f"Writing output {len(nav)} data points to", open_file)
    with open(open_file, "w") as f:
        json.dump(nav, f)


if __name__ == "__main__":
    fire.Fire(get_nav)
