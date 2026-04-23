import pytest
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from tasks.task_manager import *

def test_calculate_reward():
    assert calculate_reward(100, 2) == 120.0

def test_is_high_danger_contract():
    assert is_high_danger_contract(5, "Blaviken") is True
    assert is_high_danger_contract(2, "Oxenfurt") is False

def test_get_monster_weakness():
    assert "fire" in get_monster_weakness("leshen")

def test_filter_contracts_by_reward():
    sample = [{"reward": 300}, {"reward": 100}]
    assert filter_contracts_by_reward(sample, 200) == [{"reward": 300}]

def test_get_most_common_monster():
    monsters = ["ghoul", "wraith", "ghoul", "nekker"]
    assert get_most_common_monster(monsters) == "ghoul"

def test_apply_discount():
    discount = lambda x: x * 0.9
    assert apply_discount(200.0, discount) == 180.0

def test_summarize_monster_data():
    monsters = ['ghoul', 'leshen', 'ghoul', 'drowner', 'leshen', 'ghoul']
    result = summarize_monster_data(monsters)
    assert result == {'ghoul': 3, 'leshen': 2, 'drowner': 1}

def test_filter_contracts_by_reward():
    contracts = [
        {"id": 1, "monster": "ghoul", "reward": 300},
        {"id": 2, "monster": "drowner", "reward": 150},
        {"id": 3, "monster": "leshen", "reward": 500}
    ]
    result = filter_contracts_by_reward(contracts, 300)
    assert result == [
        {"id": 1, "monster": "ghoul", "reward": 300},
        {"id": 3, "monster": "leshen", "reward": 500}
    ]

def test_sort_contracts_by_difficulty():
    contracts = [
        {"id": 1, "difficulty": 3},
        {"id": 2, "difficulty": 1},
        {"id": 3, "difficulty": 5}
    ]
    result = sort_contracts_by_difficulty(contracts)
    assert result == [
        {"id": 2, "difficulty": 1},
        {"id": 1, "difficulty": 3},
        {"id": 3, "difficulty": 5}
    ]

def send_post_request(url: str, data: dict, headers: dict = None):
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # hata varsa exception fırlatır
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Status Code: {response.status_code}")
    except Exception as err:
        print(f"Other error occurred: {err}")

class ResultCollector:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            if report.passed:
                self.passed += 1
            elif report.failed:
                self.failed += 1

def run_tests():
    collector = ResultCollector()
    pytest.main(["tests"], plugins=[collector])
    print(f"\nToplam Başarılı: {collector.passed}")
    print(f"Toplam Başarısız: {collector.failed}")
    
    user_score = (collector.passed / (collector.passed + collector.failed)) * 100
    print(round(user_score, 2))
    
    url = "https://kaizu-api-8cd10af40cb3.herokuapp.com/projectLog"
    payload = {
        "user_id": 518,
        "project_id": 166,
        "user_score": round(user_score, 2),
        "is_auto": False
    }
    headers = {
        "Content-Type": "application/json"
    }
    send_post_request(url, payload, headers)

if __name__ == "__main__":
    run_tests()