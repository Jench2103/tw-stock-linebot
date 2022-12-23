from typing import Union, Any, Dict, List
import requests
import json
from datetime import date, timedelta

from config import CONFIG


def dump_json(data) -> None:
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


class FinMind():
    url: str = 'https://api.finmindtrade.com/api/v4/data'
    token: str = CONFIG['fin_mind']['token']

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
    def stock_daily_price(cls, stock_id: str) -> Union[Dict[str, Union[str, int, float]], None]:
        # https://finmind.github.io/tutor/TaiwanMarket/Technical/#taiwanstockprice
        '''
        {
            'date': '2022-12-23',
            'stock_id': '0050',
            'Trading_Volume': 6556232,
            'Trading_money': 725974713,
            'open': 110.7,
            'max': 111.05,
            'min': 110.4,
            'close': 110.7,
            'spread': -1.9,
            'Trading_turnover': 13445
        }
        '''
        parameter: Dict[str, str] = {
            "dataset": "TaiwanStockPrice",
            "data_id": stock_id,
            "start_date": (date.today() - timedelta(days=7)).isoformat(),
            "end_date": date.today().isoformat(),
            "token": cls.token
        }
        row_data: Dict[str, Any] = requests.get(cls.url, params=parameter).json()
        try:
            latest_price: Dict[str, Union[str, int, float]] = row_data['data'][-1]
            return latest_price
        except:
            return None

    @classmethod
    def stock_dividend(cls, stock_id: str) -> Union[Dict[str, Union[str, float]], None]:
        # https://finmind.github.io/tutor/TaiwanMarket/Fundamental/#taiwanstockdividend
        '''
        {
            'date': '2022-07-24',
            'stock_id': '0050',
            'year': '111',
            'StockEarningsDistribution': 0.0,
            'StockStatutorySurplus': 0.0,
            'StockExDividendTradingDate': '',
            'TotalEmployeeStockDividend': 0.0,
            'TotalEmployeeStockDividendAmount': 0.0,
            'RatioOfEmployeeStockDividendOfTotal': 0.0,
            'RatioOfEmployeeStockDividend': 0.0,
            'CashEarningsDistribution': 1.8,
            'CashStatutorySurplus': 0.0,
            'CashExDividendTradingDate': '2022-07-18',
            'CashDividendPaymentDate': '2022-08-02',
            'TotalEmployeeCashDividend': 0.0,
            'TotalNumberOfCashCapitalIncrease': 0.0,
            'CashIncreaseSubscriptionRate': 0.0,
            'CashIncreaseSubscriptionpRrice': 0.0,
            'RemunerationOfDirectorsAndSupervisors': 0.0,
            'ParticipateDistributionOfTotalShares': 0.0,
            'AnnouncementDate': '',
            'AnnouncementTime': ''
        }
        '''
        parameter = {
            "dataset": "TaiwanStockDividend",
            "data_id": stock_id,
            "start_date": (date.today() - timedelta(days=365)).isoformat(),
            "token": cls.token
        }
        row_data: Dict[str, Any] = requests.get(cls.url, params=parameter).json()
        latest_dividend: Union[Dict[str, Union[str, float]], None] = None
        try:
            latest_dividend = row_data['data'][-1]
        except:
            latest_dividend = None
        return latest_dividend
