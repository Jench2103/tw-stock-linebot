from typing import Union, Any, Dict, List
import requests
import json
from datetime import date, timedelta

from flask_line import config


def dump_json(data) -> None:
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


class FinMind():
    url: str = 'https://api.finmindtrade.com/api/v4/data'
    token: str = config['fin_mind']['token']

    @classmethod
    def stock_info(cls) -> List[Dict[str, str]]:
        # https://finmind.github.io/tutor/TaiwanMarket/Technical/#taiwanstockinfo
        parameter: Dict[str, str] = {"dataset": "TaiwanStockInfo", "token": cls.token}
        row_data: Dict[str, Any] = requests.get(cls.url, params=parameter).json()
        stock_list_origin: List[Dict[str, str]] = row_data['data']
        stock_dict: Dict[str, Dict[str, str]] = {}
        stock_list: List[Dict[str, str]] = []

        for item in stock_list_origin:
            if item['stock_id'] in stock_dict:
                if item['industry_category'] not in stock_dict[item['stock_id']]['industry_category']:
                    stock_dict[item['stock_id']]['industry_category'] += ", {}".format(item['industry_category'])
            else:
                stock_dict[item['stock_id']] = item
                stock_dict[item['stock_id']].pop('date', None)

        stock_list = list(stock_dict.values())

        return stock_list

    @classmethod
    def stock_daily_price(cls, stock_id: str) -> Dict[str, Union[str, int, float]]:
        # https://finmind.github.io/tutor/TaiwanMarket/Technical/#taiwanstockprice
        parameter: Dict[str, str] = {
            "dataset": "TaiwanStockPrice",
            "data_id": stock_id,
            "start_date": (date.today() - timedelta(days=7)).isoformat(),
            "end_date": date.today().isoformat(),
            "token": cls.token
        }
        row_data: Dict[str, Any] = requests.get(cls.url, params=parameter).json()
        latest_price: Dict[str, Union[str, int, float]] = row_data['data'][-1]
        return latest_price

    @classmethod
    def stock_dividend(cls, stock_id: str) -> Dict[str, Union[str, float]]:
        # https://finmind.github.io/tutor/TaiwanMarket/Fundamental/#taiwanstockdividend
        parameter = {
            "dataset": "TaiwanStockDividend",
            "data_id": stock_id,
            "start_date": (date.today() - timedelta(days=365)).isoformat(),
            "token": cls.token
        }
        row_data: Dict[str, Any] = requests.get(cls.url, params=parameter).json()
        latest_dividend: Dict[str, Union[str, float]] = row_data['data'][-1]
        return latest_dividend
