from typing import Union, Any, Dict, List
import requests


class TWSE():
    class OpenData():
        @staticmethod
        def get_listed_company() -> List[Dict[str, str]]:
            try:
                response: requests.Response = requests.get('https://openapi.twse.com.tw/v1/opendata/t187ap03_L')
                data: List[Dict[str, str]] = response.json()
                return data
            except:
                raise RuntimeError

    class ExchangeReport():
        @staticmethod
        def get_current_price(stock_id: str) -> float:
            try:
                response: requests.Response = requests.get(
                    'https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{}.tw&json=1&delay=0'.
                    format(stock_id)
                )
                data: Dict[str, Any] = response.json()
                price: float = float(data['msgArray'][0]['z'])
            except:
                raise RuntimeError("The stock ID is invalid")

            return price

        @staticmethod
        def get_daily_info(stock_id: str) -> Dict[str, Union[str, float]]:

            try:
                response: requests.Response = requests.get(
                    'https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL'
                )
                data: List[Dict[str, str]] = response.json()
                target: Dict[str, str] = next(item for item in data if item["Code"] == stock_id)
                result: Dict[str, Union[str, float]] = {
                    "Name": target['Name'],
                    "TradeVolume": float(target['TradeVolume']),
                    "TradeValue": float(target['TradeValue']),
                    "OpeningPrice": float(target['OpeningPrice']),
                    "HighestPrice": float(target['HighestPrice']),
                    "LowestPrice": float(target['LowestPrice']),
                    "ClosingPrice": float(target['ClosingPrice']),
                    "Change": float(target['Change'])
                }
            except:
                raise RuntimeError("The stock ID is invalid")

            return result
