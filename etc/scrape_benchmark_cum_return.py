import os
import requests
from typing import *
from datetime import datetime

import fire
import pandas as pd
from tqdm.auto import tqdm


def main(fund_benchmark_file: str, output_dir: str, start: str = "2000-01-01", 
         end: Optional[str] = None, target_fund: Optional[str] = None):
    mstar_benchmark_df = pd.read_csv(fund_benchmark_file, delimiter=",")
    mstar_benchmark_df[mstar_benchmark_df["type"] == "category"]

    if end is None:
        today = datetime.strftime(datetime.today(), "%Y-%m-%d")
        end = today

    for ind, row in tqdm(mstar_benchmark_df.iterrows()):
        morning_star_id = row["morning_star_id"]

        if target_fund is not None and target_fund != morning_star_id:
            continue
        category_name = row["name"].lower().replace(" ", "_")
        type_name = row["type"]
        country = row["country"]

        if country == "TH":
            url = f"https://tools.morningstarthailand.com/api/rest.svc/timeseries_cumulativereturn/4j1cmnvbju?id={morning_star_id}%5D8%5D%5DCAGBR%24%24ALL&currencyId=THB&idtype=Morningstar&frequency=daily&startDate={start}&endDate={end}&performanceType=&outputType=COMPACTJSON"
        elif country == "UK":
            url = f"https://tools.morningstar.co.uk/api/rest.svc/timeseries_cumulativereturn/t92wz0sj7c?currencyId=GBP&idtype=Morningstar&frequency=daily&startDate={start}&endDate={end}&performanceType=&outputType=COMPACTJSON&id={morning_star_id}]2]0]FOGBR$$ALL&decPlaces=8&applyTrackRecordExtension=true"
        else:
            raise ValueError(f"Unable to recognize the country {country}")
        return_df = pd.DataFrame(requests.get(url).json(), columns=["date", "cum_return"])
        return_df["date"] = pd.to_datetime(return_df["date"], unit='ms')
        return_df["name"] = row["name"]
        return_df["morning_star_id"] = morning_star_id

        filename = os.path.join(output_dir,
                                f"{end.replace('-', '')}_{morning_star_id}_{category_name}_{type_name}.json")

        print(filename)
        print(return_df.head())
        print(return_df.tail())
        return_df.to_json(filename, force_ascii=False, orient="records", lines=True)
        print("------")


if __name__ == "__main__":
    fire.Fire(main)
