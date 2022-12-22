from typing import List

INIT_STATE: str = 'init'

STOCK_MANAGER: List[str] = [
    'stock_mgr', 'add_stock', 'add_stock_operation', 'delete_stock', 'delete_stock_operation', 'list_stocks'
]
STOCK_LOOKUP: List[str] = ['stock_lookup', 'search_resp']
INFO_QUERY: List[str] = ['current_price', 'daily_info']

STATES: List[str] = [INIT_STATE] + STOCK_MANAGER + STOCK_LOOKUP + INFO_QUERY
