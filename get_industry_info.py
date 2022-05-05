from fileinput import filename
from bs4 import BeautifulSoup, SoupStrainer 
import os
from os.path import basename
import csv
import urllib.request
import requests


#folder = "Test"
folder = "Input_MS" #for reading the Morningstar website
exchanges = ["xnas", "xnys","arcx", "pinx","xcse"]
types = ["stocks","etfs"]
morningstar_url = "https://www.morningstar.com/{t}/{e}/{s}/quote"


def get_webpage(symbol):

    for type in types:
        for exchange in exchanges:
            url = morningstar_url.format(e=exchange, s=symbol, t=type)
            webpage = requests.get(url)
            if webpage.status_code == 200:
                return exchange, type, webpage

    raise Exception(f"get_webpage: page not found for {symbol} at {exchange}")


def parse_etf_page(webpage):
    return "n/a", "n/a"


def parse_stock_page(webpage):

    soup = BeautifulSoup(webpage.content, 'html.parser', from_encoding='utf-8')
    
    tagName = "div"
    className = "stock__profile"
    
    #get the ticker symbols from the html data
    stock_profile_items = soup.find(tagName, class_=className).find_all("span")    
    stock_profile_items = list(map(lambda item:item.text.strip(), stock_profile_items))
    
    if "Sector" in stock_profile_items:
        sector_idx = stock_profile_items.index("Sector") + 1
        sector = stock_profile_items[sector_idx]
        
    if "Industry" in stock_profile_items:
        industry_idx = stock_profile_items.index("Industry") + 1
        industry = stock_profile_items[industry_idx]
        
    if "Investment Style" in stock_profile_items:
        style_idx = stock_profile_items.index("Investment Style") + 1
        style = stock_profile_items[style_idx]
    
    if sector is None:
        sector = "n/a"
    
    if industry is None:
        industry = "n/a"
        
    return sector, industry


def output_list_to_file(outputFilename, output_data):
    with open(outputFilename, "w") as txt_file:
        for symbol, sector, industry in output_data:
            txt_file.write(f"{symbol}, {sector}, {industry}"+ "\n")


def process_file(symbols_file):
    output_data = list()
    
    for symbol in symbols_file:
        symbol = symbol.strip()
        print(f"Processing symbol...{symbol}")
        try:
            exchange, type, webpage = get_webpage(symbol)
        except Exception as e:
            print(e)
            type = ""
        if type == "stocks":
            sector, industry = parse_stock_page(webpage)
        elif type == "etfs":
            sector, industry = parse_etf_page(webpage)
        else:
            msg = f"type {type} is not supported yet"
            sector = ""
            industry = ""
        
        output_data.append((symbol, sector, industry))
        
    outputFilename = f"./Output/sectors_industries.txt"
    output_list_to_file(outputFilename, output_data)
    

def main():
    
    scriptName = basename(__file__).split(".")[0]
    print(f"{scriptName} started")
    
    path = "./" + folder + "/"  #the folder containing HTML files to parse for The Motley Fool webpages
    symbols_file = os.listdir(path)[0]
    fileNameParts = symbols_file.lower().split(".")
    fileSource = fileNameParts[0].split("_")[0]

    with open(path+symbols_file,"r",encoding='utf-8') as symbols_file:
        process_file(symbols_file)
    # symbols = ["AAPL", "F", "MSFT", "TSLA", "W", "SPY"]
    
    print(f"{scriptName} ended")


if __name__ == "__main__":
    main()