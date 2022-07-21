from bs4 import BeautifulSoup
import os
from os.path import basename
from utilities.logging_util import log_util
from configs.config import INPUT_FOLDER_TMF


def parseTxtFile(path, fileName):
    '''parse a txt file for the BCI (Blue Collar Investor stock picks'''
    fileNameParsed = fileName.split(".")[0].split("_")
    fileSource = fileNameParsed[0]  #BCI
    fileDate = fileNameParsed[1]
    
    symbolList = list()
    
    with open(path+fileName, newline='') as txtfile:
        rawtext = txtfile.readlines()
        for row in rawtext:
            stock = row.split(" ")[0]
            if stock:
                symbolList.append(stock)
        symbolList.sort()

    #specify the output file location
    OUTPUT_FILENAME = "./Output/stocks_" + fileSource + "_" + fileDate + ".txt"

    output_list_to_file(OUTPUT_FILENAME, symbolList)


def fix_list(symbolList):
    '''sometimes the symbolList needs to be corrected because two (or more) symbols 
    are combined into the same list entry.  so split each one based on a newline character 
    and then add it back to a newly created list'''
    new_symbols_set = set()
    for symbol in symbolList:
        symbols = symbol.split("\n")
        for s in symbols:
            new_symbols_set.add(s)
    
    return list(new_symbols_set)


def parseHtmlFile_DA(path, fileName):
    fileNameParsed = fileName.split(".")[0].split("_")
    tmfFileSource = fileNameParsed[1]  #SA = Stock Advisor; RB = Rule Breakers; BS = Back Stage
    tmfFileDate = fileNameParsed[2]

    with open(path+fileName,"r",encoding='utf-8') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser', from_encoding='utf-8')

    tagName = "div"
    className = "ticker-area"
    
    #get the ticker symbols from the html data
    symbolList = soup.find_all(tagName, class_=className)
    
    #clean up the symbols list data
    symbolList = list(map(lambda symbol: symbol.text.strip().split(" ")[0].replace(".",""), symbolList))
    symbolList = fix_list(symbolList)
    symbolList.sort()

    #specify the output file location    
    OUTPUT_FILENAME = f"./Output/stocks_{tmfFileSource}_{tmfFileDate}.txt"

    output_list_to_file(OUTPUT_FILENAME, symbolList)
    

def parseHtmlFile_TMF(path, fileName):
    
    fileNameParsed = fileName.split(".")[0].split("_")
    tmfFileSource = fileNameParsed[1]  #SA = Stock Advisor; RB = Rule Breakers; BS = Back Stage, TI = Total Income, ES = Everlasting Stocks
    tmfFileDate = fileNameParsed[2]

    with open(path+fileName,"r",encoding='utf-8') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser', from_encoding='utf-8')

    if tmfFileSource.upper() in ["BS", "RB", "ES", "SA", "TI"]:
        tagName = "button"
        className = "uppercase"
    else:
        raise Exception("TMF file type unknown ==> {t}".format(t=tmfFileSource))
    
    #get the ticker symbols from the html data
    symbolList = soup.find_all(tagName, class_=className)
    
    #clean up the symbols list data
    symbolList = list(map(lambda symbol: symbol.text.strip().split(" ")[0].replace(".",""), symbolList))
    symbolList = fix_list(symbolList)
    symbolList.sort()    

    #specify the output file location    
    OUTPUT_FILENAME = f"./Output/stocks_{tmfFileSource}_{tmfFileDate}.txt"

    output_list_to_file(OUTPUT_FILENAME, symbolList)


def output_list_to_file(OUTPUT_FILENAME, symbolList):
    with open(OUTPUT_FILENAME, "w") as txt_file:
        for symbol in symbolList:
            txt_file.write(symbol + "\n")
    

def main():
    
    scriptName = basename(__file__).split(".")[0]
    log_util(f"{scriptName} started", "INFO")
    
    path = "./" + INPUT_FOLDER_TMF + "/"  #the folder containing HTML files to parse for The Motley Fool webpages
    files = os.listdir(path)
    
    for fileName in files:
        log_util(f"Processing {fileName}...", "INFO")
        fileNameParts = fileName.lower().split(".")
        fileSource = fileNameParts[0].split("_")[0]
        if fileSource == "tmf": #tmf = the motley fool website
            parseHtmlFile_TMF(path, fileName)
        elif fileSource == "mb": #mb = market beat website
            parseHtmlFile_DA(path, fileName)
        else:
            raise Exception(f"Unknown file source ==> {fileSource}")

    log_util(f"{scriptName} ended", "INFO")


if __name__ == "__main__":
    main()