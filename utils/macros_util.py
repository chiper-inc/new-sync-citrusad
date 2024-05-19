from utils.list_utils import map_list_int_to_list_str
__meta_locations = [
        {
            "locations":[2,3,4,5,6,7,8,9,13,14,18],
            "macros":[179,177,178,173,170,169,175,180,176,167,172,171,168],
            "country":"Colombia",
            "country_id": 6
        },
        {
            "locations":[11,12,16,19,20],
            "macros":[183,186,187,182,191,195,190,184,185,188,193,192,194],
            "country":"Mexico",
            "country_id": 7
        },
        {
            "locations":[21],
            "macros":[246,247,248,249,250,251,253,254,255,256,257,261,262,263,264,265,266,267,268,272],
            "country":"Brasil",
            "country_id": 8
        },
        {
            "locations":[22],
            "macros":[269,270,271,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287],
            "country":"Chile",
            "country_id": 10
        },
    ]

def find_macros_by_country(country_id):
    print(country_id)
    for meta_location in __meta_locations:
        if meta_location['country_id'] == country_id:
            return map_list_int_to_list_str(meta_location['macros'])
    return []