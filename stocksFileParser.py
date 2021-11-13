from datetime import datetime, date
import json
from bs4 import BeautifulSoup
import os
import csv


#folder = "Test"
folder = "Input"


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
    outputFilename = "./Output/stocks_" + fileSource + "_" + fileDate + ".txt"

    output_list_to_file(outputFilename, symbolList)


def parseCsvFile_ARKK(path, fileName):
    '''parse a csv file for the AARK (Cathie Wood) holdings fund'''
    fileNameParsed = fileName.split(".")[0].split("_")
    fileSource = fileNameParsed[0]  #ARKK
    fileDate = fileNameParsed[2]
    
    symbolList = list()
    
    with open(path+fileName, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            stock = row[3]
            if stock:
                symbolList.append(stock)
        del(symbolList[0])
        symbolList.sort()

    #specify the output file location
    outputFilename = "./Output/stocks_" + fileSource + "_" + fileDate + ".txt"
    
    output_list_to_file(outputFilename, symbolList)


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


def parseHtmlFile_TMF(path, fileName):
    
    fileNameParsed = fileName.split(".")[0].split("_")
    tmfFileSource = fileNameParsed[1]  #SA = Stock Advisor; RB = Rule Breakers; BS = Back Stage
    tmfFileDate = fileNameParsed[2]
        
    with open(path+fileName,"r",encoding='utf-8') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser', from_encoding='utf-8')

    if tmfFileSource.upper() in ["BS", "RB"]:
        tagName = "span"
        className = "ticker"
    elif tmfFileSource.upper() == "SA":
        tagName = "div"
        className = "company-text"
    else:
        raise Exception("TMF file type unknown ==> {t}".format(t=tmfFileSource))
    
    #get the ticker symbols from the html data
    symbolList = soup.find_all(tagName, class_=className)
    
    #clean up the symbols list data
    symbolList = list(map(lambda symbol: symbol.text.strip().split(" ")[0].replace(".",""), symbolList))
    symbolList = fix_list(symbolList)
    symbolList.sort()    

    #specify the output file location    
    outputFilename = "./Output/stocks_" + tmfFileSource + "_" + tmfFileDate + ".txt"

    output_list_to_file(outputFilename, symbolList)


def output_list_to_file(outputFilename, symbolList):
    with open(outputFilename, "w") as txt_file:
        for symbol in symbolList:
            txt_file.write(symbol + "\n")
    

def main():
    
    print("stocksFileParser started")
    path = "./" + folder + "/"  #the folder containing HTML files to parse for The Motley Fool webpages
    files = os.listdir(path)
    
    for fileName in files:
        print("Processing {f}...".format(f=fileName))
        fileNameParts = fileName.lower().split(".")
        fileSource = fileNameParts[0].split("_")[0]
        if fileSource == "tmf":
            parseHtmlFile_TMF(path, fileName)
        elif fileSource == "arkk":
            parseCsvFile_ARKK(path, fileName)
        else:
            raise Exception("Unknown file source ==> {s}".format(e=fileSource))

    print("stocksFileParser ended")


if __name__ == "__main__":
    main()