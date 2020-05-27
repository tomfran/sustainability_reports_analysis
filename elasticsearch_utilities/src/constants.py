# elastic search constants
HOSTNAME = 'localhost'
PORT_NUMBER = 9200
ELASTIC_QUERY_URL = "localhost:9200/sustainability_reports/_search"
INDEX_NAME = "sustainability_reports"

# paths and csv constants
PDFS_PATH = 'pdf_ocr/data/converted'
POPULATION_CSV_PATH = 'elasticsearch_utilities/stats_old/' 
POPULATION_CSV_PATH_NEW = 'elasticsearch_utilities/stats/'
ENTITIES_HD = ["entity", "frequency"]
ATECO_HD = ["code", "frequency"]
REVENUE_HD = ["revenue", "frequency"]


# dandelion contants
DANDELION_URL = "https://api.dandelion.eu/datatxt/nex/v1"
TOP_ENTITIES_NUMBER = 300

# atoka contants
ATOKA_URL = "https://api.atoka.io/v2/companies"
ATOKA_MATCH_URL = "https://api.atoka.io/v2/companies/match"

CONSULTING_COMPANIES_LIST = [
    "Accenture", 
    "Allen Overy", 
    "Alvarez & Marsal", 
    "Andersen Tax & Legal", 
    "Antonini", 
    "Ashurst", 
    "Bana", 
    "Bain & Company", 
    "Baker & Mckenzie", 
    "Bernoni Grant Thornton", 
    "Bird & Bird", 
    "Biscozzi Nobili", 
    "Bdo", 
    "Bonelli Erede", 
    "Boston Consulting", 
    "Cafiero Pezzali Associati", 
    "Carnelutti", 
    "Castaldi Partners", 
    "Cba", 
    "Chilosi Martelli", 
    "Chiomenti", 
    "Cleary Gottlieb", 
    "Clifford Chance", 
    "Cms", 
    "Curtis", 
    "De Berti Jacchia Franchini Forlani", 
    "Delfino e Associati", 
    "Deloitte", 
    "Dentons", 
    "Di Tanno e Associati", 
    "Dla Piper", 
    "Dwf", 
    "Eversheds Sutherland", 
    "EY", 
    "Freshfields Bruckhaus Deringer", 
    "Gattai Minoli Agostinelli", 
    "Gatti Pavesi Bianchi", 
    "Gf legal", 
    "Gianni Origoni Partners", 
    "Giliberti Triscornia", 
    "Gitti & Partners", 
    "Grande Stevens", 
    "Grimaldi studio legale", 
    "Hogan Lovells", 
    "Herbert Smith Freehills", 
    "Interbrand", 
    "Jones Day", 
    "K&L Gates", 
    "King & Wood Mallesons ", 
    "Kon", 
    "Korn Ferry", 
    "Kpmg", 
    "La Scala", 
    "Lablaw", 
    "Latham & Watkins", 
    "Lawlinguists", 
    "Lca studio legale", 
    "Legalitax", 
    "Legance", 
    "Lexant", 
    "Linklaters", 
    "Lombardi Segni", 
    "LS LexJus Sinacta", 
    "Ludovici & Partners", 
    "Macchi di Cellere Gangemi", 
    "Maisto e Associati", 
    "McKinsey & Company", 
    "Morbidelli Bruni Righi Traina", 
    "Mpo & Partners", 
    "Nctm", 
    "Negri Clementi", 
    "Norton Rose Fulbright", 
    "Orrick", 
    "Osborne Clarke", 
    "Parva Consulting", 
    "Pavia e Ansaldo", 
    "Pedersoli studio legale", 
    "Pepe e Associati", 
    "Pirola Pennuto Zei", 
    "Porsche Consulting", 
    "Protiviti", 
    "PWC", 
    "R&P Legal", 
    "Roedl & Partner", 
    "Russo De Rosa", 
    "Simmons & Simmons", 
    "Strategic tax advisors", 
    "Studio legale Corte", 
    "Studio Tributario Tognolo", 
    "Sutti", 
    "Toffoletto De Luca Tamajo", 
    "Tonucci & Partners", 
    "Tosetto Weigmann", 
    "Tremonti Vitali Romagnoli Piccardi", 
    "Trevisan & Cuonzo", 
    "Trifirò & Partners", 
    "Ughi e Nunziante", 
    "White & Case", 
    "Withers LLP", 
    "Zunarelli",
    "SGM"
]