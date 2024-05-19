import json
import requests

from utils.list_utils import chunks
from configs.citrus_config import CITRUS_CONFIG

def post_product_citrusad(metadata):
    team_id = CITRUS_CONFIG['TEAM_CITRUS']
    url = CITRUS_CONFIG['URL_CITRUS']
    endpoint = f"{url}/catalog-products?teamId={team_id}"
    pricing_auth = CITRUS_CONFIG['AUTH_CITRUS']
    headers = {'Authorization': f'Basic {pricing_auth}',
               'Content-Type': 'application/json'}
    try:
        chunks_products = chunks(metadata, 100)
        for chunk_product in chunks_products:
            json_body = {'catalogProducts':chunk_product}
            body_string = json.dumps(json_body)
            requests.request(
                "post",
                endpoint,
                headers=headers,
                timeout=3,
                data=body_string)
    except Exception as ex2:
        print("error on sync product by warehouse")