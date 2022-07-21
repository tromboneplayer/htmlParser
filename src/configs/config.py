SOURCE_FOLDER = "src/"

#Yahoo Finance input and output files
INPUT_FOLDER_YF = f"{SOURCE_FOLDER}Input_YF" #for reading the Yahoo Finance website
INPUT_FILE_YF = "Symbols.txt"
OUTPUT_FILENAME_YF = f"{SOURCE_FOLDER}/Output/company_data.txt"

#The Motley Fool input files
INPUT_FOLDER_TMF = f"{SOURCE_FOLDER}Input_TMF"
OUTPUT_FOLDER_TMF = f"{SOURCE_FOLDER}/Output"

# yahoo_url = "https://finance.yahoo.com/quote/{s}?p={s}"
YAHOO_URL_PROFILE = "https://finance.yahoo.com/quote/{s}/profile?p={s}"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"


USE_YF_LIBRARY = False  # the yahoo finance library is slower than just retrieving from the website.  Set to true to use the library.

NOT_AVAILABLE = "n/a"