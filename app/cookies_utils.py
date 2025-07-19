import json
from typing import Any


def set_cookies(redis_client, name: str, value: Any):
    serialized_list = json.dumps(value)
    redis_client.set(name, serialized_list)


def get_cookies(redis_client, name: str):
    serialized_list = redis_client.get(name)
    if serialized_list:
        my_list = json.loads(serialized_list)
        return my_list
    else:
        return None


def clear_cookies(redis_client, name: str):
    redis_client.delete(name)