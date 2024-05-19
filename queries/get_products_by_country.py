import sys, os

from utils.macros_util import find_macros_by_country
from configs.citrus_config import CITRUS_CONFIG
from utils.citrus_util import get_catalogue_by_country

def __search_warehouse_by_warehouse(contry_warehouses_metadata, warehouse_id):
    for warehouse_item in contry_warehouses_metadata:
        if warehouse_item['warehouseId'] == warehouse_id:
            return warehouse_item
    return None

def __search_warehouses_by_country(contry_warehouses_metadata):
    warehouses_str = []
    for warehouse_item in contry_warehouses_metadata:
        warehouses_str.append(str(warehouse_item['warehouseId']))
    return warehouses_str    

def get_products_by_country(mysql_client, country_id, contry_warehouses_metadata):
    try:
        catalogue_id = get_catalogue_by_country(country_id)
        if catalogue_id == None:
            return ([],[],{})
        
        warehouses_arr_str = __search_warehouses_by_country(contry_warehouses_metadata)
        if len(warehouses_arr_str) == 0:
            return ([],[],{})
        warehouses_ids_string = ','.join(warehouses_arr_str)
            
        macros = find_macros_by_country(country_id)
        print(macros)
        if len(macros) == 0:
            return ([],[],{})
        
        macro_ids_string = ','.join(macros)
        query = f"""
            SELECT  p.storeReferenceId, p.warehouseId
            FROM Product p 
            WHERE p.warehouseId IN  ({warehouses_ids_string})
            AND p.storeReferenceId  IN (
            	SELECT DISTINCT (rp.storeReferenceId)
            	FROM ReferencePortfolio rp
            	WHERE rp.deletedAt is NULL 
            	and rp.sellingPortfolioStatusId = 1)
            AND p.storeReferenceId IN (
                SELECT DISTINCT(sr.id)
                FROM StoreReference sr
                JOIN ReferenceCategorization  refcat ON (refcat.storeReferenceId = sr.id)
                JOIN Categorization  cat ON (cat.id = refcat.categorizationId)
                JOIN SubCategory subCat ON (subCat.id = cat.subCategoryId)
                JOIN Category category ON (category.id = subCat.categoryId)
                JOIN MacroCategory  macro ON (macro.id = category.macroId)
                WHERE cat.deletedAt IS NULL
                AND subCat.deletedAt IS NULL
                AND category.deletedAt IS NULL
                AND macro.deletedAt IS NULL
                AND macro.id  IN ({macro_ids_string})  
            )
            AND p.deletedAt IS NULL
            GROUP BY p.storeReferenceId, p.warehouseId
            ORDER BY p.storeReferenceId"""
        cursor = mysql_client.cursor(buffered=True)
        mysql_client.ping(reconnect=True)
        cursor.execute(query)
        store_reference_tmp = -1
        (store_reference_ids, metadata) = ([],[])
        location_store_reference_ids = {}
        for (store_reference_id, warehouse_id) in cursor:
            store_reference_id_int = -1
            try:
                store_reference_id_int = int(store_reference_id)
            except _:
                continue

            warehouse_id_int = -1
            try:
                warehouse_id_int = int(warehouse_id)
            except _:
                continue

            inventory = 10000
            if store_reference_tmp != store_reference_id_int:
                store_reference_tmp = store_reference_id_int
                store_reference_ids.append(store_reference_id_int)
                metadata.append({
                    "gtin": str(store_reference_id_int),
                    "sellerId":"",
                    "catalogId":catalogue_id,
                    "productCollection":None,
                    "price":100,
                    "teamId": CITRUS_CONFIG['TEAM_CITRUS'],
                    'groups':[],
                    "filters": [],
                    "inventory": inventory,
                    "profit": None,
                    "tags":[]})
            warehouse_item = __search_warehouse_by_warehouse(contry_warehouses_metadata, warehouse_id_int )
            location_name = warehouse_item['location']
            location_id = warehouse_item['locationId']
            if f"locationId:{location_id}" not in metadata[-1]['filters']:
                metadata[-1]['filters'] = metadata[-1]['filters'] + [
                    f"location:{location_name}",
                    f"locationId:{location_id}"]
            if location_id not in location_store_reference_ids:
                location_store_reference_ids[location_id] = [store_reference_id_int]
            else:
                location_store_reference_ids[location_id].append(store_reference_id_int)
            metadata[-1]['filters'] = metadata[-1]['filters'] + [
                f"warehouseId:{warehouse_id_int}-1"]

        cursor.close()
        return (store_reference_ids, metadata, location_store_reference_ids)
    except Exception as er:
        print(er)
        print("error on products by country")
        exc_type, _, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)        
        return ([],[],{})