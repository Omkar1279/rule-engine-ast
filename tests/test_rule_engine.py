import requests
from app.schemas.rule_schema import RuleCreate, RuleUpdate, RuleEvaluate

BASE_URL = "http://127.0.0.1:8000"


def test_create_rule(rule_data):
    print("Testing create_rule...")
    url = f"{BASE_URL}/api/rules/create"
    response = requests.post(url, json=rule_data)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
    response.raise_for_status()
    print(f"Response: {response.json()}")
    return response.json()['id']


def test_combine_rules(rule_ids):
    print("\nTesting combine_rules...")
    url = f"{BASE_URL}/api/rules/combine"
    response = requests.post(url, json=rule_ids)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
    response.raise_for_status()
    print(f"Response: {response.json()}")
    return response.json()['id']


def test_evaluate_rule(rule_id, data):
    print("\nTesting evaluate_rule...")
    url = f"{BASE_URL}/api/rules/evaluate"
    response = requests.post(url, json={"rule_id": rule_id, "data": data})
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
    response.raise_for_status()
    print(f"Response: {response.json()}")


def test_modify_rule(rule_id, new_rule_data):
    print("\nTesting modify_rule...")
    url = f"{BASE_URL}/api/rules/{rule_id}/modify"
    response = requests.put(url, json=new_rule_data)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
    response.raise_for_status()
    print(f"Response: {response.json()}")


def test_get_rules():
    print("\nTesting get_rules...")
    url = f"{BASE_URL}/api/rules/list"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
    response.raise_for_status()
    print(f"Response: {response.json()}")
    return response.json()


def test_delete_rule(rule_id):
    print("\nTesting delete_rule...")
    url = f"{BASE_URL}/api/rules/{rule_id}/delete"
    response = requests.delete(url)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
    response.raise_for_status()
    print(f"Response: {response.json()}")


def test_delete_all_rules():
    print("\nTesting delete_all_rules...")
    url = f"{BASE_URL}/api/rules/delete_all"
    response = requests.delete(url)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
    response.raise_for_status()
    print(f"Response: {response.json()}")


if __name__ == "__main__":
    # Create Rule 1
    rule_data_1 = {
        "rule_string": "(age > 30 AND department = 'Sales')"
    }
    rule_id_1 = test_create_rule(rule_data_1)

    # Create Rule 2
    rule_data_2 = {
        "rule_string": "(salary > 50000 OR experience > 5)"
    }
    rule_id_2 = test_create_rule(rule_data_2)

    # Combine Rules
    combined_rule_id = test_combine_rules([rule_id_1, rule_id_2])

    # Evaluate Combined Rule
    evaluate_data = {
        "age": 35,
        "department": "Sales",
        "salary": 60000,
        "experience": 6
    }
    test_evaluate_rule(combined_rule_id, evaluate_data)

    # Modify Rule
    new_rule_data = {
        "rule_string": "age > 40 AND department = 'HR'"
    }
    test_modify_rule(rule_id_1, new_rule_data)

    # Get All Rules
    test_get_rules()

    # Delete a Specific Rule
    test_delete_rule(rule_id_1)

    # Delete All Rules
    test_delete_all_rules()
