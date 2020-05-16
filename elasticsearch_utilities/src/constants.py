# elastic search constants
HOSTNAME = 'localhost'
PORT_NUMBER = 9200
ELASTIC_QUERY_URL = "localhost:9200/sustainability_reports/_search"
INDEX_NAME = "sustainability_reports"

# paths and csv constants
PDFS_PATH = 'pdf_ocr/data/converted'
POPULATION_CSV_PATH = 'elasticsearch_utilities/stats/' 
POPULATION_CSV_PATH_NEW = 'elasticsearch_utilities/stats_new/' 
ENTITIES_HD = ["entity", "frequency"]
ATECO_HD = ["code", "frequency"]
REVENUE_HD = ["revenue", "frequency"]


# dandelion contants
DANDELION_URL = "https://api.dandelion.eu/datatxt/nex/v1"
TOP_ENTITIES_NUMBER = 300

# atoka contants
ATOKA_URL = "https://api.atoka.io/v2/companies"
ATOKA_MATCH_URL = "https://api.atoka.io/v2/companies/match"