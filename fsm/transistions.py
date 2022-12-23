from typing import Dict, List


TRANSITIONS: List[Dict[str, str]] = [
    # {'trigger': 'advance', 'source': '', 'dest': '', 'conditions': ''},
    # Stock Manager
    {'trigger': 'advance', 'source': 'init', 'dest': 'stock_mgr', 'conditions': 'is_going_to_stock_mgr'},
    {'trigger': 'advance', 'source': 'stock_mgr', 'dest': 'init', 'conditions': 'is_going_to_init'},
    # Stock Manager - Add Stocks
    {'trigger': 'advance', 'source': 'stock_mgr', 'dest': 'add_stock', 'conditions': 'is_going_to_add_stock'},
    {'trigger': 'advance', 'source': 'add_stock', 'dest': 'add_stock_operation', 'conditions': 'is_going_to_add_stock_operation'},
    {'trigger': 'advance', 'source': 'add_stock_operation', 'dest': 'add_stock_operation', 'conditions': 'is_going_to_add_stock_operation'},
    {'trigger': 'advance', 'source': 'add_stock_operation', 'dest': 'stock_mgr', 'conditions': 'is_going_to_stock_mgr'},
    # Stock Manager - Delete Stocks
    {'trigger': 'advance', 'source': 'stock_mgr', 'dest': 'delete_stock', 'conditions': 'is_going_to_delete_stock'},
    {'trigger': 'advance', 'source': 'delete_stock', 'dest': 'delete_stock_operation', 'conditions': 'is_going_to_delete_stock_operation'},
    {'trigger': 'advance', 'source': 'delete_stock_operation', 'dest': 'delete_stock_operation', 'conditions': 'is_going_to_delete_stock_operation'},
    {'trigger': 'advance', 'source': 'delete_stock_operation', 'dest': 'stock_mgr', 'conditions': 'is_going_to_stock_mgr'},
    # Stock Manager - List Stocks
    {'trigger': 'advance', 'source': 'stock_mgr', 'dest': 'list_stocks', 'conditions': 'is_going_to_list_stocks'},
    {'trigger': 'advance', 'source': 'list_stocks', 'dest': 'add_stock', 'conditions': 'is_going_to_add_stock'},
    {'trigger': 'advance', 'source': 'list_stocks', 'dest': 'delete_stock', 'conditions': 'is_going_to_delete_stock'},
    {'trigger': 'advance', 'source': 'list_stocks', 'dest': 'list_stocks', 'conditions': 'is_going_to_list_stocks'},
    {'trigger': 'advance', 'source': 'list_stocks', 'dest': 'init', 'conditions': 'is_going_to_init'},
    # Stock Lookup
    {'trigger': 'advance', 'source': 'init', 'dest': 'stock_lookup', 'conditions': 'is_going_to_stock_lookup'},
    {'trigger': 'advance', 'source': 'stock_lookup', 'dest': 'search_resp', 'conditions': 'is_going_to_search_resp'},
    {'trigger': 'advance', 'source': 'search_resp', 'dest': 'search_resp', 'conditions': 'is_going_to_search_resp'},
    {'trigger': 'advance', 'source': 'search_resp', 'dest': 'init', 'conditions': 'is_going_to_init'},
    {'trigger': 'advance', 'source': 'stock_lookup', 'dest': 'init', 'conditions': 'is_going_to_init'},
    # Info Query
    {'trigger': 'advance', 'source': 'init', 'dest': 'info_query', 'conditions': 'is_going_to_info_query'},
    {'trigger': 'advance', 'source': 'info_query', 'dest': 'current_price', 'conditions': 'is_going_to_current_price'},
    {'trigger': 'advance', 'source': 'info_query', 'dest': 'daily_price', 'conditions': 'is_going_to_daily_price'},
    {'trigger': 'advance', 'source': 'info_query', 'dest': 'latest_dividend', 'conditions': 'is_going_to_latest_dividend'},
    {'trigger': 'advance', 'source': 'current_price', 'dest': 'current_price', 'conditions': 'is_going_to_current_price'},
    {'trigger': 'advance', 'source': 'current_price', 'dest': 'daily_price', 'conditions': 'is_going_to_daily_price'},
    {'trigger': 'advance', 'source': 'current_price', 'dest': 'latest_dividend', 'conditions': 'is_going_to_latest_dividend'},
    {'trigger': 'advance', 'source': 'daily_price', 'dest': 'current_price', 'conditions': 'is_going_to_current_price'},
    {'trigger': 'advance', 'source': 'daily_price', 'dest': 'daily_price', 'conditions': 'is_going_to_daily_price'},
    {'trigger': 'advance', 'source': 'daily_price', 'dest': 'latest_dividend', 'conditions': 'is_going_to_latest_dividend'},
    {'trigger': 'advance', 'source': 'latest_dividend', 'dest': 'current_price', 'conditions': 'is_going_to_current_price'},
    {'trigger': 'advance', 'source': 'latest_dividend', 'dest': 'daily_price', 'conditions': 'is_going_to_daily_price'},
    {'trigger': 'advance', 'source': 'latest_dividend', 'dest': 'latest_dividend', 'conditions': 'is_going_to_latest_dividend'},
    {'trigger': 'advance', 'source': 'info_query', 'dest': 'init', 'conditions': 'is_going_to_init'},
    {'trigger': 'advance', 'source': 'current_price', 'dest': 'init', 'conditions': 'is_going_to_init'},
    {'trigger': 'advance', 'source': 'daily_price', 'dest': 'init', 'conditions': 'is_going_to_init'},
    {'trigger': 'advance', 'source': 'latest_dividend', 'dest': 'init', 'conditions': 'is_going_to_init'},
]   # yapf: disable
