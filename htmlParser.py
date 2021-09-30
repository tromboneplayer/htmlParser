from datetime import datetime, date
import json
from bs4 import BeautifulSoup
import os


#sometimes the symbolList needs to be corrected because two (or more) symbols are 
#combined into the same list entry.  so split each one based on a newline character
#and then add it back to a newly created list
def fix_list(symbolList):
    new_symbols_set = set()
    for symbol in symbolList:
        symbols = symbol.split("\n")
        for s in symbols:
            new_symbols_set.add(s)
    
    return list(new_symbols_set)


def parseFile(path, fileName):
    
    fileNameParsed = fileName.split(".")[0].split("_")
    tmfFileSource = fileNameParsed[1]  #SA = Stock Advisor; RB = Rule Breakers; BS = Back Stage
    tmfFileDate = fileNameParsed[2]
        
    with open(path+fileName,"r",encoding='utf-8') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser', from_encoding='utf-8')

    if tmfFileSource in ["BS", "RB"]:
        tagName = "span"
        className = "ticker"
    elif tmfFileSource == "SA":
        tagName = "div"
        className = "company-text"
    else:
        raise Exception("TMF file type unknown")
    
    #get the ticker symbols from the html data
    symbolList = soup.find_all(tagName, class_=className)
    
    #clean up the symbols list data
    symbolList = list(map(lambda symbol: symbol.text.strip().split(" ")[0].replace(".",""), symbolList))
    symbolList = fix_list(symbolList)
    symbolList.sort()    

    #specify the output file location    
    outputFilename = "./Output/stocks_" + tmfFileSource + "_" + tmfFileDate + ".txt"

    with open(outputFilename, "w") as txt_file:
        for symbol in symbolList:
            txt_file.write(symbol + "\n")


def main():
    
    print("htmlParser started")
    path = "./Input/"  #the folder containing HTML files to parse for The Motley Fool webpages
    files = os.listdir(path)
    
    for fileName in files:
        print("Processing {f}...".format(f=fileName))
        parseFile(path, fileName)
        
    print("htmlParser ended")


if __name__ == "__main__":
    main()