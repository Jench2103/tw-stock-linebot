from typing import Any, Dict, List
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
