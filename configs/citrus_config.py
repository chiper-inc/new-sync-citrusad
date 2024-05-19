import os
CITRUS_CONFIG = {
    "IS_NEW_CATALOGE": os.getenv('IS_NEW_CATALOGE') == "True",
    "AUTH_CITRUS": os.getenv('AUTH_CITRUS'),
    "URL_CITRUS": os.getenv('URL_CITRUS'),
    "TEAM_CITRUS": os.getenv("TEAM_CITRUS"),
    "CO_CITRUS": os.getenv("CO_CITRUS"),
    "MX_CITRUS": os.getenv("MX_CITRUS"),
    "BR_CITRUS": os.getenv("BR_CITRUS"),
    "CO_CITRUS_2": os.getenv("CO_CITRUS_2"),
    "MX_CITRUS_2": os.getenv("MX_CITRUS_2"),
    "BR_CITRUS_2": os.getenv("BR_CITRUS_2"),
    "CL_CITRUS": os.getenv("CL_CITRUS")}