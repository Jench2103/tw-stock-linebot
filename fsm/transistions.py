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
    # Stock Lookup
    {'trigger': 'advance', 'source': 'init', 'dest': 'stock_lookup', 'conditions': 'is_going_to_stock_lookup'},
    {'trigger': 'advance', 'source': 'stock_lookup', 'dest': 'search_resp', 'conditions': 'is_going_to_search_resp'},
    {'trigger': 'advance', 'source': 'search_resp', 'dest': 'search_resp', 'conditions': 'is_going_to_search_resp'},
    {'trigger': 'advance', 'source': 'search_resp', 'dest': 'init', 'conditions': 'is_going_to_init'},
    {'trigger': 'advance', 'source': 'stock_lookup', 'dest': 'init', 'conditions': 'is_going_to_init'},
]   # yapf: disable
