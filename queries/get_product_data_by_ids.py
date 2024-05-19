import sys, os

from utils.list_utils import map_list_int_to_list_str, binary_search
def get_product_data_by_ids(mysql_client, store_reference_ids, metadata):
    try:
        store_references = map_list_int_to_list_str(store_reference_ids)
        store_references_ids_string = ','.join(store_references)

        query = f"""
        SELECT 
            sr.id as id,
            sr.brandId  as brandId,
            b.name  as brandName,
            subCat.id as subCategoryId,
            subCat.name  as subCategoryName,
            COALESCE(r.displayName, 'Sin Nombre') as name,
            macro.id  as macroId,
            macro.name as macroName,
            r.sku  as sku,
            com.id  as companyId,
            com.name as company,
            CONCAT('https://d221xxk5mfaxk5.cloudfront.net/', COALESCE(i.medium, 'app/no-image-ryahXCwGV-M.jpg')) AS medium,
            category.name as categoryName,
        	category.id as categoryId
        
        FROM StoreReference as sr
        JOIN Brand b ON (b.id = sr.brandId)
        JOIN Company  com on (com.id = b.companyId)
        JOIN Reference r ON (r.id = sr.referenceId)
        JOIN Image i ON (i.id = sr.image)
        JOIN ReferenceCategorization  refcat ON (refcat.storeReferenceId = sr.id)
        JOIN Categorization  cat ON (cat.id = refcat.categorizationId)
        JOIN SubCategory subCat ON (subCat.id = cat.subCategoryId)
        JOIN Category category ON (category.id = subCat.categoryId)
        JOIN MacroCategory  macro ON (macro.id = category.macroId)
       
        WHERE b.deletedAt IS NULL
        AND r.deletedAt IS NULL 
        AND com.deletedAt IS NULL
        AND i.deletedAt IS NULL
        AND refcat.deletedAt IS NULL
        AND cat.deletedAt IS NULL
        AND subCat.deletedAt IS NULL
        AND category.deletedAt IS NULL
        AND macro.deletedAt  IS NULL
        AND sr.id IN ({store_references_ids_string})

        ORDER BY sr.id"""
        cursor = mysql_client.cursor(buffered=True)
        mysql_client.ping(reconnect=True)
        cursor.execute(query)
        for (id, brand_id, brand_name, sub_category_id, sub_category_name, name, macro_id,
             macro_name, sku, company_id, company_name, image, category_name, category_id) in cursor:
            id_int = -1
            try:
                id_int = int(id)
            except _:
                continue 
            brand_id_int = -1
            try:
                brand_id_int = int(brand_id)
            except _:
                None 
            sub_category_id_int = -1
            try:
                sub_category_id_int = int(sub_category_id)
            except _:
                None 
            macro_id_int = -1
            try:
                macro_id_int = int(macro_id)
            except _:
                None
            company_id_int = -1
            try:
                company_id_int = int(company_id)
            except _:
                None  
            category_id_int = -1
            try:
                category_id_int = int(category_id)
            except _:
                None

            idx_store_reference = binary_search(store_reference_ids, id_int)
            if idx_store_reference == -1:
                continue

            metadata[idx_store_reference]['filters'] = metadata[idx_store_reference]['filters'] + [
                f"brand:{brand_name}",
                f"brandId:{brand_id_int}",
                f"category:{category_name}", 
                f"categoryId:{category_id_int}",
                f"macroId:{macro_id_int}",
                f"macrocategory:{macro_name}",
                f"subcategory:{sub_category_name}",
                f"subcategoryId:{sub_category_id_int}"]
            
            metadata[idx_store_reference]['tags'] =  metadata[idx_store_reference]['tags'] + [
                f"imageurl:{image}",
                f"name:{sku} - {name}"]               
        cursor.close()
    except Exception as _:
        print("error on countries")
        exc_type, _, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)    