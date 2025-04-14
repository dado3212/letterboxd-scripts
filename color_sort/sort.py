# TODO: Fix this
import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
from api import fetch_list, update_list_order

list_id = 'A1sf6'
list = fetch_list(list_id)
# Currently just swaps the first two
# TODO: actually sort by color
update_list_order(list_id)