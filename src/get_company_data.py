import os
from os.path import basename
from utilities.logging_util import log_util
from services.services import process_file
from configs.config import INPUT_FOLDER_YF, OUTPUT_FILENAME_YF, INPUT_FILE_YF


def main():
    
    scriptName = basename(__file__).split(".")[0]
    log_util(f"{scriptName} started", "INFO")
    
    path = f"./{INPUT_FOLDER_YF}/"  #the folder containing symbol file to lookup
    
    # symbols_file = os.listdir(path)[0] #just process the first file
    # fileNameParts = symbols_file.lower().split(".")
    # fileSource = fileNameParts[0].split("_")[0]

    with open(path+INPUT_FILE_YF,"r",encoding='utf-8') as symbols_file:
        company_profile_data = process_file(symbols_file)
    
    with open(OUTPUT_FILENAME_YF, "w") as txt_file:
        for company_profile in company_profile_data:
            symbol = company_profile["symbol"]
            sector = company_profile["sector"]
            industry = company_profile["industry"]
            txt_file.write(f"{symbol}%{sector}%{industry}"+ "\n")

    log_util(f"{scriptName} ended", "INFO")


if __name__ == "__main__":
    main()