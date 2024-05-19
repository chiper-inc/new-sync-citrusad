from dotenv import load_dotenv
load_dotenv()

from queries.get_countries_active import get_countries_and_warehouses_active
from queries.get_products_by_country import get_products_by_country
from queries.get_product_data_by_ids import get_product_data_by_ids
from clients.mysql_client import mysql_client
from services.post_citrusad import post_product_citrusad
from services.get_pricing_service import get_pricing_service

(country_ids, contry_warehouses_metadata) = get_countries_and_warehouses_active(mysql_client)

i_country = -1
for country_id in country_ids:
    i_country = i_country + 1
    print("sincronizando")
    print(contry_warehouses_metadata[i_country][0]['country'])
    (store_reference_ids, metadata, location_store_reference_ids) = get_products_by_country(mysql_client, country_id, contry_warehouses_metadata[i_country])
    for location_key, store_reference_values in location_store_reference_ids.items():
        get_pricing_service(int(location_key), store_reference_values, store_reference_ids, metadata)
    get_product_data_by_ids(mysql_client, store_reference_ids, metadata)
    
    post_product_citrusad(metadata)
    total = len(store_reference_ids)
    print(f"{total} products was sincronyced")