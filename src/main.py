# index.py
from apify_client import ApifyClient
from os import environ
import json

client = ApifyClient(token='apify_api_DY70XhVoMgbSuguGA1Jj5ggnNt7S4x2GLtzg')

# If being run on the platform, the "APIFY_IS_AT_HOME" environment variable
# will be "1". Otherwise, it will be undefined/None
def is_on_apify ():
    return 'APIFY_IS_AT_HOME' in environ

# Get the input
def get_input ():
    if not is_on_apify():
        with open('./storage/key_value_stores/default/INPUT.json') as actor_input:
            return json.load(actor_input)

    kv_store = client.key_value_store(environ.get('APIFY_DEFAULT_KEY_VALUE_STORE_ID'))
    return kv_store.get_record('INPUT')['value']

# Push the solution to the dataset
def set_output (data):
    if not is_on_apify():
        with open('./storage/datasets/default/solution.json', 'w') as output:
            return output.write(json.dumps(data, indent=2))

    dataset = client.dataset(environ.get('APIFY_DEFAULT_DATASET_ID'))
    dataset.push_items('OUTPUT', value=[json.dumps(data, indent=4)])

def add_all_numbers (nums):
    total = 0

    for num in nums:
        total += num

    return total

actor_input = get_input()['numbers']

solution = add_all_numbers(actor_input)

set_output({ 'solution': solution })
