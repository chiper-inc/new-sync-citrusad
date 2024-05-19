
import sys, os

def get_countries_and_warehouses_active(mysql_client):
    try:
        query = f"""
            SELECT  c2.id,
            c2.name,
            w.id,
            w.name,
            l.id,
            l.name
            FROM WarehouseLocation wl 
            JOIN Warehouse w  ON (w.id = wl.warehouseId)
            JOIN Location l  ON (l.id=wl.locationId)
            JOIN City c ON (l.cityId = c.id)
            JOIN Country c2 ON (c2.id = c.countryId)
            WHERE l.deletedAt IS NULL
            AND c2.deletedAt IS NULL
            ORDER BY c2.id"""
        cursor = mysql_client.cursor()
        mysql_client.ping(reconnect=True)
        cursor.execute(query)
        (country_ids, contry_warehouses_metadata) = ([],[])
        country_id_tmp = -1
        for (country_id, country_name, warehouse_id, warehouse_name, location_id, location_name) in cursor:
            country_id_int = -1
            try:
                country_id_int = int(country_id)
            except _:
                continue               
            warehouse_id_int = -1
            try:
                warehouse_id_int = int(warehouse_id)
            except _:
                continue     
            location_id_int = -1
            try:
                location_id_int = int(location_id)
            except _:
                continue
            if country_id_int != country_id_tmp:
                country_id_tmp = country_id_int
                country_ids.append(country_id_int)
                contry_warehouses_metadata.append([])
            
            contry_warehouses_metadata[-1].append({
                    'country': country_name,
                    'countryId': country_id_int,
                    'warehouseId': warehouse_id_int,
                    'warehouse': warehouse_name,
                    'locationId':location_id_int,
                    'location': location_name})

        cursor.close()
        return  (country_ids, contry_warehouses_metadata)
    except Exception as _:
        print("error on countries")
        exc_type, _, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return ([],[])