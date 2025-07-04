from typing import Union
from data_types.entry import Entry

class KVEntry(Entry[Union[str, int, float, bool, dict, list, bytes]]):
    """
    Entry class for key-value cache entries that can store various data types.
    """
    pass 