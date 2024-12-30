__all__ = ['get_current_float_timestamp', 'get_current_str_timestamp', 'convert_str_to_float_timestamp', 'convert_float_to_str_timestamp']

import datetime

# float timestamp: UNIX timestamp in seconds
# str timestamp: yyMMddHHmmss formatted string timestamp

def get_current_float_timestamp()->float:
    return datetime.datetime.now().timestamp()

def get_current_str_timestamp()->str:
    return datetime.datetime.now().strftime('%y%m%d%H%M%S')

def convert_str_to_float_timestamp(timestamp: str)->float:
    return datetime.datetime.strptime(timestamp, '%y%m%d%H%M%S').timestamp()

def convert_float_to_str_timestamp(timestamp: float)->str:
    return datetime.datetime.fromtimestamp(timestamp).strftime('%y%m%d%H%M%S')