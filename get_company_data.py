from bs4 import BeautifulSoup 
import os
from os.path import basename
import requests
import re
import json
import string


folder = "Input_YF" #for reading the Yahoo Finance website

# yahoo_url = "https://finance.yahoo.com/quote/{s}?p={s}"
yahoo_url_profile = "https://finance.yahoo.com/quote/{s}/profile?p={s}"

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"


def get_webpage(url, symbol):
    
    try:
        url = yahoo_url_profile.format(s=symbol)
        webpage = requests.get(url, headers={"User-Agent": user_agent})
        if webpage.status_code == 200:
            return webpage
        else:
            msg = f"get_webpage: Page get error: {webpage.status_code}"
            print(msg)
            raise Exception(msg)
    except Exception as e:
        print(f"get_webpage: Page not found for {symbol}")
        return None


def parse_stock_page_YF(webpage):
    
    soup = BeautifulSoup(webpage.content, 'html.parser', from_encoding='utf-8')
    
    pattern = re.compile(r'\s--\sData\s--\s') #raw string
    
    try:
        script_data = soup.find('script', text=pattern).contents[0]
        start = script_data.find("context")-2
        json_data = json.loads(script_data[start:-12])
        asset_profile = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['assetProfile']
        # summary_detail = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['summaryDetail']
    except KeyError as e:
        asset_profile = None
    except Exception as e:
        print(f"parse_stock_page_YF: Error parsing Yahoo Finance data. Exception {e}")
        raise e

    return asset_profile


def output_list_to_file(outputFilename, output_data):
    with open(outputFilename, "w") as txt_file:
        for symbol, sector, industry in output_data:
            txt_file.write(f"{symbol}%{sector}%{industry}"+ "\n")


def fix_unprintable(string_parm):
    return string_parm.replace(chr(8212), "-") #8212 is an emdash, repace with a regular en dash


def process_file(symbols_file):
    output_data = list()
    
    for symbol in symbols_file:
        symbol = symbol.strip()
        print(f"Processing symbol...{symbol}")
        webpage = get_webpage(yahoo_url_profile, symbol)
        if not webpage:
            sector = "n/a"
            industry = "n/a"
            output_data.append((symbol, sector, industry))
            continue
        company_profile = parse_stock_page_YF(webpage)
        if not company_profile:
            sector = "n/a"
            industry = "n/a"
            output_data.append((symbol, sector, industry))
            continue
        try:
            sector = company_profile["sector"]
            industry = company_profile["industry"]
            for letter in industry:
                if letter not in string.printable:
                    industry = fix_unprintable(industry)
                    continue
        except KeyError as e:
            sector = "n/a"
            industry = "n/a"
        except Exception as e:
            print(f"process_file: Exception reading company profile data {e}")
            raise e
        output_data.append((symbol, sector, industry))


    outputFilename = f"./Output/company_data.txt"
    output_list_to_file(outputFilename, output_data)
    

def main():
    
    scriptName = basename(__file__).split(".")[0]
    print(f"{scriptName} started")
    
    path = "./" + folder + "/"  #the folder containing symbol file to lookup
    symbols_file = os.listdir(path)[0] #just process the first file
    # fileNameParts = symbols_file.lower().split(".")
    # fileSource = fileNameParts[0].split("_")[0]

    with open(path+symbols_file,"r",encoding='utf-8') as symbols_file:
        process_file(symbols_file)
    
    print(f"{scriptName} ended")


if __name__ == "__main__":
    main()