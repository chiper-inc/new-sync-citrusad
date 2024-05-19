from configs.citrus_config import CITRUS_CONFIG

def get_catalogue_by_country(country_id):
    if country_id == 6:
        return CITRUS_CONFIG['CO_CITRUS']
    elif country_id == 7:
        return CITRUS_CONFIG['MX_CITRUS']
    elif country_id == 8:
        return CITRUS_CONFIG['BR_CITRUS']
    elif country_id ==10:
        return CITRUS_CONFIG['CL_CITRUS']
    return None
        