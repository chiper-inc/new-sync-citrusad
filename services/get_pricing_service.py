import requests
import json
from utils.list_utils import chunks, binary_search
from configs.price_config import PRICE_CONFIG

def get_pricing_service(location_id, store_references, idx_store_references, metadata):
    url = PRICE_CONFIG['URL_PRICE']
    pricing_auth = PRICE_CONFIG['AUTH_PRICE']
    headers = {'Authorization': f'{pricing_auth}',
        'Content-Type': 'application/json'}
    chunks_products = chunks(store_references, 200)
    for chunk in chunks_products:
        store_references = chunk
        body = {
            "storeReferences":store_references,
            "locationId": location_id,
            "channelId":1
        }
        body_string = json.dumps(body)
        try:
            res_pricing = requests.request(
                "put",
                f"{url}/generate-pricing",
                headers=headers,
                data=body_string)
            if res_pricing.status_code != 200:
                return {}
            response_json = res_pricing.json()
            if len(response_json) < 1:
                return {}
            for pricing in response_json:
                try:
                    store_reference_id = pricing['storeReferenceId']
                    idx_store_reference = binary_search(idx_store_references, store_reference_id)
                    metadata[idx_store_reference]['price']  = pricing['values'][0]['total']
                    if "discountedExternalId" in pricing ["values"] [0]:
                        metadata[idx_store_reference]['filters'].append(f"discountLocation:{location_id}")
                except Exception as _:
                    None

        except Exception as ex:
            print("error pricing service",ex)
            return {}