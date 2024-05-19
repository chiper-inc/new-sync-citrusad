def get_countries_active(mysql_client):
    try:
        query = f"""
            SELECT id
            FROM Country c 
            WHERE c.deletedAt  IS NULL"""
        cursor = mysql_client.cursor()
        mysql_client.ping(reconnect=True)
        cursor.execute(query)
        country_ids = []
        for (id) in cursor:
            country_ids.append(int(id))

        cursor.close()
        return country_ids
    except Exception as _:
        print("error on countries")
        return []