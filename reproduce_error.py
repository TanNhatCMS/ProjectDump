from typing import Dict

def test_func(text: Dict[str, str]):
    print(text["key"])

test_func({"key": "value"})
